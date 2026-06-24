"""
create_users.py - One-off script that creates the demo accounts for the Job Portal.

Run it directly with:

    python create_users.py

It creates three ready-to-use accounts (all with simple, easy-to-remember
passwords because this is a learning/demo project):

    | Account     | Username    | Password   | Role               |
    |-------------|-------------|------------|--------------------|
    | Admin       | admin       | admin      | Superuser / Admin  |
    | Recruiter   | recruiter1  | recruiter  | Recruiter ('R')    |
    | Candidate   | candidate1  | candidate  | Candidate ('C')    |

The script is idempotent: each account is only created if it does not already
exist, so running it more than once is harmless.
"""

# Standard library module for reading/writing environment variables.
import os
# Django framework, which we boot manually because this is a standalone script.
import django

# Tell Django which settings module to use, then initialise the framework. This
# line is what lets us run the file directly with `python create_users.py`
# instead of having to pipe it through `python manage.py shell`.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

# Import the models only AFTER django.setup() has finished loading the apps.
from django.contrib.auth.models import User
from jobs.models import Profile

# --- 1. Admin / superuser account -----------------------------------------
# create_superuser() bypasses the password-strength validators, so the simple
# password "admin" is accepted. The admin can log in to /admin/.
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

# --- 2. Recruiter account --------------------------------------------------
# A normal user PLUS a linked Profile whose role is 'R' (Recruiter). Recruiters
# can post jobs and review applicants.
if not User.objects.filter(username='recruiter1').exists():
    r_user = User.objects.create_user(
        'recruiter1', 'recruiter1@example.com', 'recruiter',
        first_name='John', last_name='Doe'
    )
    Profile.objects.create(user=r_user, role='R', phone='1234567890')

# --- 3. Candidate account --------------------------------------------------
# A normal user PLUS a linked Profile whose role is 'C' (Candidate). Candidates
# can search for jobs and apply with a PDF resume.
if not User.objects.filter(username='candidate1').exists():
    c_user = User.objects.create_user(
        'candidate1', 'candidate1@example.com', 'candidate',
        first_name='Jane', last_name='Smith'
    )
    Profile.objects.create(user=c_user, role='C', phone='0987654321')

# Friendly confirmation so the person running the script knows it worked.
print("Demo accounts created successfully!")
print("  admin/admin  |  recruiter1/recruiter  |  candidate1/candidate")
