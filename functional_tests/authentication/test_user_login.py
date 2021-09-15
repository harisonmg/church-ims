from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase


class LoginTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.user_password = self.fake.password()
        self.user = UserFactory(password=self.user_password)

    def test_that_a_user_can_login(self):
        # A user visits the home page
        self.browser.get(self.live_server_url)

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

        login_link, signup_link = cta_buttons

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
        # of the login form, including labels and placeholders
        self.assertEqual(
            self.browser.find_element_by_css_selector("h1").text, "Log in"
        )

        login_form = self.browser.find_element_by_id("login_form")

        email_input = login_form.find_element_by_css_selector("input#id_email")
        self.assertEqual(
            login_form.find_element_by_css_selector('label[for="id_email"]').text,
            "Email address",
        )

        password_input = login_form.find_element_by_css_selector("input#id_password")
        self.assertEqual(
            login_form.find_element_by_css_selector('label[for="id_password"]').text,
            "Password",
        )

        # He enters his email and password and clicks the login button
        # to log in to the resource center.
        email_input.send_keys(self.user.email)
        password_input.send_keys(self.user_password)
        login_form.find_element_by_css_selector('button[type="submit"]').click()

        # The login was successful and he is redirected to his dashboard
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/dashboard/"
        )
