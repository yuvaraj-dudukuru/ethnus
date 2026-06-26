# ============================================================================
#  tests.py — Online Exam API checks.  Run with:  python manage.py test
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Exam, Question, Choice, Attempt


class ExamAPITests(APITestCase):
    def setUp(self):
        self.s1 = User.objects.create_user("stud1", password="x")
        self.s2 = User.objects.create_user("stud2", password="x")
        self.exam = Exam.objects.create(title="Math Quiz", duration=30, total_marks=2)
        self.q1 = Question.objects.create(exam=self.exam, text="2+2?", marks=1)
        self.c1ok = Choice.objects.create(question=self.q1, text="4", is_correct=True)
        self.c1no = Choice.objects.create(question=self.q1, text="5")
        self.q2 = Question.objects.create(exam=self.exam, text="3*3?", marks=1)
        self.c2ok = Choice.objects.create(question=self.q2, text="9", is_correct=True)
        self.c2no = Choice.objects.create(question=self.q2, text="6")

    def _correct_answers(self):
        return {"answers": [
            {"question": self.q1.id, "choice": self.c1ok.id},
            {"question": self.q2.id, "choice": self.c2ok.id}]}

    def test_public_can_list_exams(self):
        self.assertEqual(self.client.get("/api/exams/").status_code, 200)

    def test_take_serializer_hides_answer_key(self):
        r = self.client.get(f"/api/exams/{self.exam.id}/")
        choice = r.data["questions"][0]["choices"][0]
        self.assertNotIn("is_correct", choice)

    def test_single_attempt_rule(self):
        self.client.force_authenticate(self.s1)
        self.assertEqual(
            self.client.post(f"/api/exams/{self.exam.id}/start/").status_code, 201)
        self.assertEqual(
            self.client.post(f"/api/exams/{self.exam.id}/start/").status_code, 400)

    def test_autograding_all_correct(self):
        self.client.force_authenticate(self.s1)
        self.client.post(f"/api/exams/{self.exam.id}/start/")
        r = self.client.post(f"/api/exams/{self.exam.id}/submit/",
                             self._correct_answers(), format="json")
        self.assertEqual(r.data["score"], 2)
        self.assertEqual(r.data["total"], 2)

    def test_autograding_wrong_scores_zero(self):
        self.client.force_authenticate(self.s2)
        self.client.post(f"/api/exams/{self.exam.id}/start/")
        r = self.client.post(f"/api/exams/{self.exam.id}/submit/",
                             {"answers": [{"question": self.q1.id, "choice": self.c1no.id}]},
                             format="json")
        self.assertEqual(r.data["score"], 0)

    def test_timer_enforcement_discards_late_answers(self):
        self.client.force_authenticate(self.s1)
        self.client.post(f"/api/exams/{self.exam.id}/start/")
        # Rewind the clock so the deadline is already in the past.
        attempt = Attempt.objects.get(student=self.s1, exam=self.exam)
        attempt.started = timezone.now() - timedelta(hours=2)
        attempt.save()
        r = self.client.post(f"/api/exams/{self.exam.id}/submit/",
                             self._correct_answers(), format="json")
        self.assertTrue(r.data["expired"])
        self.assertEqual(r.data["score"], 0)   # late answers don't count

    def test_cannot_submit_twice(self):
        self.client.force_authenticate(self.s1)
        self.client.post(f"/api/exams/{self.exam.id}/start/")
        self.client.post(f"/api/exams/{self.exam.id}/submit/",
                        self._correct_answers(), format="json")
        again = self.client.post(f"/api/exams/{self.exam.id}/submit/",
                                self._correct_answers(), format="json")
        self.assertEqual(again.status_code, 400)
