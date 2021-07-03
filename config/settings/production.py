from utils.config import list_of_tuples

from .base import *

# Django Settings
# ===============

# Email
ADMINS = decouple.config("ADMINS", cast=list_of_tuples)

MANAGERS = ADMINS


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

STATICFILES_STORAGE = "utils.storages.StaticRootGoogleCloudStorage"


# Media (user uploaded files)
# https://docs.djangoproject.com/en/3.1/ref/settings/#file-uploads

MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"

DEFAULT_FILE_STORAGE = "utils.storages.MediaRootGoogleCloudStorage"


# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_VERIFICATION = "mandatory"


# Project Specific Settings
# =========================

ADMIN_URL = decouple.config("ADMIN_URL")

GOOGLE_ANALYTICS_ID = decouple.config("GOOGLE_ANALYTICS_ID", default=None)

MIDDLEWARE.extend(
    [
        "django.middleware.common.BrokenLinkEmailsMiddleware",
    ]
)

TEMPLATES[0]["OPTIONS"]["context_processors"].extend(
    [
        "core.context_processors.google_analytics",
    ]
)
