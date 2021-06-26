from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "dob", "gender")
