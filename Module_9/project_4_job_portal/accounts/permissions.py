# ============================================================================
#  permissions.py — role-based access rules for the job portal.
# ============================================================================
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import role_of


class IsRecruiter(BasePermission):
    message = "Only recruiters may do this."

    def has_permission(self, request, view):
        return role_of(request.user) == "recruiter"


class IsCandidate(BasePermission):
    message = "Only candidates may do this."

    def has_permission(self, request, view):
        return role_of(request.user) == "candidate"


class IsRecruiterOwnerOrReadOnly(BasePermission):
    """Anyone may read jobs. Only recruiters may create. Only the recruiter who
    OWNS a job may edit/delete it."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return role_of(request.user) == "recruiter"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.recruiter_id == getattr(request.user, "id", None)
