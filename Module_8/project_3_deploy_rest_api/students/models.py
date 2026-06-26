# ============================================================================
#  models.py — the database design (reused unchanged from Module 4)
# ----------------------------------------------------------------------------
#  A "model" is a Python class that describes one database table. Django reads
#  these classes and builds the matching SQL tables for you (when you run
#  migrate). The whole point of Module 5 is that the API simply REUSES these
#  Module-4 models — we layer an API on top without rewriting the data design.
#
#  The relationship here is:  Department  1 ────< N  Student
#  (one department has many students; each student belongs to one department).
# ============================================================================
from django.db import models


class Department(models.Model):
    """A college department, e.g. 'Computer Science' or 'Physics'."""

    # The department's name. unique=True stops two departments sharing a name.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # Controls how the object is shown in the admin & shell (human-friendly).
        return self.name


class Student(models.Model):
    """One student record. Each student is linked to one Department."""

    # Roll number — a unique whole number identifying the student.
    roll = models.IntegerField(unique=True)

    # Basic personal details.
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Exam marks. PositiveIntegerField can't go below 0.
    marks = models.PositiveIntegerField(default=0)

    # Is the student currently enrolled/active? Defaults to True.
    is_active = models.BooleanField(default=True)

    # The date the student was admitted. auto_now_add=True means Django fills
    # it in automatically the moment the record is created, and it never
    # changes afterwards. (This is why the serializer marks it read-only.)
    admitted = models.DateField(auto_now_add=True)

    # The link to the Department table (the "N" side of 1—N).
    # on_delete=CASCADE: if a department is deleted, its students go too.
    # related_name='students' lets us write department.students.all() and is
    # what powers the "strength" count in DepartmentSerializer.
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='students',
    )

    class Meta:
        # Default sort order: highest marks first. This also makes the
        # "toppers" custom action naturally return the best students first.
        ordering = ['-marks']

    def __str__(self):
        return f"{self.roll} - {self.name}"
