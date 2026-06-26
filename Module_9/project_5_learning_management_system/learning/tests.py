# ============================================================================
#  tests.py — LMS API checks.  Run with:  python manage.py test
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Course, Lesson


class LMSAPITests(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user("teacher", password="x")
        self.other = User.objects.create_user("other", password="x")
        self.student = User.objects.create_user("student", password="x")
        self.course = Course.objects.create(
            instructor=self.instructor, title="Python 101", description="Intro")
        self.l1 = Lesson.objects.create(course=self.course, title="Vars", order=1)
        self.l2 = Lesson.objects.create(course=self.course, title="Loops", order=2)

    def test_public_can_list_courses(self):
        self.assertEqual(self.client.get("/api/courses/").status_code, 200)

    def test_enroll_then_duplicate_rejected(self):
        self.client.force_authenticate(self.student)
        r = self.client.post(f"/api/courses/{self.course.id}/enroll/")
        self.assertEqual(r.status_code, 201)
        again = self.client.post(f"/api/courses/{self.course.id}/enroll/")
        self.assertEqual(again.status_code, 400)

    def test_progress_calculation(self):
        self.client.force_authenticate(self.student)
        self.client.post(f"/api/courses/{self.course.id}/enroll/")
        # Complete 1 of 2 lessons -> 50%.
        self.client.post(f"/api/lessons/{self.l1.id}/complete/")
        r = self.client.get(f"/api/courses/{self.course.id}/progress/")
        self.assertEqual(r.data["percent"], 50)

    def test_instructor_only_can_edit_course(self):
        # Non-owner is rejected.
        self.client.force_authenticate(self.other)
        r = self.client.patch(f"/api/courses/{self.course.id}/", {"title": "Hacked"})
        self.assertEqual(r.status_code, 403)
        # Owner succeeds.
        self.client.force_authenticate(self.instructor)
        ok = self.client.patch(f"/api/courses/{self.course.id}/", {"title": "Python 102"})
        self.assertEqual(ok.status_code, 200)

    def test_cannot_add_lesson_to_others_course(self):
        self.client.force_authenticate(self.other)
        r = self.client.post("/api/lessons/", {
            "course": self.course.id, "title": "Sneaky", "order": 3})
        self.assertEqual(r.status_code, 403)
