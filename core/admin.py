from django.conf import settings
from django.contrib import admin

admin.site.site_header = f"{settings.SITE_NAME} administration"
admin.site.site_title = f"{settings.SITE_NAME} admin"
