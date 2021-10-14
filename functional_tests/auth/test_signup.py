from django.test import override_settings

from functional_tests import pages
from functional_tests.base import FunctionalTestCase


@override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory")
class SignupTestCase(FunctionalTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_email = cls.fake.email()
        cls.password = cls.fake.password()

    def test_anonymous_user_can_signup(self):
        # A user visits the signup page
        signup_page = pages.SignupPage(self)
        signup_page.visit()

        # She knows he's in the right place because she can see the name
        # of the site in the title and header

        self.assertEqual(signup_page.title, self.SITE_NAME)
        self.assertEqual(signup_page.header.title, self.header_title)
        self.assertEqual(signup_page.heading, "Sign up")

        # She sees the inputs of the signup form, including labels and placeholders.
        # She also sees a link for logging in
        self.assertEqual(signup_page.form.email_label, "E-mail*")
        self.assertEqual(signup_page.form.password_label, "Password*")
        self.assertEqual(
            signup_page.form.password_confirmation_label, "Password (again)*"
        )
        self.assertEqual(signup_page.form.submit_button_label, "Sign up")
        self.assertEqual(signup_page.form.login_link, pages.LoginPage(self).url)

        # She enters her email and password and submits the form
        signup_page.signup(self.user_email, self.password, self.password)

        # The sign up was successful and she is redirected to the email
        # verification page
        email_verification_page = pages.EmailVerificationRequiredPage(self)
        self.assertEqual(self.browser.current_url, email_verification_page.url)

        self.assertEqual(email_verification_page.title, self.SITE_NAME)
        self.assertEqual(email_verification_page.header.title, self.header_title)
        self.assertEqual(email_verification_page.heading, "Verify your email address")

        self.assertEqual(
            email_verification_page.messages[0],
            f"Confirmation e-mail sent to {self.user_email}.",
        )
        self.assertEqual(
            email_verification_page.main_text[0],
            "We have sent an e-mail to you for verification."
            + " Follow the link provided to finalize the signup process."
            + " Please contact us if you do not receive it within a few minutes.",
        )

        # She also receives an email with a link for verifying her email address
        self.assertEqual(len(self.mail.outbox), 1)
        email = self.mail.outbox[0]
        self.assertIn(self.user_email, email.to)
        self.assertIn("To confirm this is correct, go to", email.body)

        url = self.find_url(email.body)
        self.assertIn(self.live_server_url, url)

        # She clicks the link and is taken to the email confirmation page
        self.browser.get(url)
        email_confirmation_page = pages.EmailConfirmationPage(self)

        self.assertEqual(email_confirmation_page.title, self.SITE_NAME)
        self.assertEqual(email_confirmation_page.header.title, self.header_title)
        self.assertEqual(email_confirmation_page.heading, "Confirm email address")

        self.assertEqual(
            email_confirmation_page.main_text[0],
            "Please confirm that {} is an e-mail address for user {}.".format(
                self.user_email, self.user_email.split("@")[0]
            ),
        )

        # She sees an email confirmation button and ascertains that
        # the email can be used on the site
        self.assertEqual(email_confirmation_page.form.submit_button_label, "Confirm")
        email_confirmation_page.confirm_email()

        # The confirmation was successful and she is redirected to the login page
        login_page = pages.LoginPage(self)
        self.assertEqual(self.browser.current_url, login_page.url)
        self.assertEqual(
            login_page.messages[0], f"You have confirmed {self.user_email}."
        )

    def test_invalid_email_confirmation_link(self):
        email_confirmation_page = pages.EmailConfirmationPage(self)
        email_confirmation_page.visit()

        self.assertEqual(email_confirmation_page.heading, "Confirm email address")
        self.assertEqual(
            email_confirmation_page.main_text[0],
            "This e-mail confirmation link expired or is invalid."
            + " Please issue a new e-mail confirmation request.",
        )
