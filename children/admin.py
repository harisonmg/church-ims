from django.contrib import admin

from .models import Child, ParentChildRelationship, RelationshipType


class ParentChildRelationshipInline(admin.StackedInline):
    model = ParentChildRelationship
    fk_name = "child"
    extra = 0


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("slug", "full_name", "age", "gender")
    inlines = [
        ParentChildRelationshipInline,
    ]


@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ParentChildRelationship)
class ParentChildRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        "parent",
        "child",
        "relationship_type",
    )
