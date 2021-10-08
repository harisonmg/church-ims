from django import forms

from .models import Person
from .validators import validate_full_name


class PersonForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, validators=[validate_full_name])

    class Meta:  # noqa
        model = Person
        fields = ["username", "full_name"]
