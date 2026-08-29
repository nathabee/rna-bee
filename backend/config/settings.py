import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-development-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    x.strip()
    for x in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
    ).split(",")
    if x.strip()
]

CSRF_TRUSTED_ORIGINS = [
    x.strip()
    for x in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if x.strip()
]

CORS_ALLOWED_ORIGINS = [
    x.strip()
    for x in os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").split(",")
    if x.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "rnabee"),
        "USER": os.environ.get("POSTGRES_USER", "rnabee"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "RNA Bee API",
    "DESCRIPTION": "REST API for RNA Bee simulations.",
    "VERSION": "0.1.0",
}
