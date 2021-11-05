from datetime import timedelta

from django.test import TestCase

from accounts.factories import UserFactory
from people.factories import PersonFactory
from records.factories import TemperatureRecordFactory
from records.utils import is_duplicate_temp_record


class IsDuplicateTemperatureRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.temp_record = TemperatureRecordFactory(created_by=cls.user)
        cls.data = {
            "person": cls.temp_record.person,
            "body_temperature": cls.temp_record.body_temperature,
            "created_at": cls.temp_record.created_at,
        }

    def test_exact_duplicate(self):
        temp_record = TemperatureRecordFactory.build(**self.data)
        self.assertTrue(is_duplicate_temp_record(temp_record))

    def test_different_body_temperature(self):
        data = self.data.copy()
        data.pop("body_temperature")
        temp_record = TemperatureRecordFactory.build(**data)
        self.assertTrue(is_duplicate_temp_record(temp_record))

    def test_different_creator(self):
        data = self.data.copy()
        data["created_by"] = UserFactory()
        temp_record = TemperatureRecordFactory.build(**data)
        self.assertTrue(is_duplicate_temp_record(temp_record))

    def test_different_date(self):
        data = self.data.copy()
        data["created_at"] = data["created_at"] - timedelta(days=1)
        temp_record = TemperatureRecordFactory.build(**data)
        self.assertFalse(is_duplicate_temp_record(temp_record))

    def test_null_date(self):
        data = self.data.copy()
        data.pop("created_at")
        temp_record = TemperatureRecordFactory.build(**data)
        self.assertIsNone(temp_record.created_at)
        self.assertTrue(is_duplicate_temp_record(temp_record))

    def test_not_duplicate(self):
        data = self.data.copy()
        data["person"] = PersonFactory()
        temp_record = TemperatureRecordFactory.build(**data)
        self.assertFalse(is_duplicate_temp_record(temp_record))
