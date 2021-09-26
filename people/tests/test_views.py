from django.contrib.auth.models import Permission
from django.test import TestCase

from accounts.factories import UserFactory
from people.factories import PersonFactory
from people.models import Person


class PeopleListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/"
        cls.table_head = """
        <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Username</th>
              <th scope="col">Full name</th>
            </tr>
        </thead>
        """
        # users
        permission = Permission.objects.filter(name="Can view person")
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permission))
        cls.staff_user = UserFactory(is_staff=True)

    def test_anonymous_user_response(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_authenticated_user_response(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_response(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_response(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_template_used(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "people/people_list.html")

    def test_context_data_contains_people(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertIn("people", response.context)

    def test_is_paginated(self):
        PersonFactory.create_batch(11)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("people")), 10)

    def test_pagination_lists_all_items(self):
        PersonFactory.create_batch(12)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?page=2")
        expected_people = list(Person.objects.all())[-2:]
        people = list(response.context.get("people"))
        self.assertEqual(people, expected_people)

    def test_response_with_no_people(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML("There are no people yet!", response.content.decode())

    def test_response_with_people(self):
        PersonFactory.create_batch(3)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML("There are no people yet!", response.content.decode())
        self.assertInHTML(self.table_head, response.content.decode())

    def test_search_by_full_name(self):
        people = PersonFactory.create_batch(10)
        person = people[0]
        self.client.force_login(self.authorized_user)
        response = self.client.get(f"{self.url}?q={person.full_name}")
        response_people = list(response.context.get("people"))
        self.assertEqual(response_people, [person])

    def test_search_by_name(self):
        people = PersonFactory.create_batch(10)
        person = people[0]
        first_name = person.full_name.split()[0]
        self.client.force_login(self.authorized_user)
        response = self.client.get(f"{self.url}?q={first_name}")
        response_people = list(response.context.get("people"))
        self.assertEqual(response_people, [person])

    def test_search_by_username(self):
        people = PersonFactory.create_batch(10)
        person = people[0]
        self.client.force_login(self.authorized_user)
        response = self.client.get(f"{self.url}?q={person.username}")
        response_people = list(response.context.get("people"))
        self.assertEqual(response_people, [person])

    def test_response_with_no_search_results(self):
        PersonFactory.create_batch(10)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?q=Does not exist")
        self.assertEqual(list(response.context.get("people")), [])
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )
