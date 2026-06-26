# ============================================================================
#  seed.py — admin + a doctor + a patient + departments and doctors.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from clinic.models import Department, Doctor, Patient


class Command(BaseCommand):
    help = "Create admin/admin, doctor1/doctor, patient1/patient + sample data."

    def _user(self, username, password, role, staff=False):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.is_staff = staff
            user.is_superuser = staff
            user.save()
        user.clinic_profile.role = role
        user.clinic_profile.save()
        return user

    def handle(self, *args, **options):
        self._user("admin", "admin", "admin", staff=True)
        doc_user = self._user("doctor1", "doctor", "doctor")
        pat_user = self._user("patient1", "patient", "patient")
        self._user("reception1", "reception", "receptionist")
        self.stdout.write(self.style.SUCCESS(
            "Users: admin/admin, doctor1/doctor, patient1/patient, reception1/reception."))

        cardio, _ = Department.objects.get_or_create(name="Cardiology")
        neuro, _ = Department.objects.get_or_create(name="Neurology")
        ortho, _ = Department.objects.get_or_create(name="Orthopedics")

        Doctor.objects.get_or_create(
            name="Gregory House", defaults={
                "user": doc_user, "department": cardio,
                "specialization": "Cardiology"})
        Doctor.objects.get_or_create(
            name="Meredith Grey", defaults={
                "department": neuro, "specialization": "Neurology"})
        Doctor.objects.get_or_create(
            name="John Carter", defaults={
                "department": ortho, "specialization": "Orthopedic surgery"})

        Patient.objects.get_or_create(
            user=pat_user, defaults={"name": "Demo Patient", "phone": "555-0100"})

        self.stdout.write(self.style.SUCCESS(
            "Seeded departments, doctors and a patient. Run: python manage.py runserver"))
