from django.contrib import admin

from .models import FamilyRelationship, Person, RelationshipType


class FamilyMembersInline(admin.TabularInline):
    model = FamilyRelationship
    fk_name = "person"
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "age", "user", "created_by")
    list_filter = ("gender", "dob")
    inlines = (FamilyMembersInline,)
    search_fields = ("username", "full_name")
    ordering = ("username",)


@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(FamilyRelationship)
class FamilyRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "relative",
        "relationship_type",
    )
    ordering = ("person", "relative")
