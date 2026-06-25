# ============================================================================
#  permissions.py — the custom "IsOwnerOrReadOnly" rule
# ----------------------------------------------------------------------------
#  This is the production-grade permission class from Topic 5.3. It lets ANY
#  visitor READ an object, but only the object's OWNER (author) may change or
#  delete it. So strangers can read your post, but they can't edit it.
# ============================================================================
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Read for everyone; write only for the object's author."""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD and OPTIONS — i.e. read-only requests.
        # These are always allowed, for anyone.
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write requests (PUT/PATCH/DELETE), allow only if the logged-in
        # user is the author of this object. This is the "owner test":
        return obj.author == request.user
