from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages

# from records.factories import TemperatureRecordFactory


class TemperatureRecordsListTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        permission = Permission.objects.filter(name="Can view person")
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permission)
        )

        # temperature records
        # temperature_records = TemperatureRecordFactory.create_batch(45)
        # self.temperature_records = sorted(temperature_records, key=lambda tr: tr.username)
        self.login()

    def login(self):
        login_page = pages.LoginPage(self)
        login_page.visit()
        login_page.login(self.user.email, self.password)

    def format_temperature_records(self, temperature_records):
        search_results = {}
        for i, record in enumerate(temperature_records):
            search_results[str(i + 1)] = [record.username, record.full_name]
        return search_results

    def find_temperature_records_by_person_name(self, name):
        search_results = []
        for record in self.temperature_records:
            if name.lower() in record.full_name.lower():
                search_results.append(record)
        return self.format_temperature_records(search_results)

    def test_page_navigation(self):
        # An authorized user visits the temperature records list page
        temp_records_list_page = pages.TemperatureRecordsListPage(self)
        temp_records_list_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title, header and heading
        self.assertEqual(temp_records_list_page.title, self.SITE_NAME)
        self.assertEqual(temp_records_list_page.header.title, self.header_title)
        self.assertEqual(temp_records_list_page.heading, "Temperature records")

        # The site header an account dropdown menu as well
        temp_records_list_page.header.toggle_account_dropdown()
        self.assertEqual(
            temp_records_list_page.header.account_dropdown.links,
            self.account_dropdown_links,
        )

        # He can also see a sidebar navigation, with the temperature records
        # link highlighted
        self.assertEqual(
            temp_records_list_page.sidebar.active_links,
            {"Temperature records": self.browser.current_url},
        )

        # He also sees a list of temperature records and a page navigation
        self.assertEqual(
            temp_records_list_page.table.columns,
            ["#", "Username", "Temperature", "Time"],
        )
        self.assertEqual(
            temp_records_list_page.table.data,
            self.format_temperature_records(self.temperature_records[:10]),
        )
        self.assertEqual(
            list(temp_records_list_page.pagination.links.keys()),
            ["Previous", "1", "2", "3", "Next", "Last"],
        )
        self.assertEqual(
            temp_records_list_page.pagination.active_links,
            {"1": f"{temp_records_list_page.url}?page=1"},
        )
        self.assertEqual(temp_records_list_page.pagination.disabled_links, ["Previous"])

        # He visits the last page using the page navigation and sees a list of
        # temperature records and a page navigation
        temp_records_list_page.pagination.go_to_page("Last")

        self.assertEqual(
            temp_records_list_page.table.data,
            self.format_temperature_records(self.temperature_records[40:]),
        )
        self.assertEqual(
            list(temp_records_list_page.pagination.links.keys()),
            ["First", "Previous", "3", "4", "5", "Next"],
        )
        self.assertEqual(
            temp_records_list_page.pagination.active_links,
            {"5": self.browser.current_url},
        )
        self.assertEqual(temp_records_list_page.pagination.disabled_links, ["Next"])

        # From there, he goes to the third page finds a list of temperature records
        # and a page navigation
        temp_records_list_page.pagination.go_to_page("3")

        self.assertEqual(
            temp_records_list_page.table.data,
            self.format_temperature_records(self.temperature_records[20:30]),
        )
        self.assertEqual(
            list(temp_records_list_page.pagination.links.keys()),
            ["First", "Previous", "1", "2", "3", "4", "5", "Next", "Last"],
        )
        self.assertEqual(
            temp_records_list_page.pagination.active_links,
            {"3": self.browser.current_url},
        )
        self.assertEqual(temp_records_list_page.pagination.disabled_links, [])
