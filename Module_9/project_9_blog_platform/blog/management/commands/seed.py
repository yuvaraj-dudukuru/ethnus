# ============================================================================
#  seed.py — admin/admin + an author + sample posts and comments.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from blog.models import Category, Post, Comment


class Command(BaseCommand):
    help = "Create admin/admin, author1/author and sample blog content."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@blog.test", "admin")
        author, _ = User.objects.get_or_create(username="author1")
        author.set_password("author")
        author.save()
        reader, _ = User.objects.get_or_create(username="reader1")
        reader.set_password("reader")
        reader.save()
        self.stdout.write(self.style.SUCCESS(
            "Users: admin/admin, author1/author, reader1/reader."))

        tech, _ = Category.objects.get_or_create(name="Technology")
        life, _ = Category.objects.get_or_create(name="Lifestyle")

        p1, _ = Post.objects.get_or_create(
            title="Getting Started with Django",
            defaults={"author": author, "body": "Django makes web dev fun. **Bold** ideas!",
                      "status": "PUBLISHED", "category": tech})
        Post.objects.get_or_create(
            title="My Draft Idea",
            defaults={"author": author, "body": "Still cooking…",
                      "status": "DRAFT", "category": life})

        Comment.objects.get_or_create(
            post=p1, user=reader, defaults={"body": "Great intro, thanks!"})

        self.stdout.write(self.style.SUCCESS(
            "Seeded posts and a comment. Run: python manage.py runserver"))
