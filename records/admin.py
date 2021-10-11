from django.contrib import admin

from .models import TemperatureRecord


@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(admin.ModelAdmin):
    list_display = ["person", "body_temperature", "created_at", "created_by"]
    list_display_links = None
    list_filter = ["created_at"]
    ordering = ["person__username", "-created_at"]
    search_fields = ["created_by__email"]
