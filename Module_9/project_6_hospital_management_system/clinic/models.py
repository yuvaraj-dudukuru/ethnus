# ============================================================================
#  models.py — doctors, patients, appointments and medical records.
# ----------------------------------------------------------------------------
#  Medical data is SENSITIVE, so every user has a Profile.role that drives
#  strict, role-based access in the API layer.
#     Department 1 ─< N Doctor
#     Patient    1 ─< N Appointment >─ 1 Doctor
#     Patient    1 ─< N MedicalRecord
# ============================================================================
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLES = [
        ("patient", "Patient"), ("doctor", "Doctor"),
        ("receptionist", "Receptionist"), ("admin", "Admin"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="clinic_profile")
    role = models.CharField(max_length=12, choices=ROLES, default="patient")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def role_of(user):
    if not getattr(user, "is_authenticated", False):
        return None
    if user.is_superuser:
        return "admin"
    p = getattr(user, "clinic_profile", None)
    return p.role if p else None


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="doctor_profile")
    name = models.CharField(max_length=120)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="doctors")
    specialization = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Dr. {self.name}"


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile")
    name = models.CharField(max_length=120)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS = [("BOOKED", "Booked"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")]
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments")
    datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS, default="BOOKED")
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return f"{self.patient.name} with Dr. {self.doctor.name} @ {self.datetime}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name="records")
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Record for {self.patient.name} ({self.date})"
