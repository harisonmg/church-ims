from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class CustomSignupForm(SignupForm):
    phone_number = PhoneNumberField(
        max_length=20, help_text="Enter a valid phone number"
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
