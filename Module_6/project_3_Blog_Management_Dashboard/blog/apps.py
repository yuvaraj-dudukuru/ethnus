# ============================================================================
#  apps.py — tiny configuration class for the "blog" app
# ----------------------------------------------------------------------------
#  Django auto-generates this. It just names the app and sets the default
#  primary-key type. You normally never touch it.
# ============================================================================
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
