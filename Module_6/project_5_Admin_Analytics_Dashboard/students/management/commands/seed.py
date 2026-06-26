# ============================================================================
#  seed.py — one-command setup helper:  python manage.py seed   (M6 analytics)
# ----------------------------------------------------------------------------
#  The Analytics Dashboard is only interesting if there is interesting data to
#  chart. So this seed is richer than the other projects': it creates
#
#     1) An admin account (username "admin", password "admin").
#     2) Four departments.
#     3) ~40 students with VARIED marks (some failing) spread across the LAST
#        SIX MONTHS, so the "admissions per month" line chart actually has a
#        shape and the pass/fail doughnut isn't all one colour.
#
#  TRICKY BIT: Student.admitted uses auto_now_add=True, which forces the date to
#  "today" on creation and refuses normal edits. To give students realistic
#  admission dates spread over months, we create them first, then use a
#  queryset .update() — which writes straight to the database and bypasses
#  auto_now_add. (Good viva point!)
#
#  Safe to run more than once: it skips creation if students already exist.
# ============================================================================
import random
from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Department, Student


def months_ago(n):
    """Return a date roughly n months before today (no external libraries)."""
    today = date.today()
    # Move back n months by arithmetic on year/month, keep day = 15 (safe).
    month_index = (today.year * 12 + (today.month - 1)) - n
    year = month_index // 12
    month = month_index % 12 + 1
    return date(year, month, 15)


class Command(BaseCommand):
    help = "Create admin + a rich, chart-friendly set of sample students."

    def handle(self, *args, **options):
        # --- 1) The admin account (admin / admin) ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@college.edu', 'admin')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))
        else:
            self.stdout.write("Admin user already exists — skipping.")

        # --- 2) Departments ---
        dept_names = ['Computer Science', 'Physics', 'Mathematics', 'Biology']
        depts = [Department.objects.get_or_create(name=n)[0] for n in dept_names]

        # --- 3) Students (only if we don't already have a full set) ---
        if Student.objects.count() >= 40:
            self.stdout.write("Students already seeded — skipping.")
            self.stdout.write(self.style.SUCCESS("Done. Run: python manage.py runserver"))
            return

        # A fixed random seed makes the sample data the SAME every time, so the
        # charts look identical on every student's machine.
        rng = random.Random(42)

        first_names = ['Asha', 'Bilal', 'Chitra', 'David', 'Esha', 'Farah', 'Gita',
                       'Hari', 'Iqra', 'John', 'Kiran', 'Leela', 'Manoj', 'Nina',
                       'Omar', 'Priya', 'Qadir', 'Riya', 'Sana', 'Tarun']
        last_names = ['Rao', 'Khan', 'Devi', 'Lee', 'Patel', 'Singh', 'Bose', 'Das']

        roll = 101
        for i in range(40):
            name = f"{rng.choice(first_names)} {rng.choice(last_names)}"
            # Marks 20–99 so some students fall below the pass mark (40).
            marks = rng.randint(20, 99)
            dept = rng.choice(depts)
            student = Student.objects.create(
                roll=roll,
                name=name,
                email=f"student{roll}@college.edu",
                marks=marks,
                is_active=rng.random() > 0.15,   # ~85% active
                department=dept,
            )
            # Spread admission dates across the last 6 months (bypass auto_now_add).
            admitted = months_ago(rng.randint(0, 5))
            Student.objects.filter(pk=student.pk).update(admitted=admitted)
            roll += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {Student.objects.count()} students across "
            f"{len(depts)} departments and 6 months. "
            "Start the server with: python manage.py runserver"
        ))
