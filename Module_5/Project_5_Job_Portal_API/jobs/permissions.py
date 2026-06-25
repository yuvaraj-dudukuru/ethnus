# ============================================================================
#  permissions.py — the role-based permission classes (the heart of Project 5)
# ----------------------------------------------------------------------------
#  These classes answer "is THIS user allowed to do THIS action?" by looking
#  at the user's role (recruiter vs candidate) and, for editing, whether they
#  OWN the object.
# ============================================================================
from rest_framework import permissions


def _role(user):
    """Safely read a user's role, or None if they have no profile / aren't logged in."""
    if user and user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role
    return None


class IsRecruiter(permissions.BasePermission):
    """Allow only logged-in RECRUITERS."""
    message = "Only recruiters can do this."

    def has_permission(self, request, view):
        return _role(request.user) == 'R'


class IsCandidate(permissions.BasePermission):
    """Allow only logged-in CANDIDATES (used by the 'apply' action)."""
    message = "Only candidates can apply."

    def has_permission(self, request, view):
        return _role(request.user) == 'C'


class IsRecruiterOwnerOrReadOnly(permissions.BasePermission):
    """For jobs: anyone may READ; only recruiters may CREATE; and only the
    recruiter who OWNS a job may edit or delete it.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS (GET/HEAD/OPTIONS) = read-only -> allowed for everyone.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Any write (POST/PUT/PATCH/DELETE) requires the recruiter role.
        return _role(request.user) == 'R'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Editing/deleting a specific job: must be the job's own recruiter.
        return obj.recruiter == request.user
