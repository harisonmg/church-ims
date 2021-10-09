from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.helpers import find_people_by_name, format_people_details
from functional_tests.pages import pages
from people.factories import PersonFactory
from records.factories import TemperatureRecordFactory


class TemperatureRecordCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        create_temp = Permission.objects.filter(name="Can add temperature record")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = list(create_temp) + list(view_person)
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permissions)
        )

        # people
        people = PersonFactory.create_batch(21)
        self.people = sorted(people, key=lambda p: p.username)
        self.login(self.user, self.password)

        # body temperature
        self.body_temperature = TemperatureRecordFactory.build().body_temperature

    def test_temperature_record_creation(self):
        # An authorized user visits the people list page.
        # He sees a list of people and a search form
        people_list_page = pages.PeopleListPage(self)
        people_list_page.visit()

        self.assertEqual(people_list_page.table.columns, self.PEOPLE_LIST_COLUMNS)
        self.assertEqual(
            people_list_page.table.data, format_people_details(self.people[:10])
        )
        self.assertEqual(people_list_page.form.search_input_placeholder, "Search")
        self.assertEqual(people_list_page.form.search_input_aria_label, "Search")
        self.assertEqual(people_list_page.form.submit_button_label, "Search")

        # He looks up a person's information to add their temperature record
        search_term = self.people[15].full_name
        people_list_page.search(search_term)

        search_results = find_people_by_name(self.people, search_term)
        self.assertEqual(len(people_list_page.table.data), len(search_results))
        self.assertEqual(people_list_page.table.data, search_results)
        self.assertEqual(people_list_page.table.columns, self.PEOPLE_LIST_COLUMNS)

        # Upon seeing a link to add a temperature record for the person, he clicks
        # the it and is redirected to the temperature records creation page
        username = people_list_page.table.get_cell_data("1", "Username")
        people_list_page.table.add_temperature_for_person(username)

        temp_record_creation_page = pages.TemperatureRecordCreatePage(self, username)
        self.assertEqual(self.browser.current_url, temp_record_creation_page.url)
        self.assertEqual(temp_record_creation_page.title, self.SITE_NAME)
        self.assertEqual(temp_record_creation_page.header.title, self.header_title)
        self.assertEqual(
            temp_record_creation_page.heading,
            f"Add a temperature record for {username}",
        )

        # He sees the inputs of the temperature record creation form,
        # including labels and placeholders.
        self.assertEqual(
            temp_record_creation_page.form.body_temperature_label, "Body temperature*"
        )
        self.assertEqual(temp_record_creation_page.form.submit_button_label, "Add")

        # He enters enters the person's body temperature and submits the form
        temp_record_creation_page.add_temperature(self.body_temperature)

        # The temperature record was added successfully and he is redirected
        # back to the people list page
        self.assertEqual(self.browser.current_url, people_list_page.url)
        self.assertEqual(
            people_list_page.messages.messages[0],
            f"A temperature record for {username} has been added successfully.",
        )
