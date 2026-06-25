# ============================================================================
#  signals.py — automatically give every new User a Profile
# ----------------------------------------------------------------------------
#  Our permission classes read request.user.profile.role. That only works if
#  EVERY user has a profile. This signal makes sure of it: whenever a new User
#  is created (by registration, the admin, or createsuperuser), a Profile is
#  created for them too. The registration endpoint then sets the correct role.
#
#  A "signal" is Django's way of saying "when X happens, run this function".
#  Here X = "a User row was just saved for the first time".
# ============================================================================
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    # 'created' is True only the first time this user is saved.
    if created:
        # Default role 'C' (Candidate); registration overrides it if needed.
        Profile.objects.get_or_create(user=instance, defaults={'role': 'C'})
