from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import InterpersonalRelationshipFactory, PersonFactory


class RelationshipCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        create_relationship = Permission.objects.filter(
            name="Can add interpersonal relationship"
        )
        view_relationship = Permission.objects.filter(
            name="Can view interpersonal relationship"
        )
        permissions = create_relationship | view_relationship
        self.user = UserFactory(user_permissions=tuple(permissions))

        # relationship
        self.person = PersonFactory()
        self.relative = PersonFactory()
        relationship = InterpersonalRelationshipFactory.build()
        self.relationship_type = relationship.get_relation_display()
        self.people = f"{self.person} and {self.relative}"

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_relationship_creation(self):
        # An authorized user visits the relationship creation page.
        relationship_creation_page = pages.InterpersonalRelationshipCreationPage(self)
        relationship_creation_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(relationship_creation_page.title, self.SITE_NAME)
        self.assertEqual(relationship_creation_page.header.title, self.header_title)
        self.assertEqual(
            relationship_creation_page.heading, "Add an interpersonal relationship"
        )

        # He can also see a sidebar navigation, with the current page link highlighted
        self.assertEqual(
            relationship_creation_page.sidebar.active_links,
            {"Add an interpersonal relationship": self.browser.current_url},
        )

        # He sees the inputs of the relationship form, including labels
        # and placeholders.
        self.assertEqual(
            relationship_creation_page.form.person_username_label,
            "The person's username*",
        )
        self.assertEqual(
            relationship_creation_page.form.relative_username_label,
            "The relative's username*",
        )
        self.assertEqual(
            relationship_creation_page.form.relationship_type_label,
            "Relationship type*",
        )
        self.assertEqual(relationship_creation_page.form.submit_button_label, "Add")

        # He enters the required information and submits the form
        relationship_creation_page.add_relationship(
            self.person.username,
            self.relative.username,
            self.relationship_type,
        )

        # The relationship was added successfully and he is redirected to the
        # relationships list page
        relationship_list_page = pages.InterpersonalRelationshipsListPage(self)
        self.assertEqual(self.browser.current_url, relationship_list_page.url)
        self.assertEqual(
            relationship_list_page.messages[0],
            f"The relationship between {self.people} has been added successfully.",
        )
