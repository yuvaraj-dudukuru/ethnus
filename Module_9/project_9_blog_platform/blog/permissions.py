# ============================================================================
#  permissions.py — only the author may edit/delete their own content.
# ============================================================================
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Read for everyone; write only if you're logged in; edit/delete only if
    you are the object's author/owner."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, "author_id", None) or getattr(obj, "user_id", None)
        return owner == request.user.id or request.user.is_staff
