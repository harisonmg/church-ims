from datetime import date

from django.conf import settings
from django.contrib.auth import validators
from django.db import models

from core.models import TimeStampedModel


class Person(TimeStampedModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
        ('P', 'Prefer not to say'),
    ]
    username = models.CharField(
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=150,
        unique=True,
        validators=[validators.UnicodeUsernameValidator()]
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
        ordering = ['username']
        verbose_name_plural = 'people'

    def __str__(self):
        return self.username

    def age(self):
        today = date.today()
        age = today.year - self.dob.year
        age -= ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


class FamilyMemberRelationship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships')
    relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_relationships')
    relationship_type = models.ForeignKey('RelationshipType', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.person}'s {self.relationship_type}"


class RelationshipType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
