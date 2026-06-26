# ============================================================================
#  serializers.py — translators between Student/Department objects and JSON.
# ============================================================================
from rest_framework import serializers
from courses.serializers import CourseSerializer
from .models import Department, Student, Enrollment


class DepartmentSerializer(serializers.ModelSerializer):
    # Calculated field: how many students belong to this department.
    strength = serializers.IntegerField(source="students.count", read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "strength"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course", "grade"]


class StudentSerializer(serializers.ModelSerializer):
    # READ: full nested department. WRITE: send "department_id": 3.
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True,
    )
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["id", "roll", "name", "email", "marks", "is_active",
                  "admitted", "department", "department_id", "enrollments"]
        read_only_fields = ["id", "admitted"]

    def validate_email(self, v):
        """Every student email must be an official @college.edu address."""
        if not v.endswith("@college.edu"):
            raise serializers.ValidationError("Official @college.edu email required.")
        return v
