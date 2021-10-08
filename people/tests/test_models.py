from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from people.factories import PersonFactory


class PersonModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory()
        cls.person_meta = cls.person._meta

    def test_db_table(self):
        self.assertEqual(self.person_meta.db_table, "people_person")

    def test_ordering(self):
        self.assertEqual(self.person_meta.ordering, ["username"])

    def test_verbose_name(self):
        self.assertEqual(self.person_meta.verbose_name, "person")

    def test_verbose_name_plural(self):
        self.assertEqual(self.person_meta.verbose_name_plural, "people")

    def test_string_repr(self):
        expected_object_name = self.person.username
        self.assertEqual(str(self.person), expected_object_name)


class PersonModelFieldsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        person = PersonFactory.build()
        cls.person_meta = person._meta


class PersonUsernameTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("username")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 50)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "username")


class PersonFullNameTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("full_name")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 300)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_full_name"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "full name")


class PersonCreatedAtTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("created_at")

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


class PersonLastModifiedTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("last_modified")

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
