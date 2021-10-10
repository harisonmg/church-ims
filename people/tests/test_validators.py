from datetime import date, timedelta
from unittest import TestCase

from django.core.exceptions import ValidationError

from people import validators
from people.constants import MAX_HUMAN_AGE
from people.factories import PersonFactory


class ValidateFullNameTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory.build()

    def test_one_name(self):
        with self.assertRaisesRegex(
            ValidationError, validators.INVALID_FULL_NAME_ERROR
        ):
            validators.validate_full_name(self.person.username)

    def test_one_name_with_leading_space(self):
        with self.assertRaisesRegex(
            ValidationError, validators.INVALID_FULL_NAME_ERROR
        ):
            validators.validate_full_name(f" {self.person.username}")

    def test_one_name_with_trailing_space(self):
        with self.assertRaisesRegex(
            ValidationError, validators.INVALID_FULL_NAME_ERROR
        ):
            validators.validate_full_name(f"{self.person.username} ")


class ValidateDateOfBirthTestCase(TestCase):
    def test_date_in_future(self):
        with self.assertRaisesRegex(ValidationError, validators.DOB_IN_FUTURE_ERROR):
            tomorrow = date.today() + timedelta(days=1)
            validators.validate_date_of_birth(tomorrow)

    def test_date_in_distant_past(self):
        with self.assertRaisesRegex(
            ValidationError, validators.DOB_IN_DISTANT_PAST_ERROR
        ):
            days_lived = 365.25 * (MAX_HUMAN_AGE + 1)
            long_ago = date.today() - timedelta(days=round(days_lived))
            validators.validate_date_of_birth(long_ago)
