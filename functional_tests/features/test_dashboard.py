from functional_tests import pages
from functional_tests.base import FunctionalTestCase


class DashboardTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.create_pre_authenticated_session()

    def test_authenticated_user_can_access_dashboard(self):
        # A user visits their dashboard
        dashboard = pages.Dashboard(self)
        dashboard.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(dashboard.title, self.SITE_NAME)
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
