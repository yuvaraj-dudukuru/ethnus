# ============================================================================
#  tests.py — Job Portal API checks.  Run with:  python manage.py test
# ============================================================================
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import Job, Application


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())  # keep test uploads out of the repo
class JobPortalAPITests(APITestCase):
    def setUp(self):
        # The post_save signal makes a Profile (default candidate) for each user.
        self.recruiter = User.objects.create_user("rec1", password="x")
        self.recruiter.profile.role = "recruiter"
        self.recruiter.profile.save()
        self.recruiter2 = User.objects.create_user("rec2", password="x")
        self.recruiter2.profile.role = "recruiter"
        self.recruiter2.profile.save()
        self.candidate = User.objects.create_user("cand1", password="x")  # candidate

        self.job = Job.objects.create(
            recruiter=self.recruiter, title="Backend Dev", company="Acme",
            location="Remote", type="FT", description="Django role.")

    def _resume(self):
        return SimpleUploadedFile("cv.pdf", b"%PDF-1.4 fake", content_type="application/pdf")

    def test_public_can_list_jobs(self):
        self.assertEqual(self.client.get("/api/jobs/").status_code, 200)

    def test_candidate_cannot_post_job(self):
        self.client.force_authenticate(self.candidate)
        r = self.client.post("/api/jobs/", {
            "title": "X", "company": "Y", "location": "Z", "description": "d"})
        self.assertEqual(r.status_code, 403)

    def test_recruiter_can_post_job(self):
        self.client.force_authenticate(self.recruiter)
        r = self.client.post("/api/jobs/", {
            "title": "Frontend", "company": "Acme", "location": "NYC",
            "type": "FT", "description": "React role."})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["recruiter"], "rec1")

    def test_apply_then_duplicate_rejected(self):
        self.client.force_authenticate(self.candidate)
        r = self.client.post(f"/api/jobs/{self.job.id}/apply/",
                             {"resume": self._resume(), "cover_note": "Hi"},
                             format="multipart")
        self.assertEqual(r.status_code, 201)
        again = self.client.post(f"/api/jobs/{self.job.id}/apply/",
                                {"resume": self._resume()}, format="multipart")
        self.assertEqual(again.status_code, 400)

    def test_recruiter_sees_only_own_applicants(self):
        Application.objects.create(
            job=self.job, candidate=self.candidate, resume=self._resume())
        # Owner recruiter sees the applicant.
        self.client.force_authenticate(self.recruiter)
        self.assertEqual(len(self.client.get("/api/applications/").data["results"]), 1)
        # A different recruiter sees none of it.
        self.client.force_authenticate(self.recruiter2)
        self.assertEqual(self.client.get("/api/applications/").data["count"], 0)

    def test_non_owner_recruiter_cannot_view_applicants_action(self):
        self.client.force_authenticate(self.recruiter2)
        r = self.client.get(f"/api/jobs/{self.job.id}/applicants/")
        self.assertEqual(r.status_code, 403)
