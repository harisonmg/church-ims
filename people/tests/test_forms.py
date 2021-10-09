from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from people.constants import GENDER_CHOICES
from people.factories import PersonFactory
from people.forms import PersonForm
from people.validators import INVALID_FULL_NAME_ERROR


class PersonFormTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = PersonForm()

    def test_parent_class(self):
        self.assertIsInstance(self.form, import_string("django.forms.ModelForm"))

    def test_fields(self):
        fields = self.form.fields.keys()
        self.assertEqual(list(fields), ["username", "full_name", "gender", "dob"])


class PersonFormFieldsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.form = PersonForm
        cls.form_fields = cls.form().fields
        cls.person = PersonFactory.build()
        cls.data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }


class PersonUsernameTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("username")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 25)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.contrib.auth.validators.UnicodeUsernameValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_non_unique_value(self):
        # setup
        person = PersonFactory()
        data = self.data.copy()
        data["username"] = person.username

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"username": ["Person with this Username already exists."]}
        self.assertEqual(form.errors, errors)

    def test_value_with_spaces(self):
        # setup
        data = self.data.copy()
        data["username"] = data["full_name"]

        # test
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        username_error = "Enter a valid username. This value may contain only letters, "
        username_error += "numbers, and @/./+/-/_ characters."
        self.assertEqual(form.errors, {"username": [username_error]})


class PersonFullNameTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.field = cls.form_fields.get("full_name")

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_required(self):
        self.assertTrue(self.field.required)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 3)
        self.assertEqual(
            self.field.validators[0],
            import_string("people.validators.validate_full_name"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )
        self.assertIsInstance(
            self.field.validators[2],
            import_string("django.core.validators.ProhibitNullCharactersValidator"),
        )

    def test_value_with_one_name(self):
        data = self.data.copy()
        data["full_name"] = data["username"]
        form = self.form(data=data)
        self.assertFalse(form.is_valid())
        errors = {"full_name": [INVALID_FULL_NAME_ERROR]}
        self.assertEqual(form.errors, errors)


class PersonGenderTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("gender")

    def test_choices(self):
        none_option = [("", "---------")]
        self.assertEqual(self.field.choices, none_option + GENDER_CHOICES)

    def test_required(self):
        self.assertTrue(self.field.required)


class PersonDOBTestCase(PersonFormFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.form_fields.get("dob")

    def test_required(self):
        self.assertTrue(self.field.required)
