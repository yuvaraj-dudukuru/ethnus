"""
setup_data.py - One-off database seeding script for the Library system.

Run ``python setup_data.py`` to create:
  * an administrator account (username: admin, password: admin), and
  * two sample authors, two sample books and two sample members.

Every block uses get_or_create()/exists() checks, so running it repeatedly will
never create duplicate rows.
"""

# Standard library: read environment variables.
import os
# Django framework, so we can boot it from this standalone script.
import django
# date/timedelta are imported for convenience if you want to add sample issues.
from datetime import date, timedelta

# Tell Django which settings file to use, then start the framework.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

# Import the built-in User model and our library models AFTER django.setup().
from django.contrib.auth.models import User
from library.models import Author, Book, Member, Issue


def setup_data():
    """Create the admin user and a small catalogue of demo data."""
    # Create the admin account only if it does not already exist. create_superuser
    # skips the password validators, so the simple password "admin" is accepted.
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Created superuser: admin / admin")

    # get_or_create() returns (object, created_flag); the "_" ignores the flag.
    author1, _ = Author.objects.get_or_create(name='J.K. Rowling')
    author2, _ = Author.objects.get_or_create(name='George R.R. Martin')

    book1, _ = Book.objects.get_or_create(
        title='Harry Potter and the Sorcerer Stone',
        author=author1,
        isbn='9780590353427',
        copies_total=3,
        copies_available=3
    )

    book2, _ = Book.objects.get_or_create(
        title='A Game of Thrones',
        author=author2,
        isbn='9780553103540',
        copies_total=2,
        copies_available=2
    )

    member1, _ = Member.objects.get_or_create(name='Alice', email='alice@example.com')
    member2, _ = Member.objects.get_or_create(name='Bob', email='bob@example.com')

    print("Data populated successfully.")

if __name__ == '__main__':
    setup_data()
