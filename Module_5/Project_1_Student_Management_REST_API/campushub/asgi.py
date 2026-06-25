# ============================================================================
#  asgi.py — the "async" version of wsgi.py
# ----------------------------------------------------------------------------
#  Used by modern async-capable servers (Daphne, Uvicorn) and for things like
#  WebSockets. We don't use it in this project, but Django expects the file to
#  exist. You never edit it.
# ============================================================================
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
application = get_asgi_application()
