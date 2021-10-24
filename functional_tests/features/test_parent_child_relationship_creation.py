from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory, ChildFactory


class RelationshipCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.user = UserFactory()

        # relationship
        self.person = AdultFactory(user_account=self.user)
        self.parent = AdultFactory()
        self.child = ChildFactory()
        self.people = f"{self.parent} and {self.child}"

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_relationship_creation(self):
        # A user visits the parent-child relationship creation page.
        relationship_creation_page = pages.ParentChildRelationshipCreationPage(
            self, self.child.username
        )
        relationship_creation_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(relationship_creation_page.title, self.SITE_NAME)
        self.assertEqual(relationship_creation_page.header.title, self.header_title)
        self.assertEqual(
            relationship_creation_page.heading, f"Add {self.child}'s parent"
        )

        # He sees the inputs of the relationship form, including labels
        # and placeholders.
        self.assertEqual(
            relationship_creation_page.form.parent_username_label,
            "The parent's username*",
        )
        self.assertEqual(relationship_creation_page.form.submit_button_label, "Add")

        # He enters the required information and submits the form
        relationship_creation_page.add_parent(self.parent.username)

        # The relationship was added successfully and he is redirected to his dashboard
        dashboard = pages.Dashboard(self)
        self.assertEqual(self.browser.current_url, dashboard.url)
        self.assertEqual(
            dashboard.messages[0],
            f"A parent-child relationship between {self.people} has been added.",
        )
