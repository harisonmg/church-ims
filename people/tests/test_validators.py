from unittest import TestCase

from people.factories import PersonFactory
from people import validators


class FullNameValidatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory.build()

    def test_one_name(self):
        with self.assertRaisesRegex(ValueError, validators.INVALID_FULL_NAME_ERROR):
            validators.full_name_validator(self.person.username)

    def test_one_name_with_leading_space(self):
        with self.assertRaisesRegex(ValueError, validators.INVALID_FULL_NAME_ERROR):
            validators.full_name_validator(f" {self.person.username}")

    def test_one_name_with_trailing_space(self):
        with self.assertRaisesRegex(ValueError, validators.INVALID_FULL_NAME_ERROR):
            validators.full_name_validator(f"{self.person.username} ")

    def test_valid_full_name(self):
        result = validators.full_name_validator(self.person.full_name)
        self.assertEqual(result, None)
