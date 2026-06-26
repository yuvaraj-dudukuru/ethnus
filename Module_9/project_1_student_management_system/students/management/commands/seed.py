# ============================================================================
#  seed.py — one command to create the admin account + demo data.
#      python manage.py seed
#  Safe to run repeatedly (uses get_or_create).
# ============================================================================
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courses.models import Course
from students.models import Department, Student, Enrollment


class Command(BaseCommand):
    help = "Create the admin/admin superuser and sample students, courses, etc."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@college.edu", "admin")
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))

        cs, _ = Department.objects.get_or_create(name="Computer Science")
        phy, _ = Department.objects.get_or_create(name="Physics")
        math, _ = Department.objects.get_or_create(name="Mathematics")

        algo, _ = Course.objects.get_or_create(title="Algorithms", defaults={"credits": 4})
        db, _ = Course.objects.get_or_create(title="Databases", defaults={"credits": 3})
        Course.objects.get_or_create(title="Quantum Mechanics", defaults={"credits": 4})

        rows = [
            (101, "Asha Rao", "asha@college.edu", 92, cs),
            (102, "Bilal Khan", "bilal@college.edu", 88, cs),
            (103, "Chitra Devi", "chitra@college.edu", 95, phy),
            (104, "David Lee", "david@college.edu", 79, math),
            (105, "Esha Patel", "esha@college.edu", 84, math),
        ]
        for roll, name, email, marks, dept in rows:
            student, _ = Student.objects.get_or_create(
                roll=roll,
                defaults={"name": name, "email": email, "marks": marks, "department": dept},
            )
            if dept == cs:
                Enrollment.objects.get_or_create(student=student, course=algo)
                Enrollment.objects.get_or_create(student=student, course=db)

        self.stdout.write(self.style.SUCCESS(
            "Seeded departments, courses, students and enrollments. "
            "Run: python manage.py runserver"))
