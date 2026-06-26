# ============================================================================
#  apps.py — tiny configuration class for the "students" app
# ----------------------------------------------------------------------------
#  Django auto-generates this. It just gives the app a name and sets the
#  default primary-key type. You normally never touch it.
# ============================================================================
from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
