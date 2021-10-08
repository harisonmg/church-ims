from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages
from people.factories import PersonFactory


class PersonUpdateTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        update_person = Permission.objects.filter(name="Can change person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = list(update_person) + list(view_person)
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permissions)
        )

        # person
        self.person = PersonFactory()
        self.data = {
            "full_name": self.person.full_name + " " + self.person.username.title()
        }

        self.login(self.user, self.password)

    def test_person_creation(self):
        # An authorized user visits the person update page.
        person_update_page = pages.PersonUpdatePage(self, self.person.username)
        person_update_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_update_page.title, self.SITE_NAME)
        self.assertEqual(person_update_page.header.title, self.header_title)
        self.assertEqual(person_update_page.heading, "Update a person's information")

        # He sees the inputs of the person form, including labels and placeholders.
        self.assertEqual(person_update_page.form.username_label, "Username*")
        self.assertEqual(person_update_page.form.full_name_label, "Full name*")
        self.assertEqual(person_update_page.form.submit_button_label, "Update")

        # He enters the person's full name and submits the form
        person_update_page.update_person(**self.data)

        # The person's information was added successfully and he is redirected
        # to the person's detail page
        person_detail_page = pages.PersonDetailPage(self, self.person.username)
        self.assertEqual(self.browser.current_url, person_detail_page.url)
        self.assertEqual(
            person_detail_page.messages.messages[0],
            f"{self.person.username}'s information has been updated successfully.",
        )
