from utils.config import list_of_tuples

from .base import *

# Django Settings
# ===============

# Email
ADMINS =  decouple.config('ADMINS', cast=list_of_tuples)

MANAGERS = ADMINS



# Project Specific Settings
# =========================

ADMIN_URL =  decouple.config('ADMIN_URL')

GOOGLE_ANALYTICS_ID = decouple.config('GOOGLE_ANALYTICS_ID', default=None)

# TEMPLATES[0]['OPTIONS']['context_processors'].append(
#     'core.context_processors.google_analytics'
# )
