import uuid
from datetime import date

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Person(TimeStampedModel):
    AGE_OF_MAJORITY = 18
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("C", "Custom"),
        ("P", "Prefer not to say"),
    ]
    username = models.SlugField(
        default=uuid.uuid4,
        error_messages={"unique": "A user with that username already exists."},
        help_text="Enter a unique username. Don't use full-stops/periods",
        unique=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    full_name = models.CharField(max_length=300, null=True)
    dob = models.DateField(verbose_name="date of birth", null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    family_members = models.ManyToManyField(
        "self",
        through="FamilyRelationship",
        through_fields=("person", "relative"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="people_creators",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="people_editors",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["username"]
        verbose_name_plural = "people"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("people:person_detail", kwargs={"username": self.username})

    @property
    def age(self):
        if self.dob is not None:
            today = date.today()
            age = today.year - self.dob.year
            age -= (today.month, today.day) < (self.dob.month, self.dob.day)
            return age
        return None

    @property
    def is_adult(self):
        if self.age is not None:
            return self.age >= self.AGE_OF_MAJORITY
        return "Undefined"


class FamilyRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    relative = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="relatives"
    )
    relationship_type = models.ForeignKey(
        "RelationshipType",
        help_text="How are you related to the person?",
        on_delete=models.PROTECT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="relationship_creators",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="relationship_editors",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "family_relationship"
        constraints = [
            models.UniqueConstraint(
                fields=["person", "relative"],
                name="%(app_label)s_%(class)s_unique_relationships",
            ),
            models.CheckConstraint(
                check=~models.Q(person=models.F("relative")),
                name="%(app_label)s_%(class)s_prevent_self_relationship",
            ),
        ]

    def __str__(self):
        return f"{self.person}'s {self.relationship_type}"

    def get_absolute_url(self):
        return reverse("people:family_relationship_detail", kwargs={"pk": self.pk})


class RelationshipType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "relationship_type"

    def __str__(self):
        return self.name