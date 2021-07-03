from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from people.models import FamilyRelationship

from .models import CustomUser


class FamilyRelationshipInline(admin.TabularInline):
    model = FamilyRelationship
    fk_name = "person"
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "person", "email", "phone_number", "is_staff")
    ordering = ("username",)
    # inlines = [FamilyRelationshipInline,]

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
        ("Login credentials", {"fields": ("username", "password")}),
        ("Contact info", {"fields": ("email", "phone_number")}),
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
