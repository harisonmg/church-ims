from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from people.models import Person


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=254,
        error_messages={"unique": "A user with that email address already exists."},
        unique=True,
    )

    phone_number = PhoneNumberField(
        max_length=20, help_text="Enter a valid phone number"
    )
    profile = models.ForeignKey(
        Person,
        verbose_name="personal details",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
