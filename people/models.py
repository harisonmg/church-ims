from datetime import date
import uuid

from django.conf import settings
from django.contrib.auth import validators
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel


class Person(TimeStampedModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
        ('P', 'Prefer not to say'),
    ]
    slug = models.SlugField(
        verbose_name="username",
        help_text='Enter a URL-friendly name',
        error_messages={"unique": "A user with that username already exists."},
        unique=True
    )
    full_name = models.CharField(max_length=300)
    dob = models.DateField(verbose_name='date of birth')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    family_members = models.ManyToManyField(
        'self', through='FamilyMemberRelationship',
        through_fields=('person', 'relative')
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ['slug']
        verbose_name_plural = 'people'

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('people:detail', kwargs={"slug": self.slug})

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year
        age -= ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


class FamilyMemberRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships')
    relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_relationships')
    relationship_type = models.ForeignKey('RelationshipType', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.person}'s {self.relationship_type}"


class RelationshipType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
