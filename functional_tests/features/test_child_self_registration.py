from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory, ChildFactory


class ChildRegistrationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.user = UserFactory()

        # people
        self.parent = AdultFactory(user_account=self.user)
        self.child = ChildFactory.build()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_child_registration(self):
        # A user visits their child's registration page.
        child_registration_page = pages.ChildSelfRegistrationPage(
            self, self.parent.username
        )
        child_registration_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(child_registration_page.title, self.SITE_NAME)
        self.assertEqual(child_registration_page.header.title, self.header_title)
        self.assertEqual(
            child_registration_page.heading, "Add your child's personal information"
        )

        # He sees the inputs of the adult form, including labels and placeholders.
        self.assertEqual(child_registration_page.form.username_label, "Username*")
        self.assertEqual(child_registration_page.form.full_name_label, "Full name*")
        self.assertEqual(child_registration_page.form.gender_label, "Gender*")
        self.assertEqual(
            child_registration_page.form.date_of_birth_label, "Date of birth*"
        )
        self.assertEqual(child_registration_page.form.submit_button_label, "Add")

        # He enters his child's details and submits the form
        child_registration_page.add_child(
            self.child.username,
            self.child.full_name,
            self.child.get_gender_display(),
            str(self.child.dob),
        )

        # His information was added successfully and is redirected
        # to his dashboard
        dashboard = pages.Dashboard(self)
        self.assertEqual(self.browser.current_url, dashboard.url)
        self.assertEqual(
            dashboard.messages[0],
            f"{self.child.username}'s information has been added successfully.",
        )
