from django.contrib import admin

from .models import InterpersonalRelationship, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "dob", "created_by", "created_at"]
    list_display_links = None
    list_filter = ["created_at", "last_modified"]
    ordering = ["username"]
    search_fields = ["username", "created_by__email"]


@admin.register(InterpersonalRelationship)
class InterpersonalRelationshipAdmin(admin.ModelAdmin):
    list_display = ["person", "relative", "relation", "created_by", "created_at"]
    list_display_links = None
    list_filter = ["relation", "created_at"]
    ordering = ["person__username"]
    search_fields = ["person__username", "relative__username", "created_by__email"]
