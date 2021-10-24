from config.helpers import list_of_tuples

from .base import *

# Django Settings
# ===============

# Email
ADMINS = decouple.config("ADMINS", cast=list_of_tuples)

EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "

MANAGERS = ADMINS

SECURE_SSL_REDIRECT = decouple.config("SECURE_SSL_REDIRECT", cast=bool, default=True)

SECURE_HSTS_SECONDS = decouple.config("SECURE_HSTS_SECONDS", cast=int, default=3600)

SECURE_HSTS_INCLUDE_SUBDOMAINS = decouple.config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=True
)

SECURE_HSTS_PRELOAD = decouple.config("SECURE_HSTS_PRELOAD", cast=bool, default=True)

SESSION_COOKIE_SECURE = decouple.config(
    "SESSION_COOKIE_SECURE", cast=bool, default=True
)

CSRF_COOKIE_SECURE = decouple.config("CSRF_COOKIE_SECURE", cast=bool, default=True)


# Third Party Apps Settings
# =========================

# Django Storages: Google Cloud Storage
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html#settings

GS_BUCKET_NAME = decouple.config("GCP_STORAGE_BUCKET_NAME")


# Django Settings that depend on 3rd party app settings
# ------------------------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/ref/settings/#static-files

STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

STATICFILES_STORAGE = "config.storages.StaticRootGoogleCloudStorage"


# Media (user uploaded files)
# https://docs.djangoproject.com/en/3.1/ref/settings/#file-uploads

MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

DEFAULT_FILE_STORAGE = "config.storages.MediaRootGoogleCloudStorage"


# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_VERIFICATION = "mandatory"


# Project Specific Settings
# =========================

ADMIN_URL = decouple.config("ADMIN_URL")

MIDDLEWARE += [
    "django.middleware.common.BrokenLinkEmailsMiddleware",
]

TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "core.context_processors.google_analytics"
]
