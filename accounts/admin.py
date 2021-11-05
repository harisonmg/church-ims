from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["email", "person", "is_staff", "date_joined"]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "date_joined",
        "last_login",
    ]
    ordering = ["email"]
