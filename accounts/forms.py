from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import fields

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
