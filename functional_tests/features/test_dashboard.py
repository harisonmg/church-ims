from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory


class DashboardTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.user = UserFactory()
        self.person = AdultFactory(user_account=self.user)
        self.create_pre_authenticated_session(self.user)

    def test_navigation(self):
        # A user visits his dashboard
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

    def test_user_details(self):
        # A user visits his dashboard
        dashboard = pages.Dashboard(self)
        dashboard.visit()

        # He sees his personal details and interpersonal relationships
        self.assertEqual(dashboard.main_text[0], f"Username: {self.person.username}")
        self.assertEqual(dashboard.main_text[1], f"Name: {self.person.full_name}")
        self.assertEqual(
            dashboard.main_text[2],
            f"Gender: {self.person.get_gender_display()}",
        )
        self.assertEqual(dashboard.main_text[3], f"Age: {self.person.age}")
        self.assertEqual(
            dashboard.main_text[4], f"Phone number: {self.person.phone_number}"
        )
        self.assertEqual(dashboard.main_text[5], f"Email address: {self.user.email}")
