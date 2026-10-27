"""
Django settings for the Inventory backend.

These settings are for local development only. Before putting the site on
the internet: set a new SECRET_KEY, set DEBUG = False, and fill in
ALLOWED_HOSTS.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Development-only key. Replace before deploying anywhere public.
SECRET_KEY = "django-insecure-dev-only-change-me-before-deploying"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Our app: user accounts and the sign-in / sign-up API
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
        "DIRS": [],
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

# The account database. SQLite stores everything in one file (db.sqlite3)
# next to manage.py, so there is nothing extra to install. Later you can
# switch to PostgreSQL by changing only this block.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Use our own User model (accounts/models.py) instead of Django's default.
# Doing this at the start of a project is much easier than changing it later.
AUTH_USER_MODEL = "accounts.User"

# Password rules applied when someone creates an account.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# The React site runs on the Vite dev server (port 8443) and forwards /api
# requests here. Django's CSRF protection needs to trust that address.
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8443",
    "http://127.0.0.1:8443",
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
