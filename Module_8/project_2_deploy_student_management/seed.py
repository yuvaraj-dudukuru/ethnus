"""
seed.py - One-off database seeding script for CampusHub.

Running ``python seed.py`` populates the database with:
  * a superuser/admin account (username: admin, password: admin), and
  * three sample departments plus three sample students.

It is safe to run multiple times: every block first checks whether the data
already exists, so duplicates are never created.
"""

# Standard library module used to read/write environment variables.
import os
# Django framework entry point so we can bootstrap it from a standalone script.
import django

# Point Django at the project's settings module before we initialise the framework.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campushub.settings")
# Boot Django so the ORM (database models) become usable below.
django.setup()

# Built-in user model that powers authentication and the admin site.
from django.contrib.auth.models import User
# Our own application models for departments and students.
from students.models import Department, Student

# --- Create the administrator account -------------------------------------
# Only create the admin if it does not already exist (keeps re-runs idempotent).
if not User.objects.filter(username='admin').exists():
    # create_superuser() bypasses the password-strength validators, so the simple
    # password "admin" is allowed here for easy classroom/demo logins.
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser created: admin / admin")

# Seed data
d1, _ = Department.objects.get_or_create(name="Computer Science")
d2, _ = Department.objects.get_or_create(name="Information Technology")
d3, _ = Department.objects.get_or_create(name="Electronics")

if not Student.objects.exists():
    Student.objects.create(roll=101, name="Alice Smith", email="alice@college.edu", marks=85, department=d1)
    Student.objects.create(roll=102, name="Bob Jones", email="bob@college.edu", marks=78, department=d2)
    Student.objects.create(roll=103, name="Charlie Brown", email="charlie@college.edu", marks=92, department=d1)
    print("Seed data created.")
else:
    print("Data already exists.")
