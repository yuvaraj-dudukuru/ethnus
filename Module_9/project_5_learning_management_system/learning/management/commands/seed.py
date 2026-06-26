# ============================================================================
#  seed.py — admin/admin + an instructor + a student + a sample course.
#      python manage.py seed
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from learning.models import Course, Lesson


class Command(BaseCommand):
    help = "Create admin/admin, instructor1/instructor, student1/student + a course."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@lms.test", "admin")
        instructor, _ = User.objects.get_or_create(username="instructor1")
        instructor.set_password("instructor")
        instructor.save()
        student, _ = User.objects.get_or_create(username="student1")
        student.set_password("student")
        student.save()
        self.stdout.write(self.style.SUCCESS(
            "Users: admin/admin, instructor1/instructor, student1/student."))

        course, _ = Course.objects.get_or_create(
            title="Django for Beginners",
            defaults={"instructor": instructor,
                      "description": "Build web apps with Django."})
        lessons = [
            ("Setup & Hello World", 1, "https://example.com/v1"),
            ("Models & Migrations", 2, "https://example.com/v2"),
            ("Views & Templates", 3, "https://example.com/v3"),
            ("The REST API", 4, "https://example.com/v4"),
        ]
        for title, order, url in lessons:
            Lesson.objects.get_or_create(
                course=course, title=title,
                defaults={"order": order, "video_url": url,
                          "content": f"Lesson {order}: {title}."})

        self.stdout.write(self.style.SUCCESS(
            "Seeded a course with lessons. Run: python manage.py runserver"))
