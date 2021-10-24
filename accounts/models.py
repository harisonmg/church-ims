from django.contrib.auth.models import AbstractUser

from people.utils import get_personal_details


class User(AbstractUser):
    class Meta:  # noqa
        ordering = ["email"]

    @property
    def personal_details(self):
        return get_personal_details(self)
