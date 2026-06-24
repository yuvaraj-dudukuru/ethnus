# Base class and field types for defining database tables.
from django.db import models
# Django's built-in User model — we link Profiles, Jobs and Applications to it.
from django.contrib.auth.models import User
# Ready-made validator that restricts an uploaded file to certain extensions.
from django.core.validators import FileExtensionValidator
# Exception we raise from our own validator when a rule is broken.
from django.core.exceptions import ValidationError


def validate_size(value):
    """Custom validator that rejects uploaded files larger than 2 MB.

    Django calls this automatically for the Application.resume field. ``value``
    is the uploaded file object; ``value.size`` is its size in bytes.
    """
    # Read the size (in bytes) of the uploaded file.
    filesize = value.size
    # 2 * 1024 * 1024 bytes == 2 MB. If the file is bigger, block the upload.
    if filesize > 2 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
    else:
        # Returning the value is optional for validators, but harmless.
        return value


class Profile(models.Model):
    """Extra information attached to each User, most importantly their ROLE.

    Django's User model has no concept of "recruiter" vs "candidate", so we add a
    Profile linked one-to-one to the User to store that role.
    """
    # The two kinds of user this portal supports. Stored as 'R'/'C' in the DB,
    # but shown as the friendly labels in forms and the admin.
    ROLE_CHOICES = [
        ('R', 'Recruiter'),
        ('C', 'Candidate')
    ]
    # OneToOneField == exactly one Profile per User (and vice-versa).
    # CASCADE: if the User is deleted, their Profile is deleted too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The role flag; defaults to Candidate ('C').
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C')
    # Optional phone number (blank=True means the form may leave it empty).
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # e.g. "jane (Candidate)" — get_role_display() turns 'C' into 'Candidate'.
        return f"{self.user.username} ({self.get_role_display()})"


class Job(models.Model):
    """A job posting created by a recruiter."""
    # The available employment types, stored as 2-letter codes.
    JTYPE_CHOICES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('CT', 'Contract'),
        ('IN', 'Internship')
    ]
    # The recruiter (a User) who posted this job. related_name='posted_jobs' lets
    # us write recruiter.posted_jobs.all(). CASCADE: delete user -> delete jobs.
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    # Core text fields describing the role.
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # Employment type, limited to the JTYPE_CHOICES above; defaults to Full Time.
    jtype = models.CharField(max_length=2, choices=JTYPE_CHOICES, default='FT', verbose_name="Job Type")
    # Salary is free text (e.g. "$80k–$100k"), so it is optional.
    salary = models.CharField(max_length=100, blank=True)
    # The full job description.
    description = models.TextField()
    # Timestamp set automatically when the job is first created.
    posted = models.DateTimeField(auto_now_add=True)
    # Recruiters can deactivate a posting without deleting it; only active jobs
    # appear on the public job list.
    active = models.BooleanField(default=True)

    def __str__(self):
        # Show the job title in the admin and templates.
        return self.title


class Application(models.Model):
    """A candidate's application to a specific Job (with resume + status)."""
    # The lifecycle of an application, stored as single-letter codes.
    STATUS = [('A', 'Applied'), ('S', 'Shortlisted'), ('R', 'Rejected')]
    # Which job this application is for. related_name='applications' lets us write
    # job.applications.all(). CASCADE: delete job -> delete its applications.
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    # Which candidate (User) applied.
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    # The uploaded resume. It is saved under media/resumes/YEAR/MONTH/ and must be
    # a PDF (FileExtensionValidator) no larger than 2 MB (our validate_size).
    resume = models.FileField(upload_to='resumes/%Y/%m/', validators=[FileExtensionValidator(['pdf']), validate_size])
    # An optional message from the candidate to the recruiter.
    cover_note = models.TextField(blank=True)
    # Current status of the application; starts as 'Applied'.
    status = models.CharField(max_length=1, choices=STATUS, default='A')
    # Timestamp set automatically when the application is submitted.
    applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Database-level rule: a candidate can apply to a given job only ONCE.
        # Trying to apply twice raises an IntegrityError (handled in the view).
        unique_together = ('job', 'candidate')

    def __str__(self):
        # e.g. "jane - Senior Developer"
        return f"{self.candidate.username} - {self.job.title}"
