# ============================================================================
#  tests.py — automated checks for the Student Management API.
#  Run with:  python manage.py test
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from courses.models import Course
from .models import Department, Student


class StudentAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@college.edu", "admin")
        self.teacher = User.objects.create_user("teacher", password="teacher")
        self.dept = Department.objects.create(name="Computer Science")
        self.course = Course.objects.create(title="Algorithms", credits=4)
        self.top = Student.objects.create(
            roll=1, name="Asha", email="asha@college.edu", marks=90, department=self.dept)
        self.low = Student.objects.create(
            roll=2, name="Bilal", email="bilal@college.edu", marks=70, department=self.dept)

    def test_public_can_list_students(self):
        self.assertEqual(self.client.get("/api/students/").status_code, 200)

    def test_anonymous_cannot_create(self):
        r = self.client.post("/api/students/", {
            "roll": 9, "name": "X", "email": "x@college.edu",
            "department_id": self.dept.id})
        self.assertEqual(r.status_code, 401)

    def test_department_strength_is_counted(self):
        r = self.client.get(f"/api/departments/{self.dept.id}/")
        self.assertEqual(r.data["strength"], 2)

    def test_toppers_orders_by_marks(self):
        r = self.client.get("/api/students/toppers/")
        self.assertEqual(r.data[0]["roll"], 1)  # 90 marks comes first

    def test_email_must_be_college_domain(self):
        self.client.force_authenticate(self.teacher)
        r = self.client.post("/api/students/", {
            "roll": 9, "name": "X", "email": "x@gmail.com",
            "department_id": self.dept.id})
        self.assertEqual(r.status_code, 400)

    def test_enroll_then_duplicate_is_rejected(self):
        self.client.force_authenticate(self.teacher)
        r = self.client.post(f"/api/students/{self.top.id}/enroll/",
                             {"course_id": self.course.id})
        self.assertEqual(r.status_code, 201)
        again = self.client.post(f"/api/students/{self.top.id}/enroll/",
                                {"course_id": self.course.id})
        self.assertEqual(again.status_code, 400)

    def test_only_admin_can_delete(self):
        self.client.force_authenticate(self.teacher)
        self.assertEqual(
            self.client.delete(f"/api/students/{self.top.id}/").status_code, 403)
        self.client.force_authenticate(self.admin)
        self.assertEqual(
            self.client.delete(f"/api/students/{self.top.id}/").status_code, 204)
