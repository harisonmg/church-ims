from datetime import date, timedelta

from django.test import SimpleTestCase

from people.utils import get_age


class GetAgeTestCase(SimpleTestCase):
    def test_birth_day_minus_one_day(self):
        days_lived = round(365.25 * 1) - 1
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(get_age(dob), 0)

    def test_birth_day(self):
        days_lived = round(365.25 * 1)
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(get_age(dob), 1)
