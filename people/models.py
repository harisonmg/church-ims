import uuid

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

from .constants import (
    AGE_OF_MAJORITY,
    GENDER_CHOICES,
    INTERPERSONAL_RELATIONSHIP_CHOICES,
)
from .utils import get_age, get_age_category
from .validators import validate_full_name


class Person(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A person with that username already exists."},
    )
    full_name = models.CharField(max_length=300, validators=[validate_full_name])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(verbose_name="date of birth")
    phone_number = PhoneNumberField(null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="This person's user account.",
    )
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The user who created this record.",
        related_name="people_creators",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        ordering = ["username"]
        verbose_name_plural = "people"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("people:person_detail", kwargs={"username": self.username})

    @property
    def age(self):
        return get_age(self.dob)

    @property
    def age_category(self):
        return get_age_category(self.age)

    @property
    def is_adult(self):
        return self.age >= AGE_OF_MAJORITY


class InterpersonalRelationship(models.Model):
    id = models.UUIDField(
        editable=False, default=uuid.uuid4, primary_key=True, verbose_name="ID"
    )
    person = models.ForeignKey(
        to=Person, on_delete=models.CASCADE, related_name="relationships"
    )
    relative = models.ForeignKey(
        to=Person, on_delete=models.CASCADE, related_name="reverse_relationships"
    )
    relation = models.CharField(
        max_length=2,
        choices=INTERPERSONAL_RELATIONSHIP_CHOICES,
        help_text="How the person and the relative are associated.",
    )
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The user who created this record.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        constraints = [
            models.UniqueConstraint(
                fields=["person", "relative"],
                name="%(app_label)s_unique_%(class)s",
            )
        ]
        db_table = "people_relationship"
        ordering = ["person__username"]

    def __str__(self):
        people = f"{self.person} and {self.relative}"
        relation = self.get_relation_display().lower()
        return f"{people} have a {relation} relationship"
