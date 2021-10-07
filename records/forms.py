from django import forms

from . import constants
from .models import TemperatureRecord


class TemperatureRecordForm(forms.ModelForm):
    body_temperature = forms.DecimalField(
        min_value=constants.MIN_HUMAN_BODY_TEMP,
        max_value=constants.MAX_HUMAN_BODY_TEMP,
        decimal_places=2,
        required=True,
    )

    class Meta:  # noqa
        model = TemperatureRecord
        fields = ["body_temperature"]
