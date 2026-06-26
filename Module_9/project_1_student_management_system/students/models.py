# ============================================================================
#  models.py — the database design for students & enrollments.
# ----------------------------------------------------------------------------
#  Relationships:
#     Department 1 ───< N Student          (a department has many students)
#     Student    1 ───1   User (optional)  (a login account for self-service)
#     Student    M ───< N Course           (via the Enrollment "through" table)
# ============================================================================
from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    """A college department, e.g. 'Computer Science'."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    """One student record, optionally linked to a login account."""

    # OneToOne link to a Django login account (lets a student log in to see
    # their own profile). Optional so admins can add a student before an
    # account exists. SET_NULL keeps the student row if the user is deleted.
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="student_profile",
    )
    roll = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    marks = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    admitted = models.DateField(auto_now_add=True)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="students",
    )
    # The M2M to Course is expressed THROUGH Enrollment so we can store a grade.
    courses = models.ManyToManyField(
        "courses.Course", through="students.Enrollment", related_name="students",
    )

    class Meta:
        ordering = ["-marks"]  # toppers first

    def __str__(self):
        return f"{self.roll} - {self.name}"


class Enrollment(models.Model):
    """Join row: which student takes which course, plus their grade."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments",
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="enrollments",
    )
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        # A student can't be enrolled in the same course twice.
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.name} -> {self.course.title} ({self.grade or '-'})"
