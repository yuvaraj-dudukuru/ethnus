# ============================================================================
#  tests.py — Blog API checks.  Run with:  python manage.py test
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Post


class BlogAPITests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user("author1", password="x")
        self.other = User.objects.create_user("other", password="x")
        self.published = Post.objects.create(
            author=self.author, title="Hello World", body="published body",
            status="PUBLISHED")
        self.draft = Post.objects.create(
            author=self.author, title="Secret Draft", body="wip", status="DRAFT")

    def test_anonymous_sees_published_not_draft(self):
        self.assertEqual(
            self.client.get(f"/api/posts/{self.published.slug}/").status_code, 200)
        self.assertEqual(
            self.client.get(f"/api/posts/{self.draft.slug}/").status_code, 404)

    def test_author_can_see_own_draft(self):
        self.client.force_authenticate(self.author)
        self.assertEqual(
            self.client.get(f"/api/posts/{self.draft.slug}/").status_code, 200)

    def test_other_user_cannot_see_draft(self):
        self.client.force_authenticate(self.other)
        self.assertEqual(
            self.client.get(f"/api/posts/{self.draft.slug}/").status_code, 404)

    def test_author_only_can_edit(self):
        self.client.force_authenticate(self.other)
        self.assertEqual(
            self.client.patch(f"/api/posts/{self.published.slug}/",
                              {"title": "Hacked"}).status_code, 403)
        self.client.force_authenticate(self.author)
        self.assertEqual(
            self.client.patch(f"/api/posts/{self.published.slug}/",
                              {"title": "Edited"}).status_code, 200)

    def test_anonymous_cannot_comment(self):
        r = self.client.post("/api/comments/",
                            {"post": self.published.id, "body": "hi"})
        self.assertEqual(r.status_code, 401)

    def test_authenticated_can_comment(self):
        self.client.force_authenticate(self.other)
        r = self.client.post("/api/comments/",
                            {"post": self.published.id, "body": "nice post"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["user"], "other")

    def test_like_toggles(self):
        self.client.force_authenticate(self.other)
        on = self.client.post(f"/api/posts/{self.published.slug}/like/")
        self.assertTrue(on.data["liked"])
        self.assertEqual(on.data["like_count"], 1)
        off = self.client.post(f"/api/posts/{self.published.slug}/like/")
        self.assertFalse(off.data["liked"])
        self.assertEqual(off.data["like_count"], 0)
