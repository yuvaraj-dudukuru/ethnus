# ============================================================================
#  models.py — jobs posted by recruiters and applications by candidates.
# ----------------------------------------------------------------------------
#  Recruiter(User) 1 ─< N Job 1 ─< N Application >─ 1 Candidate(User)
#  unique_together(job, candidate) stops a candidate applying twice.
# ============================================================================
from django.contrib.auth.models import User
from django.db import models


class Job(models.Model):
    TYPES = [
        ("FT", "Full-time"), ("PT", "Part-time"),
        ("CT", "Contract"), ("IN", "Internship"),
    ]
    recruiter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="jobs_posted")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=120)
    type = models.CharField(max_length=2, choices=TYPES, default="FT")
    salary = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted"]

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Application(models.Model):
    STATUS = [
        ("APPLIED", "Applied"), ("REVIEW", "Under review"),
        ("ACCEPTED", "Accepted"), ("REJECTED", "Rejected"),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/")
    cover_note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="APPLIED")
    applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")
        ordering = ["-applied"]

    def __str__(self):
        return f"{self.candidate.username} → {self.job.title}"
