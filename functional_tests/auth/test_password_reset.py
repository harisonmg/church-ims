from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages


class PasswordResetTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.user = UserFactory()
        self.password = self.fake.password()

    def test_registered_user_can_reset_their_password(self):
        # A user visits the password reset request page
        password_reset_request_page = pages.PasswordResetRequestPage(self)
        password_reset_request_page.visit()

        # She knows he's in the right place because she can see the name
        # of the site in the site title and header
        self.assertEqual(password_reset_request_page.title, self.SITE_NAME)
        self.assertEqual(
            password_reset_request_page.header.title,
            self.header_title,
        )
        self.assertEqual(password_reset_request_page.heading, "Password reset")

        self.assertEqual(
            password_reset_request_page.main_text[0],
            "Forgotten your password? Enter your e-mail address below,"
            + " and we'll send you an e-mail allowing you to reset it.",
        )

        # She sees the inputs of the password reset request form,
        # including labels and placeholders
        self.assertEqual(password_reset_request_page.form.email_label, "E-mail*")
        self.assertEqual(
            password_reset_request_page.form._submit_button.text, "Reset my password"
        )

        # She enters her email and submits the form
        password_reset_request_page.request_password_reset(self.user.email)

        # She is redirected to the password reset request done page
        # and receives an email with instructions for resetting her password
        password_reset_request_done_page = pages.PasswordResetRequestDonePage(self)
        self.assertEqual(self.browser.current_url, password_reset_request_done_page.url)
        self.assertEqual(password_reset_request_done_page.title, self.SITE_NAME)
        self.assertEqual(
            password_reset_request_done_page.header.title,
            self.header_title,
        )
        self.assertEqual(password_reset_request_done_page.heading, "Password reset")

        self.assertEqual(
            password_reset_request_done_page.main_text[0],
            "We have sent you an e-mail. Please contact us if you do not receive it"
            + " within a few minutes.",
        )

        self.assertEqual(len(self.mail.outbox), 1)
        email = self.mail.outbox[0]
        self.assertIn(self.user.email, email.to)
        self.assertIn("Click the link below to reset your password", email.body)

        # The email has a password reset link
        url = self.find_url(email.body)
        self.assertIn(self.live_server_url, url)

        # She clicks the link and is taken to the password reset page
        self.browser.get(url)
        password_reset_page = pages.PasswordResetPage(self)
        self.assertEqual(password_reset_page.title, self.SITE_NAME)
        self.assertEqual(password_reset_page.header.title, self.header_title)
        self.assertEqual(password_reset_page.heading, "Change password")

        # She sees the inputs of the password change form,
        # including labels and placeholders
        self.assertEqual(password_reset_page.form.password_label, "New Password*")
        self.assertEqual(
            password_reset_page.form.password_confirmation_label,
            "New Password (again)*",
        )
        self.assertEqual(
            password_reset_page.form._submit_button.text, "Change password"
        )

        # She enters a new password and submits the form
        password_reset_page.set_password(self.password, self.password)

        # The password reset is successful and she is redirected
        # to the password reset done page
        password_reset_done_page = pages.PasswordResetDonePage(self)
        self.assertEqual(self.browser.current_url, password_reset_done_page.url)
        self.assertEqual(password_reset_done_page.title, self.SITE_NAME)
        self.assertEqual(password_reset_done_page.header.title, self.header_title)
        self.assertEqual(password_reset_done_page.heading, "Password reset complete")

        self.assertEqual(
            password_reset_done_page.messages.messages[0],
            "Password successfully changed.",
        )
        self.assertEqual(
            password_reset_done_page.main_text[0],
            "You can now log in with your new password.",
        )
        self.assertEqual(password_reset_done_page.login_link, pages.LoginPage(self).url)
