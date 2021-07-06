from django.contrib import admin

from .models import BodyTemperature


@admin.register(BodyTemperature)
class TemperatureRecordAdmin(admin.ModelAdmin):
    list_display = ("person", "temp", "created_at")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
