from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import fields

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields