from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.User = get_user_model()

        # create a normal user
        cls.user = cls.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword",
        )

    def test_user_basic(self):
        self.assertEqual(self.user.username, "AlvinMukuna")
        self.assertEqual(self.user.email, "alvin@mukuna.com")
        self.assertEqual(self.user.phone_number, "+254 701 234 567")

    # class methods
    def test_user_object_name_is_username(self):
        self.assertEqual(self.user.username, str(self.user))

    # email
    def test_email_label(self):
        email__meta = self.user._meta.get_field("email")
        self.assertEqual(email__meta.verbose_name, "email address")

    def test_email_is_null(self):
        email__meta = self.user._meta.get_field("email")
        self.assertFalse(email__meta.null)

    def test_email_is_blank(self):
        email__meta = self.user._meta.get_field("email")
        self.assertFalse(email__meta.blank)

    # first name
    def test_first_name_label(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.verbose_name, "first name")

    def test_first_name_max_length(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.max_length, 150)

    def test_first_name_is_null(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertFalse(first_name__meta.null)

    def test_first_name_is_blank(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertTrue(first_name__meta.blank)

    # last name
    def test_last_name_label(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.verbose_name, "last name")

    def test_last_name_max_length(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.max_length, 150)

    def test_last_name_is_null(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertFalse(last_name__meta.null)

    def test_last_name_is_blank(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertTrue(last_name__meta.blank)

    # phone number
    def test_phone_number_label(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.verbose_name, "phone number")

    def test_phone_number_max_length(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.max_length, 50)

    def test_phone_number_help_text(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(
            phone_number__meta.help_text,
            "Enter a valid phone number that starts with a country code.",
        )

    def test_phone_number_is_null(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertFalse(phone_number__meta.null)

    def test_phone_number_is_blank(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertFalse(phone_number__meta.blank)
