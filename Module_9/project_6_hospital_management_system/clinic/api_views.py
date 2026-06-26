# ============================================================================
#  api_views.py — doctor search, booking (no double-booking) and records (RBAC).
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .filters import DoctorFilter
from .models import Department, Doctor, Patient, Appointment, MedicalRecord, role_of
from .permissions import IsAdminRole, IsDoctorOrAdmin, IsMedicalStaffOrReadOnly
from .serializers import (
    DepartmentSerializer, DoctorSerializer, PatientSerializer,
    AppointmentSerializer, MedicalRecordSerializer,
)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DoctorViewSet(viewsets.ModelViewSet):
    """Public doctor directory. Only admins manage doctors. Patients book slots."""
    queryset = Doctor.objects.select_related("department")
    serializer_class = DoctorSerializer
    filterset_class = DoctorFilter
    search_fields = ["name", "specialization", "department__name"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminRole()]
        return [AllowAny()]

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        """POST /api/doctors/<id>/book/  body: {"datetime": "...", "reason": "..."}.
        Refuses to double-book the same doctor for the same time slot."""
        doctor = self.get_object()
        when = parse_datetime(request.data.get("datetime", ""))
        if when is None:
            return Response({"detail": "Provide a valid ISO datetime."}, status=400)
        if timezone.is_naive(when):
            when = timezone.make_aware(when)
        # Double-booking guard: any still-active appointment at that exact slot.
        clash = Appointment.objects.filter(
            doctor=doctor, datetime=when).exclude(status="CANCELLED").exists()
        if clash:
            return Response({"detail": "That slot is already booked."}, status=400)
        patient, _ = Patient.objects.get_or_create(
            user=request.user, defaults={"name": request.user.username})
        appt = Appointment.objects.create(
            patient=patient, doctor=doctor, datetime=when,
            reason=request.data.get("reason", ""))
        return Response(AppointmentSerializer(appt).data, status=201)


class PatientViewSet(viewsets.ModelViewSet):
    """Patient registry — clinic staff only (contains personal data)."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsMedicalStaffOrReadOnly]


class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Role-shaped: patients see their own; doctors see theirs; staff see all."""
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "doctor")
        user, role = self.request.user, role_of(self.request.user)
        if role in {"admin", "receptionist"}:
            return qs
        if role == "doctor":
            return qs.filter(doctor__user=user)
        return qs.filter(patient__user=user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """POST /api/appointments/<id>/cancel/ — patient (own) or staff."""
        appt = self.get_object()
        is_owner = appt.patient.user_id == request.user.id
        if not (is_owner or role_of(request.user) in {"admin", "receptionist", "doctor"}):
            return Response({"detail": "Not allowed."}, status=403)
        appt.status = "CANCELLED"
        appt.save()
        return Response(AppointmentSerializer(appt).data)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """STRICT: patients read only their OWN records; only doctors/admins write."""
    serializer_class = MedicalRecordSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsDoctorOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related("patient", "doctor")
        user, role = self.request.user, role_of(self.request.user)
        if role == "admin":
            return qs
        if role == "doctor":
            return qs.filter(doctor__user=user)
        # patients (and everyone else) see ONLY their own records
        return qs.filter(patient__user=user)
