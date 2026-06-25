# ============================================================================
#  serializers.py — translators between database objects and JSON (and files!)
# ----------------------------------------------------------------------------
#  Highlights:
#    - RegisterSerializer: validates sign-up data and creates a User + role.
#    - ApplicationSerializer: includes a FILE field (the resume) plus a size
#      check, so files can be uploaded through the API.
# ============================================================================
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Job, Application

# Maximum resume size: 5 MB. (A Module 4.9-style validator.)
MAX_RESUME_MB = 5


class RegisterSerializer(serializers.Serializer):
    """Validates POST /api/register/  ->  {username, password, role}."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=4)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)   # 'R' or 'C'

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("That username is already taken.")
        return value

    def create(self, validated_data):
        # create_user hashes the password properly. The post_save signal makes
        # a Profile automatically; we then set the chosen role on it.
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.profile.role = validated_data['role']
        user.profile.save()
        return user


class JobSerializer(serializers.ModelSerializer):
    """The shape of a Job in the API."""
    recruiter_name = serializers.CharField(source='recruiter.username', read_only=True)
    application_count = serializers.IntegerField(source='applications.count', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'jtype',
                  'recruiter', 'recruiter_name', 'application_count', 'created']
        # The recruiter is stamped from the logged-in user, never sent by the client.
        read_only_fields = ['recruiter', 'created']


class ApplicationSerializer(serializers.ModelSerializer):
    """The shape of an Application — including the uploaded resume FILE."""
    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.username', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'candidate', 'candidate_name',
                  'resume', 'cover_note', 'status', 'applied_at']
        # job, candidate and status are set by the server (from the URL, the
        # logged-in user, and the recruiter's decision) — not by the applicant.
        read_only_fields = ['job', 'candidate', 'status', 'applied_at']

    def validate_resume(self, file):
        """Reject resumes larger than MAX_RESUME_MB. (File type is checked by
        the FileExtensionValidator on the model field.)"""
        if file.size > MAX_RESUME_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"Resume too large (max {MAX_RESUME_MB} MB)."
            )
        return file
