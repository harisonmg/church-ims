from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin

from children.models import ParentChildRelationship

from .models import CustomUser, Profile


class ChildrenInline(admin.TabularInline):
    model = ParentChildRelationship
    fk_name = 'parent'
    extra = 1

class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "phone_number", "is_staff")
    ordering = ("username",)
    # inlines = [ProfileInline, ChildrenInline]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('slug', 'full_name', 'age', 'gender')