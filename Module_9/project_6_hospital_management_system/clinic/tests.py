# ============================================================================
#  tests.py — Hospital API checks (focus: RBAC + no double-booking).
#  Run with:  python manage.py test
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Department, Doctor, Patient, MedicalRecord

SLOT = "2030-01-01T10:00:00Z"


class HospitalAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@h.test", "admin")
        self.doc_user = User.objects.create_user("dr_house", password="x")
        self.doc_user.clinic_profile.role = "doctor"
        self.doc_user.clinic_profile.save()
        self.dept = Department.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            user=self.doc_user, name="House", department=self.dept,
            specialization="Cardiology")

        self.p1 = User.objects.create_user("pat1", password="x")  # patient role
        self.p2 = User.objects.create_user("pat2", password="x")
        self.patient1 = Patient.objects.create(user=self.p1, name="Pat One")
        self.patient2 = Patient.objects.create(user=self.p2, name="Pat Two")

    def test_public_can_list_doctors(self):
        self.assertEqual(self.client.get("/api/doctors/").status_code, 200)

    def test_no_double_booking(self):
        self.client.force_authenticate(self.p1)
        r = self.client.post(f"/api/doctors/{self.doctor.id}/book/", {"datetime": SLOT})
        self.assertEqual(r.status_code, 201)
        self.client.force_authenticate(self.p2)
        clash = self.client.post(f"/api/doctors/{self.doctor.id}/book/", {"datetime": SLOT})
        self.assertEqual(clash.status_code, 400)

    def test_appointment_lifecycle(self):
        self.client.force_authenticate(self.p1)
        appt = self.client.post(
            f"/api/doctors/{self.doctor.id}/book/", {"datetime": SLOT}).data
        self.assertEqual(appt["status"], "BOOKED")
        cancelled = self.client.post(f"/api/appointments/{appt['id']}/cancel/")
        self.assertEqual(cancelled.data["status"], "CANCELLED")

    def test_records_are_private_to_the_patient(self):
        MedicalRecord.objects.create(
            patient=self.patient1, doctor=self.doctor, diagnosis="Flu")
        self.client.force_authenticate(self.p2)            # a different patient
        self.assertEqual(self.client.get("/api/records/").data["count"], 0)
        self.client.force_authenticate(self.p1)            # the owner
        self.assertEqual(self.client.get("/api/records/").data["count"], 1)

    def test_patient_cannot_create_record(self):
        self.client.force_authenticate(self.p1)
        r = self.client.post("/api/records/", {
            "patient": self.patient1.id, "diagnosis": "self-diagnosis"})
        self.assertEqual(r.status_code, 403)

    def test_doctor_can_create_record(self):
        self.client.force_authenticate(self.doc_user)
        r = self.client.post("/api/records/", {
            "patient": self.patient1.id, "doctor": self.doctor.id,
            "diagnosis": "Hypertension", "prescription": "Rest"})
        self.assertEqual(r.status_code, 201)
