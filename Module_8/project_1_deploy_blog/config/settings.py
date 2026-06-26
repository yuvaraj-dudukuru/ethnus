"""
Django settings for the Blog project — PRODUCTION-READY (Module 8).

This file was upgraded from the Module 4 development version so the SAME code
runs locally (SQLite, DEBUG on) and live on Render (PostgreSQL, DEBUG off,
HTTPS, WhiteNoise static files). Every environment-specific value is now read
from an environment variable, with safe local defaults.

Env vars (set these in the Render dashboard → Environment):
    SECRET_KEY      -> a long random string
    DEBUG           -> "False" in production
    ALLOWED_HOSTS   -> e.g. "blog-app.onrender.com" (comma-separated)
    DATABASE_URL    -> provided automatically by the Render PostgreSQL add-on
"""

from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load a local .env file if present (does nothing on Render, where real env
# vars are injected by the platform).
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: str = "False") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


# ---------------------------------------------------------------------------
#  CORE SECURITY SETTINGS (all from the environment)
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    # Insecure fallback for local development ONLY. Render overrides this.
    "django-insecure-local-dev-key-do-not-use-in-production",
)

DEBUG = env_bool("DEBUG", "True")  # local default True; Render sets DEBUG=False

# "blog.onrender.com,localhost,127.0.0.1"  ->  ['blog.onrender.com', ...]
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]
# Render injects RENDER_EXTERNAL_HOSTNAME automatically — trust it.
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)

# Any *.onrender.com preview/prod URL is a trusted CSRF origin.
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    *[f"https://{h}" for h in ALLOWED_HOSTS if h not in {"localhost", "127.0.0.1"}],
]


# ---------------------------------------------------------------------------
#  APPLICATION DEFINITION
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves compressed static files straight from the web process,
    # so we do not need a separate CDN/Nginx for CSS/JS. Must sit right after
    # SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------------------------
#  DATABASE
#  Locally (no DATABASE_URL) -> SQLite file. On Render -> the Postgres add-on
#  sets DATABASE_URL and dj-database-url parses it into Django's config.
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,                       # reuse connections (faster on Postgres)
        # Only force SSL when a real Postgres URL is supplied (Render). SQLite
        # locally must NOT receive an sslmode option.
        ssl_require=bool(DATABASE_URL) and not DEBUG,
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
#  INTERNATIONALISATION
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
#  STATIC FILES (WhiteNoise)
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# collectstatic copies everything here during the Render build step.
STATIC_ROOT = BASE_DIR / "staticfiles"
# Compress + hash static filenames for long-lived caching.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# ---------------------------------------------------------------------------
#  PRODUCTION-ONLY SECURITY HARDENING (active when DEBUG=False)
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000      # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
