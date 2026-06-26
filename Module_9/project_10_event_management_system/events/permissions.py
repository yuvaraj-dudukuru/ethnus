# ============================================================================
#  permissions.py — only the organizer who owns an event may edit it.
# ============================================================================
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.organizer_id == request.user.id or request.user.is_staff
