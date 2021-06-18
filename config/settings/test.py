from .base import *

# Django Settings
# ===============

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_HOST_USER =  'test@example.com'

EMAIL_HOST_PASSWORD =  'vErYiNsEcUrEp@sSW0rd!'
