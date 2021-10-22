from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils.module_loading import import_string

from accounts.factories import UserFactory
from people.factories import (
    AdultFactory,
    ChildFactory,
    InterpersonalRelationshipFactory,
    PersonFactory,
)
from people.models import InterpersonalRelationship, Person

from .helpers import search_interpersonal_relationships, search_people


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
                <th scope="col">Age category</th>
                <th scope="col">Actions</th>
            </tr>
        </thead>
        """
        # users
        view_person = Permission.objects.filter(name="Can view person")
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(view_person))
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

    def test_search_results(self):
        # setup
        people = PersonFactory.create_batch(10)
        search_term = people[0].full_name.split()[0]
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        search_results = response.context.get("people")
        self.assertQuerysetEqual(search_results, search_people(search_term))

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


class PersonCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/add/"

        # users
        create_person = Permission.objects.filter(name="Can add person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_person | view_person
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permissions))
        cls.staff_user = UserFactory(is_staff=True)

        # POST data
        person = PersonFactory.build()
        cls.data = {
            "username": person.username,
            "full_name": person.full_name,
            "gender": person.gender,
            "dob": person.dob,
        }

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
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_context_data_contains_action(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("action"), "add")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(form.__class__.__name__, "PersonCreationForm")
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(form, import_string("people.forms.PersonCreationForm"))

    def test_form_valid(self):
        self.client.force_login(self.authorized_user)
        self.client.post(self.url, self.data)
        person = Person.objects.get(username=self.data["username"])
        self.assertEqual(person.created_by, self.authorized_user)

    def test_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(
            response,
            reverse("people:person_detail", kwargs={"username": self.data["username"]}),
        )


class AdultCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/add/adult/"

        # users
        create_person = Permission.objects.filter(name="Can add person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_person | view_person
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permissions))
        cls.staff_user = UserFactory(is_staff=True)

        # POST data
        person = AdultFactory.build()
        cls.data = {
            "username": person.username,
            "full_name": person.full_name,
            "gender": person.gender,
            "dob": person.dob,
            "phone_number": person.phone_number,
        }

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
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_context_data_contains_action(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("action"), "add")

    def test_context_data_contains_age_category(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("age_category"), "an adult")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(form.__class__.__name__, "AdultCreationForm")
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(form, import_string("people.forms.AdultCreationForm"))

    def test_form_valid(self):
        self.client.force_login(self.authorized_user)
        self.client.post(self.url, self.data)
        person = Person.objects.get(username=self.data["username"])
        self.assertEqual(person.created_by, self.authorized_user)

    def test_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(
            response,
            reverse("people:person_detail", kwargs={"username": self.data["username"]}),
        )


class AdultSelfRegisterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/register/self/"

        # users
        create_person = Permission.objects.filter(name="Can add person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_person | view_person
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permissions))
        cls.staff_user = UserFactory(is_staff=True)

        # POST data
        person = AdultFactory.build()
        cls.data = {
            "username": person.username,
            "full_name": person.full_name,
            "gender": person.gender,
            "dob": person.dob,
            "phone_number": person.phone_number,
        }

    def test_anonymous_user_response(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_authenticated_user_response(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_authorized_user_response(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_response(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "people/self_register_form.html")

    def test_context_data_contains_action(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("action"), "add")

    def test_context_data_contains_age_category(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("age_category"), "an adult")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(form.__class__.__name__, "AdultCreationForm")
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(form, import_string("people.forms.AdultCreationForm"))

    def test_form_valid(self):
        self.client.force_login(self.authorized_user)
        self.client.post(self.url, self.data)
        person = Person.objects.get(username=self.data["username"])
        self.assertEqual(person.user_account, self.authorized_user)
        self.assertEqual(person.created_by, self.authorized_user)

    def test_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse("core:dashboard"))


class ChildCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/add/child/"

        # users
        cls.user = UserFactory()
        cls.authorized_user = UserFactory()

        # POST data
        cls.parent = AdultFactory(user_account=cls.authorized_user)
        child = ChildFactory.build()
        cls.data = {
            "username": child.username,
            "full_name": child.full_name,
            "gender": child.gender,
            "dob": child.dob,
        }

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

    def test_template_used(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_context_data_contains_action(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("action"), "add")

    def test_context_data_contains_age_category(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("age_category"), "a child")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(form.__class__.__name__, "ChildCreationForm")
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(form, import_string("people.forms.ChildCreationForm"))

    def test_is_parent_form_valid(self):
        # setup
        data = self.data.copy()
        data["is_parent"] = True
        self.client.force_login(self.authorized_user)

        # test person
        self.client.post(self.url, self.data)
        person = Person.objects.get(username=self.data["username"])
        self.assertEqual(person.created_by, self.authorized_user)

        # test relationship
        relationship = InterpersonalRelationship.objects.get(person=self.parent)
        self.assertEqual(relationship.relative, person)
        self.assertEqual(relationship.relation, "PC")
        self.assertEqual(relationship.created_by, self.authorized_user)

    def test_not_parent_form_valid(self):
        self.client.force_login(self.authorized_user)
        self.client.post(self.url, self.data)
        person = Person.objects.get(username=self.data["username"])
        self.assertEqual(person.created_by, self.authorized_user)

    def test_is_parent_success_url(self):
        # setup
        data = self.data.copy()
        data["is_parent"] = True
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("core:dashboard"))

    def test_not_parent_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse("core:dashboard"))


class PersonDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory()
        cls.url = cls.person.get_absolute_url()

        # users
        view_person = Permission.objects.filter(name="Can view person")
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(view_person))
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
        self.assertTemplateUsed(response, "people/person_detail.html")

    def test_context_data_contains_person(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("person"), self.person)


class PersonUpdateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory()
        cls.url = cls.person.get_absolute_url() + "update/"

        # users
        update_person = Permission.objects.filter(name="Can change person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = update_person | view_person
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permissions))
        cls.staff_user = UserFactory(is_staff=True)

        # POST data
        cls.data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name + " " + cls.person.username.title(),
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }

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
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_context_data_contains_person(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("person"), self.person)

    def test_context_data_contains_action(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context.get("action"), "update")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(form.__class__.__name__, "PersonUpdateForm")
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(form, import_string("people.forms.PersonUpdateForm"))

    def test_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, self.person.get_absolute_url())


class RelationshipsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/relationships/"
        cls.table_head = """
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Person</th>
                <th scope="col">Relative</th>
                <th scope="col">Relationship type</th>
            </tr>
        </thead>
        """
        # users
        view_relationships = Permission.objects.filter(
            name="Can view interpersonal relationship"
        )
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(view_relationships))
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
        self.assertTemplateUsed(response, "people/relationships_list.html")

    def test_context_data_contains_relationships(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertIn("relationships", response.context)

    def test_is_paginated(self):
        InterpersonalRelationshipFactory.create_batch(11)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("relationships")), 10)

    def test_pagination_lists_all_items(self):
        InterpersonalRelationshipFactory.create_batch(12)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?page=2")
        expected_relationships = list(InterpersonalRelationship.objects.all())[-2:]
        people = list(response.context.get("relationships"))
        self.assertEqual(people, expected_relationships)

    def test_response_with_no_relationships(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "There are no interpersonal relationships yet!", response.content.decode()
        )

    def test_response_with_relationships(self):
        InterpersonalRelationshipFactory.create_batch(3)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(
                "There are no interpersonal relationships yet!",
                response.content.decode(),
            )
        self.assertInHTML(self.table_head, response.content.decode())

    def test_search_results(self):
        # setup
        relationships = InterpersonalRelationshipFactory.create_batch(10)
        search_term = relationships[0].person.username
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        search_results = response.context.get("relationships")
        self.assertQuerysetEqual(
            search_results, search_interpersonal_relationships(search_term)
        )

    def test_response_with_no_search_results(self):
        InterpersonalRelationshipFactory.create_batch(10)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?q=Does not exist")
        self.assertEqual(list(response.context.get("relationships")), [])
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )


class RelationshipCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/relationships/add/"

        # users
        create_relationship = Permission.objects.filter(
            name="Can add interpersonal relationship"
        )
        view_relationship = Permission.objects.filter(
            name="Can view interpersonal relationship"
        )
        permissions = create_relationship | view_relationship
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permissions))
        cls.staff_user = UserFactory(is_staff=True)

        # POST data
        cls.person = PersonFactory()
        cls.relative = PersonFactory()
        cls.relation = InterpersonalRelationshipFactory.build().relation
        cls.data = {
            "person": cls.person.username,
            "relative": cls.relative.username,
            "relation": cls.relation,
        }

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
        self.assertTemplateUsed(response, "people/relationship_form.html")

    def test_form_class(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertEqual(
            form.__class__.__name__, "InterpersonalRelationshipCreationForm"
        )
        self.assertIsInstance(form, import_string("django.forms.ModelForm"))
        self.assertIsInstance(
            form, import_string("people.forms.InterpersonalRelationshipCreationForm")
        )

    def test_form_valid(self):
        self.client.force_login(self.authorized_user)
        self.client.post(self.url, self.data)
        relationship = InterpersonalRelationship.objects.get(
            person__username=self.data["person"]
        )
        self.assertEqual(relationship.created_by, self.authorized_user)

    def test_success_url(self):
        self.client.force_login(self.authorized_user)
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse("people:relationships_list"))
