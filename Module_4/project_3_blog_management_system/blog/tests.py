from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Post, Comment

class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            body='This is a test body',
            author=self.user,
            category=self.category,
            status='P'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            body='Nice post!'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Tech')
        self.assertEqual(str(self.category), 'Tech')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(str(self.post), 'Test Post')
        self.assertEqual(self.post.status, 'P')

    def test_comment_creation(self):
        self.assertEqual(self.comment.body, 'Nice post!')
        self.assertIn('Comment by testuser', str(self.comment))

class BlogViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.category = Category.objects.create(name='Django', slug='django')
        self.post1 = Post.objects.create(
            title='Django Post', slug='django-post', body='Body 1',
            author=self.user1, category=self.category, status='P'
        )
        self.draft_post = Post.objects.create(
            title='Draft Post', slug='draft-post', body='Draft body',
            author=self.user1, category=self.category, status='D'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Post')
        self.assertNotContains(response, 'Draft Post') # Only published posts

    def test_category_list_view(self):
        response = self.client.get(reverse('blog:category_list', kwargs={'slug': 'django'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:detail', kwargs={'slug': 'django-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Post')

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('blog:dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_dashboard_view_authenticated(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('blog:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Post')
        self.assertContains(response, 'Draft Post')

    def test_post_create_view(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'slug': 'new-post',
            'body': 'This is new',
            'category': self.category.id,
            'status': 'P'
        })
        self.assertEqual(response.status_code, 302) # Redirects to detail
        self.assertTrue(Post.objects.filter(slug='new-post').exists())

    def test_post_update_view_authorized(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('blog:post_update', kwargs={'slug': 'django-post'}), {
            'title': 'Updated Title',
            'slug': 'django-post',
            'body': 'Updated body',
            'category': self.category.id,
            'status': 'P'
        })
        self.assertEqual(response.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Title')

    def test_post_update_view_unauthorized(self):
        self.client.login(username='user2', password='password')
        response = self.client.post(reverse('blog:post_update', kwargs={'slug': 'django-post'}), {
            'title': 'Hacked Title',
            'slug': 'django-post',
            'body': 'Hacked body',
            'category': self.category.id,
            'status': 'P'
        })
        self.assertEqual(response.status_code, 403) # Forbidden
        self.post1.refresh_from_db()
        self.assertNotEqual(self.post1.title, 'Hacked Title')

    def test_add_comment(self):
        self.client.login(username='user2', password='password')
        response = self.client.post(reverse('blog:add_comment', kwargs={'slug': 'django-post'}), {
            'body': 'Great post!'
        })
        self.assertRedirects(response, reverse('blog:detail', kwargs={'slug': 'django-post'}))
        self.assertTrue(Comment.objects.filter(body='Great post!').exists())
