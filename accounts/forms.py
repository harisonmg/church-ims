from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from core.validators import validate_adult, validate_date_of_birth
from people.models import Person


class CustomSignupForm(SignupForm):
    phone_number = PhoneNumberField(
        max_length=20, help_text="Enter a valid phone number"
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user


class ProfileForm(forms.ModelForm):
    dob = forms.DateField(
        label="Date of birth",
        help_text="Please use the following format: <em>DD/MM/YYYY.</em>",
        validators=[validate_date_of_birth, validate_adult],
    )

    class Meta:
        model = Person
        fields = ("username", "full_name", "dob", "gender")
