# ============================================================================
#  apps.py — configuration class for the "jobs" app
# ----------------------------------------------------------------------------
#  Besides naming the app, the ready() method imports our signals module so
#  the "auto-create a Profile for every new user" signal gets connected when
#  Django starts.
# ============================================================================
from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        # Importing the module connects the post_save signal (see signals.py).
        from . import signals  # noqa: F401
