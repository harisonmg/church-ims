from datetime import date, timedelta
from random import randint
from unittest import TestCase

from people import constants, utils


class GetAgeTestCase(TestCase):
    def test_birth_day_minus_one_day(self):
        days_lived = round(365.25 * 1) - 1
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(utils.get_age(dob), 0)

    def test_birth_day(self):
        days_lived = round(365.25 * 1)
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(utils.get_age(dob), 1)


class GetAgeGroupTestCase(TestCase):
    def test_negative_age(self):
        with self.assertRaisesRegex(ValueError, utils.NEGATIVE_AGE_ERROR):
            utils.get_age_category(-1)

    def test_child(self):
        age = randint(0, constants.TEENAGE[0] - 1)
        self.assertEqual(utils.get_age_category(age), "child")

    def test_teenager(self):
        age = randint(*constants.TEENAGE)
        self.assertEqual(utils.get_age_category(age), "teenager")

    def test_young_adult(self):
        age = randint(*constants.YOUNG_ADULTHOOD)
        self.assertEqual(utils.get_age_category(age), "young adult")

    def test_adult(self):
        age = randint(constants.YOUNG_ADULTHOOD[1] + 1, constants.MIDDLE_AGE[0] - 1)
        self.assertEqual(utils.get_age_category(age), "adult")

    def test_middle_aged(self):
        age = randint(*constants.MIDDLE_AGE)
        self.assertEqual(utils.get_age_category(age), "middle-aged")

    def test_senior_citizen(self):
        age = randint(constants.AGE_OF_SENIORITY + 1, constants.MAX_HUMAN_AGE)
        self.assertEqual(utils.get_age_category(age), "senior citizen")

    def test_max_human_age_exceeded(self):
        with self.assertRaisesRegex(ValueError, utils.MAX_HUMAN_AGE_EXCEEDED_ERROR):
            utils.get_age_category(constants.MAX_HUMAN_AGE + 1)
