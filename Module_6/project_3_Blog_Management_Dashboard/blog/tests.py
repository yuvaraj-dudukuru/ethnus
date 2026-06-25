# ============================================================================
#  tests.py — automated checks for the two most important rules
# ----------------------------------------------------------------------------
#  Run every test with:   python manage.py test
#
#  We test:
#    1) A STRANGER cannot edit someone else's post (PATCH -> 403 Forbidden).
#    2) DRAFT posts are NOT shown in the public, anonymous list.
#
#  Each test uses a temporary throwaway database, so your real data is safe.
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from blog.models import Post


class BlogAPITest(APITestCase):

    def setUp(self):
        # Two different users: the real author and a stranger.
        self.author = User.objects.create_user('author', password='pass12345')
        self.stranger = User.objects.create_user('stranger', password='pass12345')

        # A published post written by 'author'.
        self.post = Post.objects.create(
            title='Django Tips', body='Some helpful tips.',
            author=self.author, status='P',
        )

    def test_stranger_cannot_edit_post(self):
        # The stranger logs in and tries to change someone else's post.
        self.client.force_authenticate(self.stranger)
        r = self.client.patch(
            f'/api/posts/{self.post.slug}/',
            {'title': 'Hacked title'},
        )
        # 403 = "Forbidden" — IsOwnerOrReadOnly blocked it.
        self.assertEqual(r.status_code, 403)

    def test_drafts_hidden_from_anonymous_list(self):
        # Add a DRAFT post by the author.
        Post.objects.create(
            title='Secret Draft', body='Not finished yet.',
            author=self.author, status='D',
        )
        # An anonymous visitor lists the posts.
        r = self.client.get('/api/posts/')
        self.assertEqual(r.status_code, 200)

        # Collect the titles that came back. The draft must NOT be among them.
        titles = [item['title'] for item in r.data['results']]
        self.assertIn('Django Tips', titles)        # published post IS shown
        self.assertNotIn('Secret Draft', titles)    # draft is HIDDEN
