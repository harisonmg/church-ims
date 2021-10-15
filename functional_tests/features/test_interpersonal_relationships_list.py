from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from functional_tests.utils.formatting import (
    INTERPERSONAL_RELATIONSHIPS_LIST_COLUMNS,
    format_interpersonal_relationships,
)
from functional_tests.utils.search import search_interpersonal_relationships

# from people.factories import RelationshipFactory


class RelationshipsListTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        permission = Permission.objects.filter(name="Can view relationship")
        self.user = UserFactory(user_permissions=tuple(permission))

        # relationships
        # relationships = RelationshipFactory.create_batch(45)
        # self.relationships = sorted(relationships, key=lambda r: r.person.username)

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_page_navigation(self):
        # An authorized user visits the relationships list page
        relationships_list_page = pages.RelationshipsListPage(self)
        relationships_list_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title, header and heading
        self.assertEqual(relationships_list_page.title, self.SITE_NAME)
        self.assertEqual(relationships_list_page.header.title, self.header_title)
        self.assertEqual(relationships_list_page.heading, "Relationships")

        # The site header an account dropdown menu as well
        relationships_list_page.header.toggle_account_dropdown()
        self.assertEqual(
            relationships_list_page.header.account_dropdown.links,
            self.account_dropdown_links,
        )

        # He can also see a sidebar navigation, with the relationships link highlighted
        self.assertEqual(
            relationships_list_page.sidebar.active_links,
            {"Relationships": self.browser.current_url},
        )

        # He also sees a list of relationships and a page navigation
        self.assertEqual(
            relationships_list_page.table.columns,
            INTERPERSONAL_RELATIONSHIPS_LIST_COLUMNS,
        )
        self.assertEqual(
            relationships_list_page.table.data.get("1"),
            format_interpersonal_relationships(self.relationships[:1]).get("1"),
        )
        self.assertEqual(
            relationships_list_page.table.data,
            format_interpersonal_relationships(self.relationships[:10]),
        )
        self.assertEqual(
            list(relationships_list_page.pagination.links.keys()),
            ["Previous", "1", "2", "3", "Next", "Last"],
        )
        self.assertEqual(
            relationships_list_page.pagination.active_links,
            {"1": f"{relationships_list_page.url}?page=1"},
        )
        self.assertEqual(
            relationships_list_page.pagination.disabled_links, ["Previous"]
        )

        # He visits the last page using the page navigation and sees
        # a list of relationships and a page navigation
        relationships_list_page.pagination.go_to_page("Last")

        self.assertEqual(
            relationships_list_page.table.data,
            format_interpersonal_relationships(self.relationships[40:]),
        )
        self.assertEqual(
            list(relationships_list_page.pagination.links.keys()),
            ["First", "Previous", "3", "4", "5", "Next"],
        )
        self.assertEqual(
            relationships_list_page.pagination.active_links,
            {"5": self.browser.current_url},
        )
        self.assertEqual(relationships_list_page.pagination.disabled_links, ["Next"])

        # From there, he goes to the third page finds a list of relationships
        # and a page navigation
        relationships_list_page.pagination.go_to_page("3")

        self.assertEqual(
            relationships_list_page.table.data,
            format_interpersonal_relationships(self.relationships[20:30]),
        )
        self.assertEqual(
            list(relationships_list_page.pagination.links.keys()),
            ["First", "Previous", "1", "2", "3", "4", "5", "Next", "Last"],
        )
        self.assertEqual(
            relationships_list_page.pagination.active_links,
            {"3": self.browser.current_url},
        )
        self.assertEqual(relationships_list_page.pagination.disabled_links, [])

    def test_search(self):
        # An authorized user visits the relationships list page.
        # He sees a list of relationships and a search form
        relationships_list_page = pages.RelationshipsListPage(self)
        relationships_list_page.visit()

        self.assertEqual(
            relationships_list_page.table.columns,
            INTERPERSONAL_RELATIONSHIPS_LIST_COLUMNS,
        )
        self.assertEqual(
            relationships_list_page.table.data,
            format_interpersonal_relationships(self.relationships[:10]),
        )
        self.assertEqual(
            relationships_list_page.form.search_input_placeholder, "Search"
        )
        self.assertEqual(relationships_list_page.form.search_input_aria_label, "Search")
        self.assertEqual(relationships_list_page.form.submit_button_label, "Search")

        # He decides to search for a relationship that exists
        search_term = self.relationships[20].person.username
        relationships_list_page.search(search_term)

        search_results = search_interpersonal_relationships(search_term)
        self.assertEqual(len(relationships_list_page.table.data), len(search_results))
        self.assertEqual(relationships_list_page.table.data, search_results)
        self.assertEqual(
            relationships_list_page.table.columns,
            INTERPERSONAL_RELATIONSHIPS_LIST_COLUMNS,
        )

        # He decides to search for a relationship that doesn't exist
        relationships_list_page.search("Does not exist")

        self.assertEqual(
            relationships_list_page.main_text[0], "Your search didn't yield any results"
        )
