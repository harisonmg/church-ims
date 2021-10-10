import uuid

from django.conf import settings
from django.db import models

from .utils import format_temperature
from .validators import validate_human_body_temperature


class TemperatureRecord(models.Model):
    id = models.UUIDField(
        editable=False, default=uuid.uuid4, primary_key=True, verbose_name="ID"
    )
    person = models.ForeignKey("people.Person", on_delete=models.PROTECT)
    body_temperature = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[validate_human_body_temperature],
        help_text="The person's body temperature in degrees celsius.",
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
        db_table = "records_temperature"
        ordering = ["person__username", "created_at"]

    def __str__(self):
        temp = format_temperature(self.body_temperature)
        return f"{self.person} was {temp} at {self.created_at}"
