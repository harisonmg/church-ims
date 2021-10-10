from django.test import SimpleTestCase
from django.utils.module_loading import import_string

from records import constants
from records.forms import TemperatureRecordForm


class TemperatureRecordFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = TemperatureRecordForm()

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(["body_temperature"], list(fields))


class TemperatureRecordFormFieldsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = TemperatureRecordForm
        cls.form_fields = cls.form().fields


class TemperatureRecordBodyTemperatureTestCase(TemperatureRecordFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("body_temperature")

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.core.validators.MaxValueValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MinValueValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.DecimalValidator"),
        )

    def test_value_above_max(self):
        data = {"body_temperature": constants.MAX_HUMAN_BODY_TEMP + 1}
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {
            "body_temperature": ["Ensure this value is less than or equal to 45."]
        }
        self.assertEqual(form.errors, errors)

    def test_value_below_min(self):
        data = {"body_temperature": constants.MIN_HUMAN_BODY_TEMP - 1}
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {
            "body_temperature": ["Ensure this value is greater than or equal to 30."]
        }
        self.assertEqual(form.errors, errors)
