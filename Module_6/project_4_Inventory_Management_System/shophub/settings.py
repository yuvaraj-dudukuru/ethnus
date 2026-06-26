# ============================================================================
#  settings.py — the project's master configuration file
# ----------------------------------------------------------------------------
#  Every important switch lives here: which apps are on, where the database is,
#  and the big REST_FRAMEWORK block (authentication, permissions, pagination,
#  throttling, docs).
# ============================================================================
from pathlib import Path

# BASE_DIR is the absolute path to the "Project 4" folder (two levels up).
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
#  SECURITY
# ---------------------------------------------------------------------------
# A deliberately fake learning key (this project lives on GitHub). Never reuse
# it in production.
SECRET_KEY = 'django-insecure-shop-learning-key-change-me-in-production'

DEBUG = True              # full, helpful error pages (turn off on a real server)
ALLOWED_HOSTS = ['*']     # any host may serve the site (fine for local learning)

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
    'django_filters',               # The ?category=&min_price= filtering backend
    'drf_spectacular',              # Auto-builds the Swagger API documentation

    # --- Our own app ---
    'shop',                          # Categories, Products, Cart, Orders live here
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

ROOT_URLCONF = 'shophub.urls'

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

WSGI_APPLICATION = 'shophub.wsgi.application'

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

# ---------------------------------------------------------------------------
#  STATICFILES_DIRS — extra folders Django searches for static files (NEW in M6)
# ---------------------------------------------------------------------------
#  Our Module-6 front-end JavaScript lives in the project-root "static/" folder
#  (static/js/dashboard.js). Listing that folder here lets the
#  {% static 'js/dashboard.js' %} tag inside dashboard.html find and serve it.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================================================================
#  REST_FRAMEWORK — authentication, permissions, pagination, throttling, docs
# ===========================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',   # header: Authorization: Token <token>
        'rest_framework.authentication.SessionAuthentication', # normal browser login
    ],

    # Default: anyone can READ, you must log in to WRITE. Cart and Orders
    # tighten this to "logged-in only" in their own views.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Default paging style for most lists (orders, etc.). The PRODUCT catalog
    # overrides this with CursorPagination (see shop/pagination.py) because a
    # live shop catalog is big and constantly changing.
    'DEFAULT_PAGINATION_CLASS': 'shophub.pagination.StandardPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '2000/day',
    },

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce REST API',
    'DESCRIPTION': 'A simple, fully working DRF teaching project (ShopHub).',
    'VERSION': '1.0.0',
}
