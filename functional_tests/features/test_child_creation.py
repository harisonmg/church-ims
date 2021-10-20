from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory, ChildFactory


class ChildCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.user = UserFactory()

        # child
        self.parent = AdultFactory(user_account=self.user)
        self.child = ChildFactory.build()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_child_creation_by_parent(self):
        # A parent visits the child creation page.
        child_creation_page = pages.ChildCreationPage(self)
        child_creation_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(child_creation_page.title, self.SITE_NAME)
        self.assertEqual(child_creation_page.header.title, self.header_title)
        self.assertEqual(child_creation_page.heading, "Add a child's information")

        # He sees the inputs of the child form, including labels and placeholders.
        self.assertEqual(child_creation_page.form.username_label, "Username*")
        self.assertEqual(child_creation_page.form.full_name_label, "Full name*")
        self.assertEqual(child_creation_page.form.gender_label, "Gender*")
        self.assertEqual(child_creation_page.form.date_of_birth_label, "Date of birth*")
        self.assertEqual(
            child_creation_page.form.is_parent_checkbox_label, "I am the child's parent"
        )
        self.assertEqual(child_creation_page.form.submit_button_label, "Add")

        # He enters the child's username and full name and submits the form
        child_creation_page.add_child(
            self.child.username,
            self.child.full_name,
            self.child.get_gender_display(),
            str(self.child.dob),
            True,
        )

        # The child's information was added successfully and he is redirected
        # to the his dashboard
        dashboard = pages.Dashboard(self)
        self.assertEqual(self.browser.current_url, dashboard.url)
        self.assertEqual(
            dashboard.messages[0],
            f"{self.child.username}'s information has been added successfully.",
        )
        people = f"{self.parent.username} and {self.child.username}"
        self.assertEqual(
            dashboard.messages[0],
            f"The relationship between {people} has been added successfully.",
        )
