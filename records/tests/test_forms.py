from django.test import SimpleTestCase
from django.utils.module_loading import import_string

from records.forms import TemperatureRecordForm


class TemperatureRecordFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = TemperatureRecordForm()

    def test_parent_class(self):
        self.assertIsInstance(self.form, import_string("django.forms.ModelForm"))

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(["body_temperature"], list(fields))

    def test_body_temperature_validators(self):
        body_temperature_field = self.form.fields.get("body_temperature")
        self.assertEqual(len(body_temperature_field.validators), 3)
        self.assertIsInstance(
            body_temperature_field.validators[0],
            import_string("django.core.validators.MaxValueValidator"),
        )
        self.assertIsInstance(
            body_temperature_field.validators[1],
            import_string("django.core.validators.MinValueValidator"),
        )
        self.assertIsInstance(
            body_temperature_field.validators[2],
            import_string("django.core.validators.DecimalValidator"),
        )
