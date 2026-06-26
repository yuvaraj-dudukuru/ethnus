# ============================================================================
#  seed.py — admin + a recruiter + a candidate + sample jobs.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from jobs.models import Job


class Command(BaseCommand):
    help = "Create admin/admin, recruiter1/recruiter, candidate1/candidate + jobs."

    def _user(self, username, password, role, staff=False):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.is_staff = staff
            user.is_superuser = staff
            user.save()
        # The post_save signal created the profile; set the role.
        user.profile.role = role
        user.profile.save()
        return user

    def handle(self, *args, **options):
        self._user("admin", "admin", "recruiter", staff=True)
        recruiter = self._user("recruiter1", "recruiter", "recruiter")
        self._user("candidate1", "candidate", "candidate")
        self.stdout.write(self.style.SUCCESS(
            "Users: admin/admin, recruiter1/recruiter, candidate1/candidate."))

        jobs = [
            ("Senior Django Developer", "Acme Corp", "Remote", "FT", 120000),
            ("Frontend Engineer", "Pixel Labs", "Bengaluru", "FT", 90000),
            ("Data Science Intern", "Insight AI", "Hyderabad", "IN", 30000),
        ]
        for title, company, location, type_, salary in jobs:
            Job.objects.get_or_create(
                title=title, company=company,
                defaults={"recruiter": recruiter, "location": location,
                          "type": type_, "salary": salary,
                          "description": f"We are hiring a {title}."})

        self.stdout.write(self.style.SUCCESS(
            "Seeded sample jobs. Run: python manage.py runserver"))
