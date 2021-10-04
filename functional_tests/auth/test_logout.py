from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages


class LogoutTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.password = self.fake.password()
        self.user = UserFactory(password=self.password)
        self.login()

    def login(self):
        login_page = pages.LoginPage(self)
        login_page.visit()
        login_page.login(self.user.email, self.password)

    def test_authenticated_user_can_logout(self):
        # A user visits the logout page
        logout_page = pages.LogoutPage(self)
        logout_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(logout_page.title, self.SITE_NAME)
        self.assertEqual(logout_page.header.title, self.header_title)
        self.assertEqual(logout_page.heading, "Log out")

        # The site header an account dropdown menu as well
        logout_page.header.toggle_account_dropdown()
        self.assertEqual(
            logout_page.header.account_dropdown.links, self.account_dropdown_links
        )

        # He sees a logout confirmation button and ascertains that he wants to log out
        self.assertEqual(logout_page.main_text[0], "Are you sure you want to log out?")
        self.assertEqual(logout_page.form._submit_button.text, "Log out")
        logout_page.logout()

        # The logout was successful and he is redirected to the home page
        home_page = pages.HomePage(self)
        self.assertEqual(self.browser.current_url, home_page.url)
        self.assertEqual(
            home_page.messages.messages[0],
            "You have signed out.",
        )
