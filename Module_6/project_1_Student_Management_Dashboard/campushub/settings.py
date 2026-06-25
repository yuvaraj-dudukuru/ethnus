# ============================================================================
#  settings.py — the project's master configuration file
# ----------------------------------------------------------------------------
#  Every important switch for the whole project lives here: which apps are
#  turned on, where the database is, and (most importantly for us) the big
#  REST_FRAMEWORK block that configures authentication, permissions,
#  pagination, throttling and documentation for the API.
# ============================================================================
from pathlib import Path

# BASE_DIR is the absolute path to the "Project 1" folder (two levels up from
# this file). Everything else is described relative to it.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
#  SECURITY
# ---------------------------------------------------------------------------
# This key signs cookies and tokens. For a real, public website you must keep
# it secret. Because this is a LEARNING project that will live on GitHub, we
# use a simple, obviously-fake key. Never reuse this key in production.
SECRET_KEY = 'django-insecure-student-learning-key-change-me-in-production'

# DEBUG=True shows full error pages with helpful tracebacks. Great while
# learning, but must be False on a real live server.
DEBUG = True

# Which host names are allowed to serve this site. '*' means "any", which is
# fine for local learning. (Don't use '*' on a real server.)
ALLOWED_HOSTS = ['*']

# ---------------------------------------------------------------------------
#  INSTALLED APPS — every "feature module" Django should load
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # --- Django's own built-in apps ---
    'django.contrib.admin',          # The /admin/ control panel
    'django.contrib.auth',           # Users, groups, passwords, permissions
    'django.contrib.contenttypes',   # Plumbing the auth system needs
    'django.contrib.sessions',       # Server-side login sessions
    'django.contrib.messages',       # One-time flash messages
    'django.contrib.staticfiles',    # CSS/JS handling

    # --- Third-party apps we installed with pip ---
    'rest_framework',                # Django REST Framework (the API toolkit)
    'rest_framework.authtoken',      # Gives each user an auth token (the login token)
    'django_filters',               # The ?min_marks=&department= filtering backend
    'drf_spectacular',              # Auto-builds the Swagger API documentation

    # --- Our own app ---
    'students',                      # All our models, serializers and views live here
]

# ---------------------------------------------------------------------------
#  MIDDLEWARE — small layers every request passes through (security, sessions…)
#  These are Django defaults; you normally don't change them.
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The Python path to the project-wide URL table (campushub/urls.py).
ROOT_URLCONF = 'campushub.urls'

# Template settings — needed so the Django admin and the browsable API can
# render their HTML pages. Defaults are fine.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Entry point used by production web servers. Not used during "runserver".
WSGI_APPLICATION = 'campushub.wsgi.application'

# ---------------------------------------------------------------------------
#  DATABASE
# ---------------------------------------------------------------------------
# SQLite is a tiny database stored in a single file (db.sqlite3). It needs no
# setup or password, which is perfect for students. The file is created
# automatically the first time you run "python manage.py migrate".
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
#  PASSWORD VALIDATION
# ---------------------------------------------------------------------------
# These rules normally reject weak passwords. Because this is a teaching
# project and we deliberately use the simple password "admin", we leave this
# list EMPTY so Django won't complain. (On a real site, keep the validators.)
AUTH_PASSWORD_VALIDATORS = []

# ---------------------------------------------------------------------------
#  INTERNATIONALISATION (language / time zone) — defaults are fine
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Where the browsable API / admin CSS & JS are served from.
STATIC_URL = 'static/'

# ---------------------------------------------------------------------------
#  STATICFILES_DIRS — extra folders Django searches for static files (NEW in M6)
# ---------------------------------------------------------------------------
#  Our Module-6 front-end JavaScript lives in the project-root "static/" folder
#  (static/js/dashboard.js). Listing that folder here lets the
#  {% static 'js/dashboard.js' %} tag inside dashboard.html find and serve it
#  while the development server is running. This is the only settings change
#  Module 6 needs — everything else is reused unchanged from Module 5.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default type for auto-created primary key (id) columns.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================================================================
#  REST_FRAMEWORK — the heart of the API configuration
#  This single dictionary wires up authentication, permissions, pagination,
#  throttling and the documentation schema for EVERY endpoint at once.
# ===========================================================================
REST_FRAMEWORK = {
    # HOW a request proves who it is. We accept two methods:
    #  - TokenAuthentication: send header "Authorization: Token <your-token>"
    #  - SessionAuthentication: normal browser login (lets the browsable API work)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    # The DEFAULT rule for who may do what, unless a view overrides it.
    # "IsAuthenticatedOrReadOnly" = anyone can READ (GET), but you must be
    # logged in to WRITE (POST/PUT/PATCH/DELETE).
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Long lists are split into pages of 10 (see campushub/pagination.py).
    'DEFAULT_PAGINATION_CLASS': 'campushub.pagination.StandardPagination',

    # Rate limiting: stop anyone hammering the API too fast.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',   # limits anonymous users
        'rest_framework.throttling.UserRateThrottle',   # limits logged-in users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',     # an anonymous visitor: 100 requests per hour
        'user': '2000/day',     # a logged-in user: 2000 requests per day
        'login': '5/minute',    # the login endpoint: 5 tries per minute (anti-brute-force)
    },

    # Tells drf-spectacular how to build the OpenAPI schema for the docs page.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Optional title/description shown at the top of the Swagger docs page.
SPECTACULAR_SETTINGS = {
    'TITLE': 'Student Management REST API',
    'DESCRIPTION': 'A simple, fully working DRF teaching project (CampusHub).',
    'VERSION': '1.0.0',
}
