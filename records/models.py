import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel
from people.models import Person


class BodyTemperature(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temp = models.DecimalField(
        verbose_name="temperature record",
        help_text="A person's body temperature in degrees celsius",
        max_digits=4,
        decimal_places=2,
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="temperature_creators",
        null=True,
    )

    class Meta:
        verbose_name_plural = "body temperature"
        db_table = "records_body_temperature"

    def __str__(self):
        return "{}'s temperature at {}".format(
            self.person, self.created_at.strftime("%d %b %Y %H:%M:%S")
        )

    def get_absolute_url(self):
        return reverse("temperature_detail", kwargs={"pk": self.pk})
