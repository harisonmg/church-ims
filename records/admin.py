from django.contrib import admin

from .models import ChildTemperature


@admin.register(ChildTemperature)
class TemperatureRecordAdmin(admin.ModelAdmin):
    list_display = ("child", "temp", "created_at")
