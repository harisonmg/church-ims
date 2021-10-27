from datetime import date, timedelta
from random import randint

from django.test import SimpleTestCase, TestCase

from accounts.factories import UserFactory
from people import utils
from people.constants import AGE_OF_MAJORITY, MAX_HUMAN_AGE
from people.factories import AdultFactory


class GetAgeTestCase(SimpleTestCase):
    def test_birth_day_minus_one_day(self):
        days_lived = round(365.25 * 1) - 1
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(utils.get_age(dob), 0)

    def test_birth_day(self):
        days_lived = round(365.25 * 1)
        dob = date.today() - timedelta(days=days_lived)
        self.assertEqual(utils.get_age(dob), 1)


class GetTodaysAdultDOBTestCase(SimpleTestCase):
    def test_age(self):
        dob = utils.get_todays_adult_dob()
        self.assertEqual(utils.get_age(dob), AGE_OF_MAJORITY)


class GetAgeGroupTestCase(SimpleTestCase):
    def test_negative_age(self):
        with self.assertRaisesRegex(ValueError, utils.NEGATIVE_AGE_ERROR):
            utils.get_age_category(-1)

    def test_child_start(self):
        self.assertEqual(utils.get_age_category(utils.CHILD[0]), "child")

    def test_child(self):
        age = randint(*utils.CHILD)
        self.assertEqual(utils.get_age_category(age), "child")

    def test_child_end(self):
        self.assertEqual(utils.get_age_category(utils.CHILD[1]), "child")

    def test_teenager_start(self):
        self.assertEqual(utils.get_age_category(utils.TEENAGER[0]), "teenager")

    def test_teenager(self):
        age = randint(*utils.TEENAGER)
        self.assertEqual(utils.get_age_category(age), "teenager")

    def test_teenager_end(self):
        self.assertEqual(utils.get_age_category(utils.TEENAGER[1]), "teenager")

    def test_young_adult_start(self):
        self.assertEqual(utils.get_age_category(utils.YOUNG_ADULT[0]), "young adult")

    def test_young_adult(self):
        age = randint(*utils.YOUNG_ADULT)
        self.assertEqual(utils.get_age_category(age), "young adult")

    def test_young_adult_end(self):
        self.assertEqual(utils.get_age_category(utils.YOUNG_ADULT[1]), "young adult")

    def test_adult_start(self):
        self.assertEqual(utils.get_age_category(utils.ADULT[0]), "adult")

    def test_adult(self):
        age = randint(*utils.ADULT)
        self.assertEqual(utils.get_age_category(age), "adult")

    def test_adult_end(self):
        self.assertEqual(utils.get_age_category(utils.ADULT[1]), "adult")

    def test_middle_aged_start(self):
        self.assertEqual(utils.get_age_category(utils.MIDDLE_AGED[0]), "middle-aged")

    def test_middle_aged(self):
        age = randint(*utils.MIDDLE_AGED)
        self.assertEqual(utils.get_age_category(age), "middle-aged")

    def test_middle_aged_end(self):
        self.assertEqual(utils.get_age_category(utils.MIDDLE_AGED[1]), "middle-aged")

    def test_senior_citizen_start(self):
        self.assertEqual(
            utils.get_age_category(utils.SENIOR_CITIZEN[0]), "senior citizen"
        )

    def test_senior_citizen(self):
        age = randint(*utils.SENIOR_CITIZEN)
        self.assertEqual(utils.get_age_category(age), "senior citizen")

    def test_senior_citizen_end(self):
        self.assertEqual(
            utils.get_age_category(utils.SENIOR_CITIZEN[1]), "senior citizen"
        )

    def test_max_human_age_exceeded(self):
        with self.assertRaisesRegex(ValueError, utils.MAX_HUMAN_AGE_EXCEEDED_ERROR):
            utils.get_age_category(MAX_HUMAN_AGE + 1)


class GetPersonalDetailsTestCase(TestCase):
    def test_personal_details(self):
        user = UserFactory()
        person = AdultFactory(user=user)
        self.assertEqual(utils.get_personal_details(user), person)

    def test_non_existent_personal_details(self):
        user = UserFactory()
        self.assertEqual(utils.get_personal_details(user), None)
