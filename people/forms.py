from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from . import constants, validators
from .models import InterpersonalRelationship, Person

SELF_RELATIONSHIPS_ERROR = "Self relationships are not allowed!"
DUPLICATE_RELATIONSHIPS_ERROR = "This interpersonal relationship already exists"


class PersonUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=25, validators=[UnicodeUsernameValidator()])
    full_name = forms.CharField(
        max_length=150, validators=[validators.validate_full_name]
    )

    class Meta:  # noqa
        model = Person
        fields = ["username", "full_name"]


class PersonCreationForm(PersonUpdateForm):
    dob = forms.DateField(
        label="Date of birth", validators=[validators.validate_date_of_birth]
    )

    class Meta(PersonUpdateForm.Meta):  # noqa
        fields = ["username", "full_name", "gender", "dob"]


class AdultCreationForm(PersonCreationForm):
    dob = forms.DateField(
        label="Date of birth",
        validators=[validators.validate_date_of_birth, validators.validate_adult],
    )

    class Meta(PersonCreationForm.Meta):  # noqa
        fields = ["username", "full_name", "gender", "dob", "phone_number"]


class ChildCreationForm(PersonCreationForm):
    dob = forms.DateField(
        label="Date of birth",
        validators=[validators.validate_date_of_birth, validators.validate_child],
    )
    is_parent = forms.BooleanField(label="I am the child's parent", required=False)


class ParentChildRelationshipCreationForm(forms.ModelForm):
    person = forms.CharField(
        label="The parent's username",
        max_length=25,
        validators=[validators.validate_person_username],
    )

    class Meta:  # noqa
        model = InterpersonalRelationship
        fields = ["person"]

    def clean_person(self):
        person = self.cleaned_data["person"]
        return Person.objects.get(username=person)


class InterpersonalRelationshipCreationForm(ParentChildRelationshipCreationForm):
    person = forms.CharField(
        label="The person's username",
        max_length=25,
        validators=[validators.validate_person_username],
    )
    relative = forms.CharField(
        label="The relative's username",
        max_length=25,
        validators=[validators.validate_person_username],
    )
    relation = forms.ChoiceField(
        label="Relationship type",
        choices=constants.INTERPERSONAL_RELATIONSHIP_CHOICES,
        initial=constants.FAMILIAL_RELATIONSHIPS[0],
    )

    class Meta(ParentChildRelationshipCreationForm.Meta):  # noqa
        fields = ["person", "relative", "relation"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": DUPLICATE_RELATIONSHIPS_ERROR,
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("person") == cleaned_data.get("relative"):
            raise ValidationError(SELF_RELATIONSHIPS_ERROR)

    def clean_relative(self):
        relative = self.cleaned_data["relative"]
        return Person.objects.get(username=relative)
