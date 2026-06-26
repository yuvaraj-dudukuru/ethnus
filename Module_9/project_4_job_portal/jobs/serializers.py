# ============================================================================
#  serializers.py — JSON shapes for jobs and applications.
# ============================================================================
from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.CharField(source="recruiter.username", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    application_count = serializers.IntegerField(
        source="applications.count", read_only=True)

    class Meta:
        model = Job
        fields = ["id", "title", "company", "location", "type", "type_display",
                  "salary", "description", "posted", "recruiter", "application_count"]
        read_only_fields = ["id", "posted", "recruiter"]


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = serializers.CharField(source="candidate.username", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Application
        fields = ["id", "job", "job_title", "candidate", "resume",
                  "cover_note", "status", "applied"]
        read_only_fields = ["id", "job", "candidate", "applied"]
