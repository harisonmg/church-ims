from datetime import date

from django.conf import settings
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
        max_length=20, help_text="Enter a valid phone number"
    )


class Profile(models.Model):
    AGE_OF_MAJORITY = 18
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("C", "Custom"),
        ("P", "Prefer not to say"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, null=True)
    dob = models.DateField(verbose_name="date of birth", null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year
        age -= (today.month, today.day) < (self.dob.month, self.dob.day)
        return age

    @property
    def is_adult(self):
        return self.age >= self.AGE_OF_MAJORITY
