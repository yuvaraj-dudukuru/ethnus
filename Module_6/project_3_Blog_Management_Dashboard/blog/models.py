# ============================================================================
#  models.py — the database design (reused from Module-4 Project 3)
# ----------------------------------------------------------------------------
#  Three tables plus Django's built-in User:
#
#      User 1 ───< N Post >─── N 1 Category
#      User 1 ───< N Comment >─── N 1 Post
#
#  - A User (author) writes many Posts and many Comments.
#  - A Post belongs to one Category and has many Comments.
#  - Each Post has a unique "slug" — a clean, URL-friendly version of its
#    title (e.g. "Django Tips" -> "django-tips") used in the web address.
# ============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """A topic a post can belong to, e.g. 'Python' or 'Travel'."""
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = 'categories'   # nicer label in the admin

    def __str__(self):
        return self.name


class Post(models.Model):
    """One blog article."""

    # Posts are either a private Draft or a public Published article. Only
    # Published posts appear in the public list; drafts are hidden from others.
    STATUS_CHOICES = [
        ('D', 'Draft'),
        ('P', 'Published'),
    ]

    title = models.CharField(max_length=200)

    # The slug is the clean text used in the URL. We fill it in automatically
    # from the title (see save() below), so the API client never sends it.
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    body = models.TextField()

    # The author. This points at Django's built-in User table. CASCADE means
    # if a user is deleted, their posts go too. related_name='posts' lets us
    # write user.posts.all().
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # The category. SET_NULL means if a category is deleted, the post stays
    # but its category becomes empty. null=True allows "no category".
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts',
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')

    # --- NEW in Module 6: a simple "likes" counter ---------------------------
    # A whole number that goes up by one each time someone likes the post. It is
    # changed ONLY by the 'like' action in api_views.py (never by the client
    # directly), which is why the serializer marks it read-only. This single
    # field is what powers the optimistic-UI "heart" button on the dashboard.
    likes = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)   # set once, on creation
    updated = models.DateTimeField(auto_now=True)       # refreshed on every save

    class Meta:
        ordering = ['-created']   # newest posts first

    def save(self, *args, **kwargs):
        """Auto-generate a unique slug from the title if one isn't set."""
        if not self.slug:
            base = slugify(self.title)        # "Django Tips!" -> "django-tips"
            slug = base
            counter = 1
            # If that slug is already taken, add -2, -3, ... until it's unique.
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """A reader's comment attached to one post."""

    # Which post this comment is on. related_name='comments' lets us write
    # post.comments.all().
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # Who wrote the comment (a logged-in user).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']   # oldest comments first (natural reading order)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
