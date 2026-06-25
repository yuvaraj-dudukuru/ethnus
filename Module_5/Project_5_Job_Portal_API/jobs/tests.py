# ============================================================================
#  tests.py — automated checks for the role-based rules
# ----------------------------------------------------------------------------
#  Run every test with:   python manage.py test
#
#  We test:
#    1) A candidate CANNOT post a job (403) — role permissions work.
#    2) Recruiter B CANNOT see Recruiter A's applicants — the role-shaped
#       queryset keeps each recruiter's data separate.
#    3) Uploading a resume via multipart works, and applying twice is rejected.
#
#  We point MEDIA_ROOT at a temporary folder so test uploads don't pollute the
#  real media/ directory.
# ============================================================================
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from jobs.models import Job, Application


def make_resume():
    """A tiny fake PDF file to upload in tests."""
    return SimpleUploadedFile('cv.pdf', b'%PDF-1.4 fake', content_type='application/pdf')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class JobPortalTest(APITestCase):

    def setUp(self):
        # Two recruiters and one candidate. The signal gives each a Profile;
        # we set the recruiters' role to 'R'.
        self.recruiterA = User.objects.create_user('reca', password='pass12345')
        self.recruiterA.profile.role = 'R'; self.recruiterA.profile.save()

        self.recruiterB = User.objects.create_user('recb', password='pass12345')
        self.recruiterB.profile.role = 'R'; self.recruiterB.profile.save()

        self.candidate = User.objects.create_user('cand', password='pass12345')
        # candidate keeps the default role 'C'

        # Recruiter A posts a job.
        self.jobA = Job.objects.create(
            title='Python Dev', description='Build APIs.',
            location='Remote', jtype='FT', recruiter=self.recruiterA,
        )

    def test_candidate_cannot_post_job(self):
        self.client.force_authenticate(self.candidate)
        r = self.client.post('/api/jobs/', {
            'title': 'Fake', 'description': 'x', 'location': 'y', 'jtype': 'FT',
        })
        # 403 = Forbidden — only recruiters may post jobs.
        self.assertEqual(r.status_code, 403)

    def test_candidate_can_apply_with_resume(self):
        self.client.force_authenticate(self.candidate)
        r = self.client.post(
            f'/api/jobs/{self.jobA.id}/apply/',
            {'resume': make_resume(), 'cover_note': 'Please hire me!'},
            format='multipart',
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

    def test_duplicate_application_rejected(self):
        self.client.force_authenticate(self.candidate)
        url = f'/api/jobs/{self.jobA.id}/apply/'
        self.client.post(url, {'resume': make_resume()}, format='multipart')
        # Second time -> caught IntegrityError -> clean 400.
        r2 = self.client.post(url, {'resume': make_resume()}, format='multipart')
        self.assertEqual(r2.status_code, 400)
        self.assertEqual(r2.data['detail'], 'Already applied.')

    def test_recruiter_cannot_see_other_recruiters_applicants(self):
        # The candidate applies to Recruiter A's job.
        Application.objects.create(
            job=self.jobA, candidate=self.candidate, resume=make_resume(),
        )
        # Recruiter B lists applications -> must see NONE (not A's applicant).
        self.client.force_authenticate(self.recruiterB)
        rb = self.client.get('/api/applications/')
        self.assertEqual(rb.data['count'], 0)

        # Recruiter A lists applications -> sees the one applicant.
        self.client.force_authenticate(self.recruiterA)
        ra = self.client.get('/api/applications/')
        self.assertEqual(ra.data['count'], 1)
