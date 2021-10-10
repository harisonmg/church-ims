from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import Person
from .validators import validate_date_of_birth, validate_full_name


class PersonForm(forms.ModelForm):
    username = forms.CharField(max_length=25, validators=[UnicodeUsernameValidator()])
    full_name = forms.CharField(max_length=150, validators=[validate_full_name])
    dob = forms.DateField(label="date of birth", validators=[validate_date_of_birth])

    class Meta:  # noqa
        model = Person
        fields = ["username", "full_name", "gender", "dob"]
