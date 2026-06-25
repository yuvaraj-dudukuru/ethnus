# ============================================================================
#  seed.py — one-command setup helper:  python manage.py seed
# ----------------------------------------------------------------------------
#  Sets up everything you need to start playing with the API:
#
#     1) An admin account   -> username "admin",     password "admin"
#     2) A recruiter        -> username "recruiter", password "recruiter"  (role R)
#     3) A candidate        -> username "candidate", password "candidate"  (role C)
#     4) A couple of sample job openings posted by the recruiter.
#
#  (The post_save signal gives every new user a Profile automatically; here we
#  just set the right role on it.)
#
#  Safe to run more than once (uses get_or_create). Run it right after migrate.
# ============================================================================
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job


class Command(BaseCommand):
    help = "Create admin + recruiter + candidate accounts and sample jobs."

    def _make_user(self, username, password, role, is_admin=False):
        """Create a user (if missing), set the password and the profile role."""
        user, created = User.objects.get_or_create(username=username)
        if created:
            if is_admin:
                user.is_staff = True
                user.is_superuser = True
            user.set_password(password)
            user.save()
        # The signal already created a Profile; set its role.
        user.profile.role = role
        user.profile.save()
        return user, created

    def handle(self, *args, **options):
        # 1) Admin (superuser).
        self._make_user('admin', 'admin', role='R', is_admin=True)
        self.stdout.write(self.style.SUCCESS("Admin ready (admin / admin)."))

        # 2) Recruiter and 3) candidate.
        recruiter, _ = self._make_user('recruiter', 'recruiter', role='R')
        self._make_user('candidate', 'candidate', role='C')
        self.stdout.write(self.style.SUCCESS(
            "Recruiter (recruiter / recruiter) and candidate (candidate / candidate) ready."
        ))

        # 4) Sample jobs, posted by the recruiter.
        sample_jobs = [
            ('Python Developer', 'Build REST APIs with Django.', 'Bengaluru', 'FT'),
            ('Frontend Intern',  'Work on the React UI.',        'Remote',    'IN'),
        ]
        for title, desc, location, jtype in sample_jobs:
            Job.objects.get_or_create(
                title=title, recruiter=recruiter,
                defaults={'description': desc, 'location': location, 'jtype': jtype},
            )

        self.stdout.write(self.style.SUCCESS(
            "Sample jobs are ready. Start the server with: python manage.py runserver"
        ))
