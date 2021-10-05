from django.test import SimpleTestCase
from django.urls import resolve


class TemperatureRecordsListURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/records/temperature/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "TemperatureRecordsListView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "records:temperature_records_list")


class TemperatureRecordCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/records/temperature/username/add/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "TemperatureRecordCreateView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "records:temperature_record_create")
