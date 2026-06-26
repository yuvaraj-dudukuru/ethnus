# ============================================================================
#  serializers.py — JSON shape of a Course.
# ============================================================================
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "credits"]
