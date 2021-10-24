from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from functional_tests.utils.formatting import PEOPLE_LIST_COLUMNS, format_people_list
from functional_tests.utils.search import search_people
from people.factories import PersonFactory


class PeopleListTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        permission = Permission.objects.filter(name="Can view person")
        self.user = UserFactory(user_permissions=tuple(permission))

        # people
        people = PersonFactory.create_batch(45)
        self.people = sorted(people, key=lambda p: p.username)

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_page_navigation(self):
        # An authorized user visits the people list page
        people_list_page = pages.PeopleListPage(self)
        people_list_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title, header and heading
        self.assertEqual(people_list_page.title, self.SITE_NAME)
        self.assertEqual(people_list_page.header.title, self.header_title)
        self.assertEqual(people_list_page.heading, "People")

        # The site header an account dropdown menu as well
        people_list_page.header.toggle_account_dropdown()
        self.assertEqual(
            people_list_page.header.account_dropdown.links, self.account_dropdown_links
        )

        # He can also see a sidebar navigation, with the current page link highlighted
        self.assertEqual(
            people_list_page.sidebar.active_links,
            {"All people": self.browser.current_url},
        )

        # He also sees a list of people and a page navigation
        self.assertEqual(people_list_page.table.columns, PEOPLE_LIST_COLUMNS)
        self.assertEqual(
            people_list_page.table.data.get("1"),
            format_people_list(self.people[:1]).get("1"),
        )
        self.assertEqual(
            people_list_page.table.data, format_people_list(self.people[:10])
        )
        self.assertEqual(
            list(people_list_page.pagination.links.keys()),
            ["Previous", "1", "2", "3", "Next", "Last"],
        )
        self.assertEqual(
            people_list_page.pagination.active_links,
            {"1": f"{people_list_page.url}?page=1"},
        )
        self.assertEqual(people_list_page.pagination.disabled_links, ["Previous"])

        # He visits the last page using the page navigation and sees a list of people
        # and a page navigation
        people_list_page.pagination.go_to_page("Last")

        self.assertEqual(
            people_list_page.table.data, format_people_list(self.people[40:])
        )
        self.assertEqual(
            list(people_list_page.pagination.links.keys()),
            ["First", "Previous", "3", "4", "5", "Next"],
        )
        self.assertEqual(
            people_list_page.pagination.active_links, {"5": self.browser.current_url}
        )
        self.assertEqual(people_list_page.pagination.disabled_links, ["Next"])

        # From there, he goes to the third page finds a list of people
        # and a page navigation
        people_list_page.pagination.go_to_page("3")

        self.assertEqual(
            people_list_page.table.data, format_people_list(self.people[20:30])
        )
        self.assertEqual(
            list(people_list_page.pagination.links.keys()),
            ["First", "Previous", "1", "2", "3", "4", "5", "Next", "Last"],
        )
        self.assertEqual(
            people_list_page.pagination.active_links, {"3": self.browser.current_url}
        )
        self.assertEqual(people_list_page.pagination.disabled_links, [])

    def test_search(self):
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

        # He decides to search for a person that exists
        search_term = self.people[20].full_name
        people_list_page.search(search_term)

        search_results = search_people(search_term)
        self.assertEqual(len(people_list_page.table.data), len(search_results))
        self.assertEqual(people_list_page.table.data, search_results)
        self.assertEqual(people_list_page.table.columns, PEOPLE_LIST_COLUMNS)

        # He decides to search for a person that doesn't exist
        people_list_page.search("Does not exist")

        self.assertEqual(
            people_list_page.main_text[0], "Your search didn't yield any results"
        )
