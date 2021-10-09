from django.contrib.auth.models import Permission
from django.utils import dateformat, timezone

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.pages import pages
from records.factories import TemperatureRecordFactory
from records.utils import format_temperature


class TemperatureRecordsListTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        permission = Permission.objects.filter(name="Can view temperature record")
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permission)
        )

        # temperature records
        temperature_records = TemperatureRecordFactory.create_batch(45)
        self.temperature_records = sorted(
            temperature_records, key=lambda record: record.person.username
        )
        self.login(self.user, self.password)

    @staticmethod
    def format_datetime(dt, fmt="j M Y, g:i a"):
        local_dt = timezone.localtime(dt)
        return dateformat.format(local_dt, fmt)

    def format_temperature_records(self, temperature_records):
        search_results = {}
        for i, record in enumerate(temperature_records):
            search_results[str(i + 1)] = [
                record.person.username,
                format_temperature(record.body_temperature),
                self.format_datetime(record.created_at),
            ]
        return search_results

    def find_temperature_records_by_person_name(self, name):
        search_results = []
        for record in self.temperature_records:
            if name.lower() in record.person.full_name.lower():
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
            temp_records_list_page.table.data.get("1"),
            self.format_temperature_records(self.temperature_records[:1]).get("1"),
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

    def test_search(self):
        # An authorized user visits the temperature records list page.
        # He sees a list of temperature records and a search form
        temp_records_list_page = pages.TemperatureRecordsListPage(self)
        temp_records_list_page.visit()

        self.assertEqual(
            temp_records_list_page.table.columns,
            ["#", "Username", "Temperature", "Time"],
        )
        self.assertEqual(
            temp_records_list_page.table.data,
            self.format_temperature_records(self.temperature_records[:10]),
        )
        self.assertEqual(temp_records_list_page.form.search_input_placeholder, "Search")
        self.assertEqual(temp_records_list_page.form.search_input_aria_label, "Search")
        self.assertEqual(temp_records_list_page.form.submit_button_label, "Search")

        # He decides to search temperature records for a person that exists
        search_term = self.temperature_records[20].person.full_name
        temp_records_list_page.search(search_term)

        search_results = self.find_temperature_records_by_person_name(search_term)
        self.assertEqual(len(temp_records_list_page.table.data), len(search_results))
        self.assertEqual(temp_records_list_page.table.data, search_results)
        self.assertEqual(
            temp_records_list_page.table.columns,
            ["#", "Username", "Temperature", "Time"],
        )

        # He decides to search temperature records for a person that doesn't exist
        temp_records_list_page.search("Does not exist")

        self.assertEqual(
            temp_records_list_page.main_text[0], "Your search didn't yield any results"
        )
