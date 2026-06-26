# ============================================================================
#  serializers.py — JSON shapes for the LMS.
# ============================================================================
from rest_framework import serializers
from .models import Course, Lesson, Enrollment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "content", "video_url", "order"]


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.CharField(source="instructor.username", read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "instructor", "lesson_count", "created"]
        read_only_fields = ["id", "instructor", "created"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course", "course_title", "enrolled"]
        read_only_fields = ["id", "enrolled"]
