from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import PersonFactory


class PersonUpdateTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        change_person = Permission.objects.filter(name="Can change person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = list(change_person) + list(view_person)
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permissions)
        )

        # person
        self.person = PersonFactory()
        self.login(self.user, self.password)

    def test_person_creation(self):
        # An authorized user visits a person's detail page.
        person_detail_page = pages.PersonDetailPage(self, self.person.username)
        person_detail_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_detail_page.title, self.SITE_NAME)
        self.assertEqual(person_detail_page.header.title, self.header_title)
        self.assertEqual(person_detail_page.heading, f"{self.person.username}'s info")

        # He sees the person's details and an update link.
        self.assertEqual(
            person_detail_page.main_text[0], f"Name: {self.person.full_name}"
        )
        self.assertEqual(
            person_detail_page.main_text[1],
            f"Gender: {self.person.get_gender_display()}",
        )
        self.assertEqual(person_detail_page.main_text[2], f"Age: {self.person.age}")
        self.assertEqual(
            person_detail_page.update_link,
            {"Update": pages.PersonUpdatePage(self, self.person.username).url},
        )
