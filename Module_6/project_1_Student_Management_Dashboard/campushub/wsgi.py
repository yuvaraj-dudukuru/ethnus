# ============================================================================
#  wsgi.py — the doorway real web servers use to talk to this project
# ----------------------------------------------------------------------------
#  When you eventually deploy to a production server (Gunicorn, uWSGI, Apache),
#  that server loads this file to start the app. During local learning with
#  "python manage.py runserver" you can ignore it — but Django needs it to
#  exist. You never edit it.
# ============================================================================
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
application = get_wsgi_application()
