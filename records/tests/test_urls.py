from django.test import SimpleTestCase
from django.urls import resolve
from django.utils.module_loading import import_string


class TemperatureRecordsListURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/records/temperature/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("records.views.TemperatureRecordsListView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "records:temperature_records_list")


class TemperatureRecordCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/records/temperature/username/add/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("records.views.TemperatureRecordCreateView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "records:temperature_record_create")
