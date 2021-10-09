from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase


class LoginTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.password = self.fake.password()
        self.active_user = UserFactory(password=self.password)
        self.inactive_user = UserFactory(password=self.password, is_active=False)

    def test_active_user_can_login(self):
        # A user visits the login page
        login_page = pages.LoginPage(self)
        login_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(login_page.title, self.SITE_NAME)
        self.assertEqual(login_page.header.title, self.header_title)
        self.assertEqual(login_page.heading, "Log in")

        # He sees the inputs of the login form, including labels and placeholders.
        # He also sees links for signing up and password reset
        self.assertEqual(login_page.form.email_label, "E-mail*")
        self.assertEqual(login_page.form.password_label, "Password*")
        self.assertEqual(login_page.form.remember_checkbox_label, "Remember Me")
        self.assertEqual(login_page.form.submit_button_label, "Log in")
        self.assertEqual(login_page.form.signup_link, pages.SignupPage(self).url)
        self.assertEqual(
            login_page.form.password_reset_link,
            pages.PasswordResetRequestPage(self).url,
        )

        # He enters his email and password and submits the form
        login_page.login(self.active_user.email, self.password, True)

        # The login was successful and he is redirected to his dashboard
        dashboard = pages.Dashboard(self)
        self.assertEqual(self.browser.current_url, dashboard.url)
        self.assertEqual(
            dashboard.messages.messages[0],
            f"Successfully signed in as {self.active_user.username}.",
        )

    def test_inactive_user_cannot_login(self):
        # An inactive user visits the login page
        login_page = pages.LoginPage(self)
        login_page.visit()

        # He enters his email and password and submits the form
        login_page.login(self.inactive_user.email, self.password)

        # He is redirected to the account inactive page
        account_inactive_page = pages.AccountInactivePage(self)
        self.assertEqual(self.browser.current_url, account_inactive_page.url)

        # He can see the name of the site in the site title and header
        self.assertEqual(account_inactive_page.title, self.SITE_NAME)
        self.assertEqual(account_inactive_page.header.title, self.header_title)
        self.assertEqual(account_inactive_page.heading, "Account inactive")
        self.assertEqual(
            account_inactive_page.main_text[0], "This account is inactive."
        )
