# ============================================================================
#  models.py — a Profile that gives every user a ROLE (recruiter / candidate).
# ----------------------------------------------------------------------------
#  A post_save signal auto-creates a Profile (default: candidate) for every new
#  user, so role-based permissions always have something to read.
# ============================================================================
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLES = [("recruiter", "Recruiter"), ("candidate", "Candidate")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLES, default="candidate")
    headline = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def role_of(user):
    """Return 'recruiter' / 'candidate' / None for any user object."""
    if not getattr(user, "is_authenticated", False):
        return None
    profile = getattr(user, "profile", None)
    return profile.role if profile else None
