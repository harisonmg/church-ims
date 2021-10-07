from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from records.factories import TemperatureRecordFactory
from records.utils import format_temperature


class TemperatureRecordModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.temp_record = TemperatureRecordFactory()
        cls.temp_record_meta = cls.temp_record._meta

    def test_db_table(self):
        self.assertEqual(self.temp_record_meta.db_table, "records_temperature")

    def test_ordering(self):
        self.assertEqual(
            self.temp_record_meta.ordering, ["person__username", "created_at"]
        )

    def test_verbose_name(self):
        self.assertEqual(self.temp_record_meta.verbose_name, "temperature record")

    def test_verbose_name_plural(self):
        self.assertEqual(
            self.temp_record_meta.verbose_name_plural, "temperature records"
        )

    def test_string_repr(self):
        person = self.temp_record.person
        temp = format_temperature(self.temp_record.body_temperature)
        expected_object_name = f"{person} was {temp} at {self.temp_record.created_at}"
        self.assertEqual(str(self.temp_record), expected_object_name)


class TemperatureRecordModelFieldsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        temp_record = TemperatureRecordFactory.build()
        cls.temp_record_meta = temp_record._meta


class TemperatureRecordPersonTestCase(TemperatureRecordModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.temp_record_meta.get_field("person")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_many_to_one(self):
        self.assertTrue(self.field.many_to_one)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model, import_string("people.models.Person")
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "person")


class TemperatureRecordBodyTemperatureTestCase(TemperatureRecordModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.temp_record_meta.get_field("body_temperature")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_decimal_places(self):
        self.assertEqual(self.field.decimal_places, 2)

    def test_help_text(self):
        help_text = "The person's body temperature in degrees celsius."
        self.assertEqual(self.field.help_text, help_text)

    def test_max_digits(self):
        self.assertEqual(self.field.max_digits, 4)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertEqual(
            self.field.validators[0],
            import_string("records.validators.human_body_temperature_validator"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "body temperature")


class TemperatureRecordCreatedAtTestCase(TemperatureRecordModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.temp_record_meta.get_field("created_at")

    def test_auto_now(self):
        self.assertFalse(self.field.auto_now)

    def test_auto_now_add(self):
        self.assertTrue(self.field.auto_now_add)

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "created at")


class TemperatureRecordLastModifiedTestCase(TemperatureRecordModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.temp_record_meta.get_field("last_modified")

    def test_auto_now(self):
        self.assertTrue(self.field.auto_now)

    def test_auto_now_add(self):
        self.assertFalse(self.field.auto_now_add)

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "last modified")
