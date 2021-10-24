from django.test import SimpleTestCase, TestCase
from django.utils.module_loading import import_string

from accounts.factories import UserFactory
from people.utils import get_personal_details


class UserModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.user_meta = cls.user._meta

    def test_db_table(self):
        self.assertEqual(self.user_meta.db_table, "accounts_user")

    def test_ordering(self):
        self.assertEqual(self.user_meta.ordering, ["email"])

    def test_verbose_name(self):
        self.assertEqual(self.user_meta.verbose_name, "user")

    def test_verbose_name_plural(self):
        self.assertEqual(self.user_meta.verbose_name_plural, "users")

    def test_string_repr(self):
        expected_object_name = self.user.username
        self.assertEqual(str(self.user), expected_object_name)

    def test_personal_details(self):
        self.assertEqual(self.user.personal_details, get_personal_details(self.user))


class UserModelFieldsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory.build()
        cls.user_meta = cls.user._meta


class UserUsernameTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("username")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_error_messages(self):
        error_messages = {"unique": "A user with that username already exists."}
        self.assertDictContainsSubset(error_messages, self.field.error_messages)

    def test_help_text(self):
        help_text = (
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
        self.assertEqual(self.field.help_text, help_text)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

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

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "username")


class UserEmailTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("email")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 254)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_unique(self):
        self.assertFalse(self.field.unique)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "email address")


class UserPasswordTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("password")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 128)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "password")


class UserFirstNameTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("first_name")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "first name")


class UserLastNameTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("last_name")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_max_length(self):
        self.assertEqual(self.field.max_length, 150)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "last name")


class UserIsSuperUserTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("is_superuser")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_default(self):
        self.assertEqual(self.field.default, False)

    def test_help_text(self):
        help_text = "Designates that this user has all permissions without"
        help_text += " explicitly assigning them."
        self.assertEqual(self.field.help_text, help_text)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "superuser status")


class UserIsStaffTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("is_staff")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_default(self):
        self.assertEqual(self.field.default, False)

    def test_help_text(self):
        help_text = "Designates whether the user can log into this admin site."
        self.assertEqual(self.field.help_text, help_text)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "staff status")


class UserIsActiveTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("is_active")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_default(self):
        self.assertEqual(self.field.default, True)

    def test_help_text(self):
        help_text = "Designates whether this user should be treated as active."
        help_text += " Unselect this instead of deleting accounts."
        self.assertEqual(self.field.help_text, help_text)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "active")


class UserDateJoinedTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("date_joined")

    def test_blank(self):
        self.assertFalse(self.field.blank)

    def test_default(self):
        self.assertEqual(self.field.default, import_string("django.utils.timezone.now"))

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "date joined")


class UserLastLoginTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("last_login")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_null(self):
        self.assertTrue(self.field.null)

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "last login")


class UserGroupsTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("groups")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_help_text(self):
        help_text = "The groups this user belongs to."
        help_text += " A user will get all permissions granted to each of their groups."
        self.assertEqual(self.field.help_text, help_text)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_many_to_many(self):
        self.assertTrue(self.field.many_to_many)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model, import_string("django.contrib.auth.models.Group")
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "groups")


class UserPermissionsTestCase(UserModelFieldsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.field = cls.user_meta.get_field("user_permissions")

    def test_blank(self):
        self.assertTrue(self.field.blank)

    def test_help_text(self):
        help_text = "Specific permissions for this user."
        self.assertEqual(self.field.help_text, help_text)

    def test_is_relation(self):
        self.assertTrue(self.field.is_relation)

    def test_many_to_many(self):
        self.assertTrue(self.field.many_to_many)

    def test_null(self):
        self.assertFalse(self.field.null)

    def test_related_model(self):
        self.assertEqual(
            self.field.related_model,
            import_string("django.contrib.auth.models.Permission"),
        )

    def test_verbose_name(self):
        self.assertEqual(self.field.verbose_name, "user permissions")
