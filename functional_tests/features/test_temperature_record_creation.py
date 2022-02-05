from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from functional_tests.utils.formatting import PEOPLE_LIST_COLUMNS, format_people_list
from functional_tests.utils.search import search_people
from people.factories import PersonFactory
from records.factories import TemperatureRecordFactory


class TemperatureRecordCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        create_temp = Permission.objects.filter(name="Can add temperature record")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_temp | view_person
        self.user = UserFactory(user_permissions=tuple(permissions))

        # people
        people = PersonFactory.create_batch(21)
        self.people = sorted(people, key=lambda p: p.username)

        # auth
        self.create_pre_authenticated_session(self.user)

        # body temperature
        self.body_temperature = TemperatureRecordFactory.build().body_temperature

    def test_temperature_record_creation(self):
        # An authorized user visits the people list page.
        # He sees a list of people and a search form
        people_list_page = pages.PeopleListPage(self)
        people_list_page.visit()

        self.assertEqual(people_list_page.table.columns, PEOPLE_LIST_COLUMNS)
        self.assertEqual(
            people_list_page.table.data, format_people_list(self.people[:10])
        )
        self.assertEqual(people_list_page.form.search_input_placeholder, "Search")
        self.assertEqual(people_list_page.form.search_input_aria_label, "Search")
        self.assertEqual(people_list_page.form.submit_button_label, "Search")

        # He looks up a person's information to add their temperature record
        search_term = self.people[15].full_name
        people_list_page.form.enter_search_query(search_term)
        people_list_page.form.submit()

        search_results = search_people(search_term)
        self.assertEqual(len(people_list_page.table.data), len(search_results))
        self.assertEqual(people_list_page.table.data, search_results)
        self.assertEqual(people_list_page.table.columns, PEOPLE_LIST_COLUMNS)

        # Upon seeing a link to add a temperature record for the person, he clicks
        # the it and is redirected to the temperature records creation page
        username = people_list_page.table.get_cell_data("1", "Username")
        people_list_page.table.add_temperature_for_person(username)

        temp_record_creation_page = pages.TemperatureRecordCreationPage(self, username)
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
        temp_record_creation_page.form.enter_body_temperature(
            str(self.body_temperature)
        )
        temp_record_creation_page.form.submit()

        # The temperature record was added successfully and he is redirected
        # back to the people list page
        self.assertEqual(self.browser.current_url, people_list_page.url)
        self.assertEqual(
            people_list_page.messages[0],
            f"A temperature record for {username} has been added successfully.",
        )
