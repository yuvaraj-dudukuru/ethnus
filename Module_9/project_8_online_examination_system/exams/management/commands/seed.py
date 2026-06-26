# ============================================================================
#  seed.py — admin/admin + a student + a sample auto-graded exam.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from exams.models import Exam, Question, Choice


class Command(BaseCommand):
    help = "Create admin/admin, student1/student and a sample exam."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@exam.test", "admin")
        if not User.objects.filter(username="student1").exists():
            User.objects.create_user("student1", password="student")
        self.stdout.write(self.style.SUCCESS("Users: admin/admin, student1/student."))

        if Exam.objects.filter(title="General Knowledge").exists():
            self.stdout.write("Exam already seeded — skipping.")
            return

        exam = Exam.objects.create(title="General Knowledge", duration=10, total_marks=3)
        data = [
            ("Capital of France?", [("Paris", True), ("Rome", False), ("Berlin", False)]),
            ("2 + 2 × 2 = ?", [("6", True), ("8", False), ("4", False)]),
            ("Largest planet?", [("Jupiter", True), ("Mars", False), ("Earth", False)]),
        ]
        for text, choices in data:
            q = Question.objects.create(exam=exam, text=text, marks=1)
            for ctext, correct in choices:
                Choice.objects.create(question=q, text=ctext, is_correct=correct)

        self.stdout.write(self.style.SUCCESS(
            "Seeded a 3-question exam. Run: python manage.py runserver"))
