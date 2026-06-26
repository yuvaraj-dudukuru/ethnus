# ============================================================================
#  serializers.py — JSON shapes for the hospital.
# ============================================================================
from rest_framework import serializers
from .models import Department, Doctor, Patient, Appointment, MedicalRecord


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class DoctorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "department", "department_id"]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "dob", "phone"]


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "patient", "patient_name", "doctor", "doctor_name",
                  "datetime", "status", "reason"]
        read_only_fields = ["id", "patient", "status"]


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ["id", "patient", "patient_name", "doctor", "doctor_name",
                  "diagnosis", "prescription", "date"]
        read_only_fields = ["id", "date"]
