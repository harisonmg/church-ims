from django.contrib.auth import get_user_model
from django.test import TestCase

from people.models import Person


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
            password="alvinpassword"
        )

        cls.person = Person.objects.create(
            username="AlvinMukuna",
            full_name="Alvin Mukuna",
            dob="1984-12-12",
            gender="M",
            created_by=cls.user,
        )
        cls.user.profile = cls.person
        cls.user.save()

    def test_user_basic(self):
        self.assertEqual(self.user.username, "AlvinMukuna")
        self.assertEqual(self.user.email, "alvin@mukuna.com")
        self.assertEqual(self.user.phone_number,"+254 701 234 567")
        self.assertEqual(self.user.profile, self.person)

    # class methods
    def test_user_object_name_is_username(self):
        self.assertEqual(self.user.username, str(self.user))


    # email
    def test_email_label(self):
        email__meta = self.user._meta.get_field("email")
        self.assertEqual(email__meta.verbose_name, "email address")

    def test_email_can_not_save_NULL_in_the_database(self):
        email__meta = self.user._meta.get_field("email")
        self.assertEqual(email__meta.null, False)

    def test_email_is_not_allowed_to_be_blank(self):
        email__meta = self.user._meta.get_field("email")
        self.assertEqual(email__meta.blank, False)

    # first name
    def test_first_name_label(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.verbose_name, "first name")

    def test_first_name_max_length(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.max_length, 150)

    def test_first_name_can_not_save_NULL_in_the_database(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.null, False)

    def test_first_name_is_allowed_to_be_blank(self):
        first_name__meta = self.user._meta.get_field("first_name")
        self.assertEqual(first_name__meta.blank, True)

    # last name
    def test_last_name_label(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.verbose_name, "last name")

    def test_last_name_max_length(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.max_length, 150)

    def test_last_name_can_not_save_NULL_in_the_database(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.null, False)

    def test_last_name_is_allowed_to_be_blank(self):
        last_name__meta = self.user._meta.get_field("last_name")
        self.assertEqual(last_name__meta.blank, True)

    # phone number
    def test_phone_number_label(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.verbose_name, "phone number")

    def test_phone_number_max_length(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.max_length, 20)

    def test_phone_number_help_text(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.help_text, "Enter a valid phone number")

    def test_phone_number_can_not_save_NULL_in_the_database(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.null, False)

    def test_phone_number_is_not_allowed_to_be_blank(self):
        phone_number__meta = self.user._meta.get_field("phone_number")
        self.assertEqual(phone_number__meta.blank, False)

    # profile
    def test_profile_label(self):
        profile__meta = self.user._meta.get_field("profile")
        self.assertEqual(profile__meta.verbose_name, "personal details")

    def test_profile_max_length(self):
        profile__meta = self.user._meta.get_field("profile")
        self.assertIsNone(profile__meta.max_length)

    def test_profile_can_save_NULL_in_the_database(self):
        profile__meta = self.user._meta.get_field("profile")
        self.assertEqual(profile__meta.null, True)

    def test_profile_is_allowed_to_be_blank(self):
        profile__meta = self.user._meta.get_field("profile")
        self.assertEqual(profile__meta.blank, True)
