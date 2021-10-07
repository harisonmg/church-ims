from decimal import Decimal
from random import randint
from unittest import TestCase

from records import constants, validators


class HumanBodyTemperatureValidatorTestCase(TestCase):
    def test_maximum_temperature(self):
        with self.assertRaisesRegex(
            ValueError, validators.INVALID_HUMAN_BODY_TEMP_ERROR
        ):
            temperature = constants.MAX_HUMAN_BODY_TEMP + Decimal(0.01)
            validators.human_body_temperature_validator(temperature)

    def test_minimum_temperature(self):
        with self.assertRaisesRegex(
            ValueError, validators.INVALID_HUMAN_BODY_TEMP_ERROR
        ):
            temperature = constants.MIN_HUMAN_BODY_TEMP - Decimal(0.01)
            validators.human_body_temperature_validator(temperature)

    def test_valid_temperature(self):
        temperature = randint(
            constants.MIN_HUMAN_BODY_TEMP, constants.MAX_HUMAN_BODY_TEMP
        )
        result = validators.human_body_temperature_validator(temperature)
        self.assertEqual(result, None)
