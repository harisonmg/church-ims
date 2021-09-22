from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.pages import LoginPage


class LogoutTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.password = self.fake.password()
        self.user = UserFactory(password=self.password)

    def login(self):
        login_page = LoginPage(self).visit()
        login_page.get_attributes().login(self.user.email, self.password)

    def test_that_a_user_can_logout(self):
        # A logged in user clicks on the logout link on the account dropdown
        self.login()
        self.browser.find_element_by_id("accountDropdownMenu").click()
        self.browser.find_element_by_link_text("Log out").click()

        # He is redirected to the logout page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + "/accounts/logout/"
        )
        self.assertEqual(self.browser.title, f"{self.get_site_name()}")
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Log out")

        logout_form = self.browser.find_element_by_id("logout_form")
        logout_button = logout_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.assertEqual(logout_button.text, "Log out")

        # He clicks on the logout button and is redirected to the home page
        logout_button.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/")
        self.assertEqual(self.browser.title, f"{self.get_site_name()}")
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, self.get_site_name()
        )

        alerts = self.browser.find_elements_by_class_name("alert")
        self.assertEqual(alerts[0].text, "You have signed out.")
