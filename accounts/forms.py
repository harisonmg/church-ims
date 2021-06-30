from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from people.models import Person

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("username", "full_name", "dob", "gender")
