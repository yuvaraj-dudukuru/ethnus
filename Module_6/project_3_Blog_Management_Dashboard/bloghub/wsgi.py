# ============================================================================
#  wsgi.py — the doorway real web servers use to talk to this project
# ----------------------------------------------------------------------------
#  Used when deploying to a production server. During local learning with
#  "runserver" you can ignore it, but Django needs it to exist.
# ============================================================================
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghub.settings')
application = get_wsgi_application()
