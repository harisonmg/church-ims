from django.contrib import admin

from .models import Person, FamilyMemberRelationship, RelationshipType


class FamilyMembersInline(admin.TabularInline):
    model = FamilyMemberRelationship
    fk_name = 'person'
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'age')
    inlines = (FamilyMembersInline,)


@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(FamilyMemberRelationship)
class FamilyMemberRelationshipAdmin(admin.ModelAdmin):
    list_display = ('person', 'relative', 'relationship_type',)
