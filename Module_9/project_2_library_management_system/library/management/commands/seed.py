# ============================================================================
#  seed.py — admin/admin + a demo member + sample catalogue.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.models import Author, Book, Member


class Command(BaseCommand):
    help = "Create admin/admin, a demo member and sample books."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@lib.test", "admin")
            self.stdout.write(self.style.SUCCESS("Created admin/admin (librarian)."))

        if not User.objects.filter(username="member1").exists():
            u = User.objects.create_user("member1", password="member")
            Member.objects.get_or_create(user=u, defaults={"name": "Demo Member"})
            self.stdout.write(self.style.SUCCESS("Created member1/member."))

        rowling, _ = Author.objects.get_or_create(name="J. K. Rowling")
        orwell, _ = Author.objects.get_or_create(name="George Orwell")
        knuth, _ = Author.objects.get_or_create(name="Donald Knuth")

        books = [
            ("Harry Potter", rowling, "978-0001", 3),
            ("1984", orwell, "978-0002", 2),
            ("Animal Farm", orwell, "978-0003", 1),
            ("The Art of Computer Programming", knuth, "978-0004", 2),
        ]
        for title, author, isbn, copies in books:
            Book.objects.get_or_create(
                isbn=isbn,
                defaults={"title": title, "author": author,
                          "copies_total": copies, "copies_available": copies})

        self.stdout.write(self.style.SUCCESS(
            "Seeded authors, books and a demo member. Run: python manage.py runserver"))
