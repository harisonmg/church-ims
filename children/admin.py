from django.contrib import admin

from .models import Child, ParentChildRelationship, RelationshipType


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('slug', 'full_name', 'age', 'gender')


@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ParentChildRelationship)
class ParentChildRelationshipAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child', 'relationship_type',)
