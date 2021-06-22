from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "email", "phone_number", "is_staff")
    ordering = ("username",)

    add_fieldsets = (
        (None, {
	        "classes": ("wide",),
	        "fields": ("username", "email", "phone_number", "password1", "password2"),
        }),
    )
    fieldsets = (
		("Credentials", {"fields": ("username", "password")}),
		("Personal info", {
			"fields": ("email", "phone_number")}),
		("Permissions", {
			"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
		}),
		("Important dates", {"fields": ("last_login", "date_joined")}),
	)
