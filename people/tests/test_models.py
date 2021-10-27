from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from people.constants import (
    AGE_OF_MAJORITY,
    GENDER_CHOICES,
    INTERPERSONAL_RELATIONSHIP_CHOICES,
)
from people.factories import InterpersonalRelationshipFactory, PersonFactory
from people.utils import get_age, get_age_category


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

    def test_age(self):
        self.assertEqual(self.person.age, get_age(self.person.dob))

    def test_age_category(self):
        self.assertEqual(self.person.age_category, get_age_category(self.person.age))

    def test_is_adult(self):
        self.assertEqual(self.person.is_adult, self.person.age >= AGE_OF_MAJORITY)


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

    def test_error_messages(self):
        self.assertEqual(
            self.field.error_messages.get("unique"),
            "A person with that username already exists.",
        )

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 50)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_unique(self):
        self.assertTrue(self.field.unique)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.contrib.auth.validators.UnicodeUsernameValidator"),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )

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


class PersonGenderTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("gender")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_choices(self):
        self.assertEqual(self.field.choices, GENDER_CHOICES)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 1)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 1)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.core.validators.MaxLengthValidator"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "gender")


class PersonDOBTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("dob")

    def test_auto_now(self):
        self.assertFalse(self.field.auto_now)

    def test_auto_now_add(self):
        self.assertFalse(self.field.auto_now_add)

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "date of birth")


class PersonPhoneNumberTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("phone_number")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_class(self):
        self.assertEqual(self.field.__class__.__name__, "PhoneNumberField")
        self.assertIsInstance(
            self.field, import_string("phonenumber_field.modelfields.PhoneNumberField")
        )

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 128)

    def test_null(self):
        self.assertTrue(self.field.null)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 2)
        self.assertEqual(
            self.field.validators[0],
            import_string(
                "phonenumber_field.validators.validate_international_phonenumber"
            ),
        )
        self.assertIsInstance(
            self.field.validators[1],
            import_string("django.core.validators.MaxLengthValidator"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "phone number")


class PersonUserTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("user")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_help_text(self):
        help_text = "This person's user account."
        self.assertEqual(self.field.help_text, help_text)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_one_to_one(self):
        self.assertTrue(self.field.one_to_one)

    def test_null(self):
        self.assertTrue(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model, import_string("accounts.models.User")
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "user")


class PersonCreatedByTestCase(PersonModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.person_meta.get_field("created_by")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_help_text(self):
        help_text = "The user who created this record."
        self.assertEqual(self.field.help_text, help_text)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_many_to_one(self):
        self.assertTrue(self.field.many_to_one)

    def test_null(self):
        self.assertTrue(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model, import_string("accounts.models.User")
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "created by")


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


class InterpersonalRelationshipModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.relationship = InterpersonalRelationshipFactory()
        cls.relationship_meta = cls.relationship._meta

    def test_constraints(self):
        self.assertEqual(len(self.relationship_meta.constraints), 1)
        self.assertIsInstance(
            self.relationship_meta.constraints[0],
            import_string("django.db.models.UniqueConstraint"),
        )

    def test_db_table(self):
        self.assertEqual(self.relationship_meta.db_table, "people_relationship")

    def test_ordering(self):
        self.assertEqual(self.relationship_meta.ordering, ["person__username"])

    def test_verbose_name(self):
        self.assertEqual(
            self.relationship_meta.verbose_name, "interpersonal relationship"
        )

    def test_verbose_name_plural(self):
        self.assertEqual(
            self.relationship_meta.verbose_name_plural, "interpersonal relationships"
        )

    def test_string_repr(self):
        people = f"{self.relationship.person} and {self.relationship.relative}"
        relation = self.relationship.get_relation_display().lower()
        expected_object_name = f"{people} have a {relation} relationship"
        self.assertEqual(str(self.relationship), expected_object_name)


class InterpersonalRelationshipModelFieldsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        InterpersonalRelationship = InterpersonalRelationshipFactory.build()
        cls.relationship_meta = InterpersonalRelationship._meta


class InterpersonalRelationshipIDTestCase(InterpersonalRelationshipModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("id")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_class_name(self):
        self.assertEqual(self.field.__class__.__name__, "UUIDField")

    def test_default(self):
        self.assertEqual(self.field.default, import_string("uuid.uuid4"))

    def test_editable(self):
        self.assertFalse(self.field.editable)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_primary_key(self):
        self.assertTrue(self.field.primary_key)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "ID")


class InterpersonalRelationshipPersonTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("person")

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


class InterpersonalRelationshipRelativeTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("relative")

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
        self.assertEqual(self.field.verbose_name, "relative")


class InterpersonalRelationshipRelationTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("relation")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_choices(self):
        self.assertEqual(self.field.choices, INTERPERSONAL_RELATIONSHIP_CHOICES)

    def test_help_text(self):
        help_text = "How the person and the relative are associated."
        self.assertEqual(self.field.help_text, help_text)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 2)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_validators(self):
        self.assertEqual(len(self.field.validators), 1)
        self.assertIsInstance(
            self.field.validators[0],
            import_string("django.core.validators.MaxLengthValidator"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "relation")


class InterpersonalRelationshipCreatedByTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("created_by")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_help_text(self):
        help_text = "The user who created this record."
        self.assertEqual(self.field.help_text, help_text)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_many_to_one(self):
        self.assertTrue(self.field.many_to_one)

    def test_null(self):
        self.assertTrue(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model, import_string("accounts.models.User")
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "created by")


class InterpersonalRelationshipCreatedAtTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("created_at")

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


class InterpersonalRelationshipLastModifiedTestCase(
    InterpersonalRelationshipModelFieldsTestCase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.relationship_meta.get_field("last_modified")

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
