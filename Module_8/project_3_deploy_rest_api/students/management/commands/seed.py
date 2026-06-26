# ============================================================================
#  seed.py — a one-command setup helper:  python manage.py seed
# ----------------------------------------------------------------------------
#  Creating the admin user normally needs the INTERACTIVE "createsuperuser"
#  command (it asks you questions). To keep things simple for students, this
#  custom command does everything automatically:
#
#     1) Creates an admin account with username "admin" and password "admin".
#     2) Creates a few sample Departments.
#     3) Creates a few sample Students so the API has data to show.
#
#  It is SAFE to run more than once: it uses get_or_create, so it won't make
#  duplicates. Run it right after "migrate".
# ============================================================================
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Department, Student


class Command(BaseCommand):
    help = "Create the admin/admin superuser and some sample data."

    def handle(self, *args, **options):
        # --- 1) The admin account (username: admin, password: admin) ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@college.edu', 'admin')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))
        else:
            self.stdout.write("Admin user already exists — skipping.")

        # --- 2) Sample departments ---
        cs, _ = Department.objects.get_or_create(name='Computer Science')
        phy, _ = Department.objects.get_or_create(name='Physics')
        math, _ = Department.objects.get_or_create(name='Mathematics')

        # --- 3) Sample students (roll, name, email, marks, department) ---
        sample_students = [
            (101, 'Asha Rao',    'asha@college.edu',    92, cs),
            (102, 'Bilal Khan',  'bilal@college.edu',   88, cs),
            (103, 'Chitra Devi', 'chitra@college.edu',  95, phy),
            (104, 'David Lee',   'david@college.edu',   79, math),
            (105, 'Esha Patel',  'esha@college.edu',    84, math),
        ]
        for roll, name, email, marks, dept in sample_students:
            Student.objects.get_or_create(
                roll=roll,
                defaults={
                    'name': name,
                    'email': email,
                    'marks': marks,
                    'department': dept,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            "Sample departments and students are ready. "
            "Start the server with: python manage.py runserver"
        ))
