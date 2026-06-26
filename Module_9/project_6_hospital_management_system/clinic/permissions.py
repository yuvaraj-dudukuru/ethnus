# ============================================================================
#  permissions.py — role gates for sensitive medical data.
# ============================================================================
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import role_of

MEDICAL_STAFF = {"doctor", "receptionist", "admin"}


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return role_of(request.user) == "admin"


class IsMedicalStaffOrReadOnly(BasePermission):
    """Read for any authenticated user; write only for clinic staff."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return role_of(request.user) in MEDICAL_STAFF


class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return role_of(request.user) in {"doctor", "admin"}
