# ============================================================================
#  settings.py — the project's master configuration file
# ----------------------------------------------------------------------------
#  Every important switch for the whole project lives here: which apps are on,
#  where the database is, and the big REST_FRAMEWORK block that configures
#  authentication, permissions, pagination, throttling and documentation.
# ============================================================================
from pathlib import Path

# BASE_DIR is the absolute path to the "Project 2" folder (two levels up).
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
#  SECURITY
# ---------------------------------------------------------------------------
# This key signs cookies and tokens. Because this is a LEARNING project that
# will live on GitHub, we use a simple, obviously-fake key. Never reuse this
# key in production.
SECRET_KEY = 'django-insecure-library-learning-key-change-me-in-production'

# DEBUG=True shows full, helpful error pages. Must be False on a real server.
DEBUG = True

# Which host names may serve this site. '*' = any, fine for local learning.
ALLOWED_HOSTS = ['*']

# ---------------------------------------------------------------------------
#  INSTALLED APPS — every "feature module" Django should load
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # --- Django's own built-in apps ---
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --- Third-party apps installed with pip ---
    'rest_framework',                # Django REST Framework (the API toolkit)
    'rest_framework.authtoken',      # Gives each user a login token
    'django_filters',               # The ?available=true&author= filtering backend
    'drf_spectacular',              # Auto-builds the Swagger API documentation

    # --- Our own app ---
    'library',                       # Authors, Books, Members, Issues live here
]

# ---------------------------------------------------------------------------
#  MIDDLEWARE — Django defaults; you normally don't change them.
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

# The Python path to the project-wide URL table (libraryhub/urls.py).
ROOT_URLCONF = 'libraryhub.urls'

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

WSGI_APPLICATION = 'libraryhub.wsgi.application'

# ---------------------------------------------------------------------------
#  DATABASE — SQLite: a single file, no setup or password. Perfect for students.
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# We deliberately allow the simple password "admin", so we disable the
# strength validators. (On a real site, keep them.)
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================================================================
#  REST_FRAMEWORK — authentication, permissions, pagination, throttling, docs
# ===========================================================================
REST_FRAMEWORK = {
    # HOW a request proves who it is.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',   # header: Authorization: Token <token>
        'rest_framework.authentication.SessionAuthentication', # normal browser login
    ],

    # Default rule: anyone can READ, you must log in to WRITE. Individual
    # ViewSets override this (e.g. members are staff-only, books use the
    # Librarians-group model permissions).
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Long lists are split into pages of 10 (see libraryhub/pagination.py).
    'DEFAULT_PAGINATION_CLASS': 'libraryhub.pagination.StandardPagination',

    # Rate limiting (throttling) to stop anyone hammering the API.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '2000/day',
    },

    # Tells drf-spectacular how to build the docs.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Library Management REST API',
    'DESCRIPTION': 'A simple, fully working DRF teaching project (LibraryHub).',
    'VERSION': '1.0.0',
}
