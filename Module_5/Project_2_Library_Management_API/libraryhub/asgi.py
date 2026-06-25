# ============================================================================
#  asgi.py — the "async" version of wsgi.py
# ----------------------------------------------------------------------------
#  Used by modern async-capable servers and for WebSockets. We don't use it,
#  but Django expects the file to exist. You never edit it.
# ============================================================================
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryhub.settings')
application = get_asgi_application()
