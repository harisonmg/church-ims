from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase

from .pages import LoginPage


class LoginTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.password = self.fake.password()

    def test_that_a_user_can_login(self):
        # A user visits the home page
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, self.get_site_name()
        )

        # He knows he's in the right place because he can see the name
        # of the site in the navigation bar
        self.assertEqual(
            self.browser.find_element_by_css_selector("header > a").text,
            self.get_site_name(),
        )

        # He sees two call-to-action buttons, which are links for
        # the sign up and login pages.
        cta_buttons = self.browser.find_elements_by_css_selector("main .btn")
        self.assertEqual(len(cta_buttons), 2)

        signup_link, login_link = cta_buttons

        self.assertEqual("Sign up", signup_link.text)
        self.assertEqual("Log in", login_link.text)
        self.assertEqual(
            signup_link.get_attribute("href"),
            self.live_server_url + "/accounts/signup/",
        )
        self.assertEqual(
            login_link.get_attribute("href"), self.live_server_url + "/accounts/login/"
        )

        # He has an account and therefore decides to login
        login_link.click()

        # He is redirected to the login page, where he sees the inputs
        # of the login form, including labels and placeholders.
        # He also sees links for signing up and password reset
        login_page = LoginPage(self).get_attributes()

        # He enters his email and password and clicks the login button
        user = UserFactory(password=self.password)
        login_page.login(user.email, self.password)

        # The login was successful and he is redirected to his dashboard
        self.assertEqual(self.browser.current_url, self.live_server_url + "/dashboard/")
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Dashboard")

        sidebar_navigation = self.browser.find_element_by_id("sidebarMenu")
        dashboard_link = sidebar_navigation.find_element_by_link_text("Dashboard")
        self.assertIn("active", dashboard_link.get_attribute("class"))

        alerts = self.browser.find_elements_by_class_name("alert")
        self.assertEqual(alerts[0].text, f"Successfully signed in as {user.username}.")

    def test_that_an_inactive_user_cannot_login(self):
        # An inactive user visits the login page
        user = UserFactory(password=self.password, is_active=False)
        self.browser.get(self.live_server_url + "/accounts/login/")

        # He sees the inputs of the login form, including labels and placeholders
        login_page = LoginPage(self).get_attributes()

        # He enters his email and password and clicks the login button
        login_page.login(user.email, self.password)

        # He is redirected to the account inactive page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + "/accounts/inactive/"
        )
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_css_selector("h1").text, "Account inactive"
        )
