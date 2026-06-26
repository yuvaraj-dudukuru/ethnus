"""asgi.py — the async entry point (not used by the dev server)."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicare.settings")
application = get_asgi_application()
