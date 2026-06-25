# ============================================================================
#  seed.py — one-command setup helper:  python manage.py seed
# ----------------------------------------------------------------------------
#  Sets up everything you need to start playing with the API:
#
#     1) An admin account        -> username "admin",     password "admin"
#     2) A "Librarians" group with ALL book/member/issue permissions, plus a
#        sample librarian account -> username "librarian", password "librarian"
#        (this demonstrates the DjangoModelPermissions group-based access).
#     3) Sample authors, books and members so the API has data to show.
#
#  Safe to run more than once (it uses get_or_create, so no duplicates).
#  Run it right after "migrate".
# ============================================================================
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from library.models import Author, Book, Member


class Command(BaseCommand):
    help = "Create admin + librarian accounts and some sample data."

    def handle(self, *args, **options):
        # --- 1) The admin (superuser) account: admin / admin ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@college.edu', 'admin')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))
        else:
            self.stdout.write("Admin user already exists — skipping.")

        # --- 2) The "Librarians" group with all library model permissions ---
        librarians, _ = Group.objects.get_or_create(name='Librarians')
        # Grab every permission that belongs to our 'library' app (add/change/
        # delete/view for Author, Book, Member, Issue) and give them to the group.
        lib_perms = Permission.objects.filter(content_type__app_label='library')
        librarians.permissions.set(lib_perms)

        # A sample librarian user who belongs to that group: librarian / librarian
        librarian, created = User.objects.get_or_create(
            username='librarian',
            defaults={'email': 'librarian@college.edu'},
        )
        if created:
            librarian.set_password('librarian')
            librarian.save()
        librarian.groups.add(librarians)
        self.stdout.write(self.style.SUCCESS(
            "Created Librarians group + librarian user (librarian / librarian)."
        ))

        # --- 3) Sample data ---
        rowling, _ = Author.objects.get_or_create(name='J.K. Rowling')
        orwell, _ = Author.objects.get_or_create(name='George Orwell')

        sample_books = [
            ('Harry Potter',   '978-0001', rowling, 3, 3),
            ('1984',           '978-0002', orwell,  2, 2),
            ('Animal Farm',    '978-0003', orwell,  1, 0),   # 0 available -> can't be issued
        ]
        for title, isbn, author, total, available in sample_books:
            Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'copies_total': total,
                    'copies_available': available,
                },
            )

        Member.objects.get_or_create(
            email='alice@college.edu', defaults={'name': 'Alice'}
        )
        Member.objects.get_or_create(
            email='bob@college.edu', defaults={'name': 'Bob'}
        )

        self.stdout.write(self.style.SUCCESS(
            "Sample authors, books and members are ready. "
            "Start the server with: python manage.py runserver"
        ))
