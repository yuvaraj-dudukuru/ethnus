# ============================================================================
#  models.py — the database design (reused from Module-4 Project 5)
# ----------------------------------------------------------------------------
#  Tables and how they connect:
#
#      User 1 ──(one-to-one)── Profile          (Profile stores the user's ROLE)
#      User(recruiter) 1 ───< N Job
#      Job 1 ───< N Application >─── N 1 User(candidate)
#
#  THE ROLE IDEA:  every user is either a RECRUITER (posts jobs, reviews
#  applicants) or a CANDIDATE (applies to jobs). We store that role on a
#  Profile linked one-to-one to Django's built-in User. Permission classes
#  then read profile.role to decide who may do what.
# ============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    """Extra info attached to each User — most importantly, their role."""

    ROLE_CHOICES = [
        ('R', 'Recruiter'),
        ('C', 'Candidate'),
    ]

    # OneToOne = exactly one profile per user. related_name='profile' lets us
    # write request.user.profile.role (used everywhere in permissions).
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Job(models.Model):
    """A job opening, posted by a recruiter."""

    JTYPE_CHOICES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=120)
    jtype = models.CharField(max_length=2, choices=JTYPE_CHOICES, default='FT')

    # Who posted it. Only this recruiter may edit/delete it.
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Application(models.Model):
    """A candidate's application to a job, including their uploaded resume."""

    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Selected'),
        ('R', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    # THE UPLOADED FILE. Files land in MEDIA_ROOT/resumes/. The validator
    # rejects anything that isn't a PDF or Word document (a Module 4.9 idea).
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
    )

    cover_note = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        # A candidate can apply to a given job only ONCE. Trying again raises a
        # database IntegrityError, which the apply view turns into a clean 400.
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title}"
