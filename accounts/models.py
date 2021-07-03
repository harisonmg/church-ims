from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=254,
        error_messages={"unique": "A user with that email address already exists."},
        unique=True,
    )

    phone_number = PhoneNumberField(
        max_length=50,
        help_text="Enter a valid phone number that starts with a country code.",
    )
