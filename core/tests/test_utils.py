from datetime import date, timedelta

from django.test import SimpleTestCase

from core import utils


class CoreUtilsTestCase(SimpleTestCase):
    def test_age_birthday_minus_one_day(self):
        days = round(365.25 * 1) - 1
        zero_years = date.today() - timedelta(days=days)
        self.assertEqual(utils.get_age(zero_years), 0)

    def test_age_birthday(self):
        days = round(365.25 * 1)
        one_year = date.today() - timedelta(days=days)
        self.assertEqual(utils.get_age(one_year), 1)
