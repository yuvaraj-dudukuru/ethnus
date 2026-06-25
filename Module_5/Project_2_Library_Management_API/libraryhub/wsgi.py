# ============================================================================
#  wsgi.py — the doorway real web servers use to talk to this project
# ----------------------------------------------------------------------------
#  Used when you deploy to a production server (Gunicorn, uWSGI, Apache).
#  During local learning with "runserver" you can ignore it, but Django needs
#  it to exist. You never edit it.
# ============================================================================
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryhub.settings')
application = get_wsgi_application()
