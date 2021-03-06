from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import PersonFactory


class PersonCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        create_person = Permission.objects.filter(name="Can add person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_person | view_person
        self.user = UserFactory(user_permissions=tuple(permissions))

        # person
        self.person = PersonFactory.build()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_person_creation(self):
        # An authorized user visits the person creation page.
        person_creation_page = pages.PersonCreationPage(self)
        person_creation_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_creation_page.title, self.SITE_NAME)
        self.assertEqual(person_creation_page.header.title, self.header_title)
        self.assertEqual(person_creation_page.heading, "Add a person's information")

        # He sees the inputs of the person form, including labels and placeholders.
        self.assertEqual(person_creation_page.form.username_label, "Username*")
        self.assertEqual(person_creation_page.form.full_name_label, "Full name*")
        self.assertEqual(person_creation_page.form.gender_label, "Gender*")
        self.assertEqual(
            person_creation_page.form.date_of_birth_label, "Date of birth*"
        )
        self.assertEqual(person_creation_page.form.submit_button_label, "Add")

        # He enters the person's details and submits the form
        person_creation_page.form.enter_username(self.person.username)
        person_creation_page.form.enter_full_name(self.person.full_name)
        person_creation_page.form.select_gender(self.person.get_gender_display())
        person_creation_page.form.enter_dob(str(self.person.dob))
        person_creation_page.form.submit()

        # The person's information was added successfully and he is redirected
        # to the person's detail page
        person_detail_page = pages.PersonDetailPage(self, self.person.username)
        self.assertEqual(self.browser.current_url, person_detail_page.url)
        self.assertEqual(
            person_detail_page.messages[0],
            f"{self.person.username}'s information has been added successfully.",
        )
