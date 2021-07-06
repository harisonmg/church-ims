from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from core.validators import validate_adult, validate_child, validate_date_of_birth

from .models import FamilyRelationship, Person


class ChildForm(forms.ModelForm):
    dob = forms.DateField(
        label="Date of birth",
        help_text="Please use the following format: <em>DD/MM/YYYY.</em>",
        validators=[validate_date_of_birth, validate_child],
    )

    class Meta:
        model = Person
        fields = ("username", "full_name", "dob", "gender")


class FamilyRelationshipForm(forms.ModelForm):
    class Meta:
        model = FamilyRelationship
        fields = ("relative", "relationship_type")
