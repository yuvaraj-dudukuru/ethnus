# ============================================================================
#  seed.py — one-command setup helper:  python manage.py seed
# ----------------------------------------------------------------------------
#  Sets up everything you need to start playing with the API:
#
#     1) An admin account  -> username "admin",  password "admin"
#     2) A normal writer   -> username "writer", password "writer"
#        (a regular, non-admin user — perfect for testing "owner only" edits)
#     3) Sample categories, posts (published + a draft) and a comment.
#
#  Safe to run more than once (uses get_or_create). Run it right after migrate.
# ============================================================================
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment


class Command(BaseCommand):
    help = "Create admin + writer accounts and some sample blog data."

    def handle(self, *args, **options):
        # --- 1) The admin (superuser): admin / admin ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@blog.test', 'admin')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))
        else:
            self.stdout.write("Admin user already exists — skipping.")

        # --- 2) A normal writer account: writer / writer ---
        writer, created = User.objects.get_or_create(
            username='writer', defaults={'email': 'writer@blog.test'}
        )
        if created:
            writer.set_password('writer')
            writer.save()
            self.stdout.write(self.style.SUCCESS("Created writer user (writer / writer)."))

        # --- 3) Sample categories ---
        python_cat, _ = Category.objects.get_or_create(name='Python')
        travel_cat, _ = Category.objects.get_or_create(name='Travel')

        # --- Sample posts (slug is auto-generated from the title) ---
        post1, _ = Post.objects.get_or_create(
            title='Django Tips',
            defaults={
                'body': 'Always use select_related to avoid N+1 queries.',
                'author': writer, 'category': python_cat, 'status': 'P',  # Published
            },
        )
        Post.objects.get_or_create(
            title='Visiting Japan',
            defaults={
                'body': 'Cherry blossoms are best in early April.',
                'author': writer, 'category': travel_cat, 'status': 'P',
            },
        )
        # A DRAFT post — it will be HIDDEN from the public list, but visible to
        # its author at /api/my-posts/.
        Post.objects.get_or_create(
            title='Unfinished Draft',
            defaults={
                'body': 'Still writing this one...',
                'author': writer, 'category': python_cat, 'status': 'D',  # Draft
            },
        )

        # --- A sample comment on the first post ---
        Comment.objects.get_or_create(
            post=post1, user=writer,
            defaults={'body': 'Great tip, thanks!'},
        )

        self.stdout.write(self.style.SUCCESS(
            "Sample categories, posts and a comment are ready. "
            "Start the server with: python manage.py runserver"
        ))
