# ============================================================================
#  permissions.py — instructors (course owners) may edit; everyone may read.
# ============================================================================
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInstructorOwnerOrReadOnly(BasePermission):
    """Read for all. Create for any logged-in user (they become the instructor).
    Edit/delete only for the course's own instructor (or an admin)."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = obj.instructor_id if hasattr(obj, "instructor_id") else obj.course.instructor_id
        return owner == request.user.id or request.user.is_staff
