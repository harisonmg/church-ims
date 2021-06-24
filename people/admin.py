from django.contrib import admin

from .models import Person, FamilyRelationship, RelationshipType


class FamilyMembersInline(admin.TabularInline):
    model = FamilyRelationship
    fk_name = 'person'
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('slug', 'full_name', 'age')
    inlines = (FamilyMembersInline,)


@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(FamilyRelationship)
class FamilyRelationshipAdmin(admin.ModelAdmin):
    list_display = ('person', 'relative', 'relationship_type',)
