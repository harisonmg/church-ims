import uuid

from django.conf import settings
from django.db import models

from children.models import Child
from core.models import TimeStampedModel


class TemperatureRecord(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temp = models.DecimalField(
        verbose_name="temperature record",
        help_text="A person's body temperature in degrees celsius",
        max_digits=4,
        decimal_places=2,
    )

    class Meta:
        abstract = True


class ChildTemperature(TemperatureRecord):
    child = models.ForeignKey(Child, on_delete=models.PROTECT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="childtemperature_creators",
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="childtemperature_editors",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "ChildrenTemperature"

    def __str__(self):
        return "{}'s temperature at {}".format(
            self.child, self.created_at.strftime("%d %b %Y %H:%M:%S")
        )
