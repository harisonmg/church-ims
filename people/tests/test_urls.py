from django.test import SimpleTestCase
from django.urls import resolve
from django.utils.module_loading import import_string


class PeopleListURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.PeopleListView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:people_list")


class PersonCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/add/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.PersonCreateView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_create")


class AdultCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/add/adult/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.AdultCreateView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:adult_create")


class AdultSelfRegisterURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/register/self/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("people.views.AdultSelfRegisterView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:adult_self_register")


class ChildCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/add/child/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.ChildCreateView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:child_create")


class PersonDetailURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/username/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.PersonDetailView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_detail")


class PersonUpdateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/username/update/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("people.views.PersonUpdateView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_update")


class RelationshipsListURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/relationships/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("people.views.RelationshipsListView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:relationships_list")


class RelationshipCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/relationships/add/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("people.views.RelationshipCreateView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:relationship_create")


class ParentChildRelationshipCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/relationships/add/username/parent/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("people.views.ParentChildRelationshipCreateView"),
        )

    def test_view_name(self):
        self.assertEqual(
            self.match.view_name, "people:parent_child_relationship_create"
        )
