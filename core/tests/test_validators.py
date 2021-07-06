from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from core import constants, validators


class CoreValidatorsTestCase(SimpleTestCase):
    def test_dob_not_in_future(self):
        with self.assertRaises(ValidationError):
            tomorrow = date.today() + timedelta(days=1)
            validators.validate_date_of_birth(tomorrow)

    def test_dob_not_in_distant_past(self):
        with self.assertRaises(ValidationError):
            days = 365.25 * (constants.MAX_HUMAN_LIFESPAN + 1)
            long_ago = date.today() - timedelta(days=round(days))
            validators.validate_date_of_birth(long_ago)

    def test_adult_dob(self):
        with self.assertRaises(ValidationError):
            days = round(365.25 * constants.AGE_OF_MAJORITY)
            child_dob = date.today() - timedelta(days=round(days))
            validators.validate_adult(child_dob)

    def test_child_dob(self):
        with self.assertRaises(ValidationError):
            days = round(365.25 * constants.AGE_OF_MAJORITY) + 1
            adult_dob = date.today() - timedelta(days=days)
            validators.validate_child(adult_dob)
