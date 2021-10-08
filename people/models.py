from django.db import models
from django.urls import reverse

from people.validators import full_name_validator


class Person(models.Model):
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=300, validators=[full_name_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        ordering = ["username"]
        verbose_name_plural = "people"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("people:person_detail", kwargs={"username": self.username})
