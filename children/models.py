import uuid
from datetime import date

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Child(TimeStampedModel):
    AGE_OF_MAJORITY = 18
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("C", "Custom"),
        ("P", "Prefer not to say"),
    ]
    slug = models.SlugField(
        verbose_name="username",
        help_text="Enter a unique username for your child. Don't use full-stops/periods",
        error_messages={"unique": "A child with that username already exists."},
        unique=True,
    )
    full_name = models.CharField(max_length=300)
    dob = models.DateField(
        verbose_name="date of birth", help_text="The format should be DD/MM/YYYY"
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="children_creators",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="children_editors",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["slug"]
        verbose_name_plural = "children"

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("children:detail", kwargs={"slug": self.slug})

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year
        age -= (today.month, today.day) < (self.dob.month, self.dob.day)
        return age

    @property
    def is_adult(self):
        return self.age >= self.AGE_OF_MAJORITY


class ParentChildRelationship(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parents"
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="children")
    relationship_type = models.ForeignKey(
        "RelationshipType",
        help_text="How are you related to the child?",
        on_delete=models.PROTECT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="parentchildrelationship_creators",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="parentchildrelationship_editors",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.child}'s {self.relationship_type}"

    def get_absolute_url(self):
        return reverse(
            "children:parent_child_relationship_detail", kwargs={"pk": self.pk}
        )


class RelationshipType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
