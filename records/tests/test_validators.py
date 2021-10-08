from decimal import Decimal
from unittest import TestCase

from django.core.exceptions import ValidationError

from records import constants, validators


class HumanBodyTemperatureValidatorTestCase(TestCase):
    def test_maximum_temperature(self):
        with self.assertRaisesRegex(
            ValidationError, validators.INVALID_HUMAN_BODY_TEMP_ERROR
        ):
            temperature = constants.MAX_HUMAN_BODY_TEMP + Decimal(0.01)
            validators.validate_human_body_temperature(temperature)

    def test_minimum_temperature(self):
        with self.assertRaisesRegex(
            ValidationError, validators.INVALID_HUMAN_BODY_TEMP_ERROR
        ):
            temperature = constants.MIN_HUMAN_BODY_TEMP - Decimal(0.01)
            validators.validate_human_body_temperature(temperature)
