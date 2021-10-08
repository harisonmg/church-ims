from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse

from .validators import validate_full_name


class Person(models.Model):
    username = models.CharField(
        max_length=50, unique=True, validators=[UnicodeUsernameValidator()]
    )
    full_name = models.CharField(max_length=300, validators=[validate_full_name])
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        ordering = ["username"]
        verbose_name_plural = "people"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("people:person_detail", kwargs={"username": self.username})
