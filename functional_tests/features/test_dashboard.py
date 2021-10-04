from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages


class DashboardTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.password = self.fake.password()
        self.user = UserFactory(password=self.password)
        self.login()

    def login(self):
        login_page = pages.LoginPage(self)
        login_page.visit()
        login_page.login(self.user.email, self.password)

    def test_authenticated_user_can_access_dashboard(self):
        # A user visits their dashboard
        dashboard = pages.Dashboard(self)
        dashboard.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        site_name = self.get_site_name()
        self.assertEqual(dashboard.title, site_name)
        self.assertEqual(dashboard.header.title, self.header_title)
        self.assertEqual(dashboard.heading, "Dashboard")

        # The site header an account dropdown menu as well
        dashboard.header.toggle_account_dropdown()
        self.assertEqual(
            dashboard.header.account_dropdown.links, self.account_dropdown_links
        )

        # He can also see a sidebar navigation, with the dashboard link highlighted
        self.assertEqual(
            dashboard.sidebar.active_links, {"Dashboard": self.browser.current_url}
        )
