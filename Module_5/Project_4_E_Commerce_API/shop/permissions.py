# ============================================================================
#  permissions.py — a small reusable "admin writes, everyone reads" rule
# ----------------------------------------------------------------------------
#  Used for the product catalog: any visitor may browse (read) products, but
#  only an admin/staff user may create, edit or delete them.
# ============================================================================
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Read for everyone; write only for staff/admin users."""

    def has_permission(self, request, view):
        # SAFE_METHODS (GET, HEAD, OPTIONS) are read-only — always allowed.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Any other method (POST/PUT/PATCH/DELETE) requires a staff user.
        return bool(request.user and request.user.is_staff)
