# ============================================================================
#  models.py — exams, questions, choices, attempts and answers.
# ----------------------------------------------------------------------------
#  Exam 1 ─< N Question 1 ─< N Choice
#  Student(User) 1 ─< N Attempt (one per exam) 1 ─< N Answer
#  unique_together(student, exam) enforces the ONE-ATTEMPT rule at DB level.
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(default=30, help_text="minutes")
    total_marks = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def max_marks(self):
        """The real total — sum of every question's marks."""
        return sum(q.marks for q in self.questions.all())

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    marks = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text


class Attempt(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempts")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)
    submitted = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "exam")  # one attempt per student
        ordering = ["-started"]

    @property
    def deadline(self):
        return self.started + timedelta(minutes=self.exam.duration)

    def __str__(self):
        return f"{self.student.username} · {self.exam.title}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("attempt", "question")
