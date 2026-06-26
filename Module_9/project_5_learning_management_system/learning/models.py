# ============================================================================
#  models.py — courses, lessons, enrollments and per-lesson progress.
# ----------------------------------------------------------------------------
#  Instructor(User) 1 ─< N Course 1 ─< N Lesson
#  Student(User)    M ─< N Course   (via Enrollment)
#  Student(User)    1 ─< N Progress >─ 1 Lesson
# ============================================================================
from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses_taught")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    @property
    def lesson_count(self):
        return self.lessons.count()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.title} · {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrolled"]

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"


class Progress(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress")
    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student.username} ✓ {self.lesson.title}"
