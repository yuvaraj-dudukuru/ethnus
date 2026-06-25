# ============================================================================
#  serializers.py — translators between database objects and JSON
# ----------------------------------------------------------------------------
#  A serializer does two jobs:
#    1) SERIALIZE: turn a Student/Department object FROM the database INTO JSON
#       so it can be sent to the client.
#    2) DESERIALIZE + VALIDATE: take JSON sent BY the client, check it is
#       valid, and turn it into a database object to save.
#
#  Think of it as the "shape" of the data the API speaks.
# ============================================================================
from rest_framework import serializers
from .models import Department, Student


class DepartmentSerializer(serializers.ModelSerializer):
    """Defines what a Department looks like in the API."""

    # An EXTRA, calculated field that isn't a real column. It counts how many
    # students belong to this department by following the 'students' related
    # name from the model. read_only=True means clients can't set it.
    strength = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = Department
        # The exact fields (and their order) that appear in the JSON.
        fields = ['id', 'name', 'strength']


class StudentSerializer(serializers.ModelSerializer):
    """Defines what a Student looks like in the API."""

    # When READING a student, show the full nested department object
    # (id + name + strength) instead of just a number. read_only -> display only.
    department = DepartmentSerializer(read_only=True)

    # When WRITING a student, the client sends "department_id": 3 (just the id).
    # PrimaryKeyRelatedField validates that a Department with that id exists.
    # source='department' maps it back onto the model's department field.
    # write_only=True -> it is used for input but never shown in output.
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True,
    )

    class Meta:
        model = Student
        fields = ['id', 'roll', 'name', 'email', 'marks',
                  'is_active', 'admitted', 'department', 'department_id']
        # These fields can never be set by the client:
        #  - id is created by the database
        #  - admitted is filled automatically (auto_now_add) when created
        read_only_fields = ['id', 'admitted']

    def validate_email(self, v):
        """Custom rule: every student email must be an official college email.

        DRF calls any method named validate_<fieldname> automatically while
        checking incoming data. If we raise ValidationError, the API responds
        with a 400 error and this message instead of saving bad data.
        """
        if not v.endswith('@college.edu'):
            raise serializers.ValidationError("Official @college.edu email required.")
        return v
