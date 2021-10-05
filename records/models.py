from django.db import models

from .utils import format_temperature


class TemperatureRecord(models.Model):
    person = models.ForeignKey("people.Person", on_delete=models.PROTECT)
    body_temperature = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="The person's body temperature in degrees celsius.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        db_table = "records_temperature"
        ordering = ["person__username", "created_at"]

    def __str__(self):
        temp = format_temperature(self.body_temperature)
        return f"{self.person} was {temp} at {self.created_at}"
