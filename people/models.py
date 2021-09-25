from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        ordering = ["username"]
        verbose_name_plural = "people"

    def __str__(self):
        return self.username
