from datetime import date, timedelta
from unittest import TestCase

from django.core.exceptions import ValidationError

from people import validators
from people.constants import MAX_HUMAN_AGE
from people.factories import PersonFactory
from people.utils import get_todays_adult_dob


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


class ValidateAdultTestCase(TestCase):
    def test_child_dob(self):
        error_message = f"Date of birth must be before {get_todays_adult_dob()}"
        with self.assertRaisesRegex(ValidationError, error_message):
            child_dob = get_todays_adult_dob() + timedelta(days=1)
            validators.validate_adult(child_dob)


class ValidateChildTestCase(TestCase):
    def test_child_dob(self):
        error_message = f"Date of birth must be after {get_todays_adult_dob()}"
        with self.assertRaisesRegex(ValidationError, error_message):
            adult_dob = get_todays_adult_dob() - timedelta(days=1)
            validators.validate_child(adult_dob)


class ValidatePersonUsernameTestCase(TestCase):
    def test_non_existent_username(self):
        username = "does-not-exist"
        error_message = validators.PERSON_DOES_NOT_EXIST_ERROR % dict(username=username)
        with self.assertRaisesRegex(ValidationError, error_message):
            validators.validate_person_username(username)
