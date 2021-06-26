from django.contrib.auth import get_user_model
from django.test import TestCase

from children.models import Child, ParentChildRelationship, RelationshipType


class ChildModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

        cls.admin_user = cls.User.objects.create_superuser(
            username="Kelvin", email="kelvin@murage.com", password="kelvinpassword"
        )

        cls.child = Child.objects.create(
            slug="Josephine",
            full_name="Josephine Nyakinyua",
            dob="2015-09-25",
            gender="F",
            created_by=cls.admin_user,
        )

    def test_child_basic(self):
        self.assertEqual(self.child.slug, "Josephine")
        self.assertEqual(self.child.full_name, "Josephine Nyakinyua")
        self.assertEqual(self.child.dob, "2015-09-25")
        self.assertEqual(self.child.gender, "F")
        self.assertEqual(self.child.created_by, self.admin_user)

    # class methods
    def test_child_object_name_is_slug(self):
        self.assertEqual(self.child.slug, str(self.child))

    # slug
    def test_slug_label(self):
        slug__meta = self.child._meta.get_field("slug")
        self.assertEqual(slug__meta.verbose_name, "username")

    def test_slug_max_length(self):
        slug__meta = self.child._meta.get_field("slug")
        self.assertEqual(slug__meta.max_length, 50)

    def test_slug_is_null(self):
        slug__meta = self.child._meta.get_field("slug")
        self.assertFalse(slug__meta.null)

    def test_slug_is_blank(self):
        slug__meta = self.child._meta.get_field("slug")
        self.assertFalse(slug__meta.blank)

    # full name
    def test_full_name_label(self):
        full_name__meta = self.child._meta.get_field("full_name")
        self.assertEqual(full_name__meta.verbose_name, "full name")

    def test_full_name_max_length(self):
        full_name__meta = self.child._meta.get_field("full_name")
        self.assertEqual(full_name__meta.max_length, 300)

    def test_full_name_is_null(self):
        full_name__meta = self.child._meta.get_field("full_name")
        self.assertFalse(full_name__meta.null)

    def test_full_name_is_blank(self):
        full_name__meta = self.child._meta.get_field("full_name")
        self.assertFalse(full_name__meta.blank)

    # date of birth
    def test_dob_label(self):
        dob__meta = self.child._meta.get_field("dob")
        self.assertEqual(dob__meta.verbose_name, "date of birth")

    def test_dob_max_length(self):
        dob__meta = self.child._meta.get_field("dob")
        self.assertIsNone(dob__meta.max_length)

    def test_dob_is_null(self):
        dob__meta = self.child._meta.get_field("dob")
        self.assertFalse(dob__meta.null)

    def test_dob_is_blank(self):
        dob__meta = self.child._meta.get_field("dob")
        self.assertFalse(dob__meta.blank)

    # gender
    def test_gender_label(self):
        gender__meta = self.child._meta.get_field("gender")
        self.assertEqual(gender__meta.verbose_name, "gender")

    def test_gender_max_length(self):
        gender__meta = self.child._meta.get_field("gender")
        self.assertTrue(gender__meta.max_length, 2)

    def test_gender_is_null(self):
        gender__meta = self.child._meta.get_field("gender")
        self.assertFalse(gender__meta.null)

    def test_gender_is_blank(self):
        gender__meta = self.child._meta.get_field("gender")
        self.assertFalse(gender__meta.blank)

    # created by
    def test_created_by_label(self):
        created_by__meta = self.child._meta.get_field("created_by")
        self.assertEqual(created_by__meta.verbose_name, "created by")

    def test_created_by_max_length(self):
        created_by__meta = self.child._meta.get_field("created_by")
        self.assertIsNone(created_by__meta.max_length)

    def test_created_by_is_null(self):
        created_by__meta = self.child._meta.get_field("created_by")
        self.assertTrue(created_by__meta.null)

    def test_created_by_is_blank(self):
        created_by__meta = self.child._meta.get_field("created_by")
        self.assertFalse(created_by__meta.blank)

    # updated by
    def test_updated_by_label(self):
        updated_by__meta = self.child._meta.get_field("updated_by")
        self.assertEqual(updated_by__meta.verbose_name, "updated by")

    def test_updated_by_max_length(self):
        updated_by__meta = self.child._meta.get_field("updated_by")
        self.assertIsNone(updated_by__meta.max_length)

    def test_updated_by_is_null(self):
        updated_by__meta = self.child._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.null)

    def test_updated_by_is_blank(self):
        updated_by__meta = self.child._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.blank)


class RelationshipTypeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mother = RelationshipType.objects.create(name="mother")

    def test_relationship_type_basic(self):
        self.assertEqual(self.mother.name, "mother")

    def test_relationship_type_object_name_is_name(self):
        self.assertEqual(self.mother.name, str(self.mother))

    # name
    def test_name_label(self):
        name__meta = self.mother._meta.get_field("name")
        self.assertEqual(name__meta.verbose_name, "name")

    def test_name_max_length(self):
        name__meta = self.mother._meta.get_field("name")
        self.assertEqual(name__meta.max_length, 50)

    def test_name_is_null(self):
        name__meta = self.mother._meta.get_field("name")
        self.assertFalse(name__meta.null)

    def test_name_is_blank(self):
        name__meta = self.mother._meta.get_field("name")
        self.assertFalse(name__meta.blank)


class FamilyRelationshipModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

        cls.admin = cls.User.objects.create_superuser(
            username="Kelvin", email="kelvin@murage.com", password="kelvinpassword"
        )

        cls.alvin = cls.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword",
        )

        cls.christine = cls.User.objects.create_user(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword",
        )

        cls.abigael = Child.objects.create(
            slug="AbigaelAuma",
            full_name="Abigael Auma",
            dob="2015-05-14",
            gender="F",
            created_by=cls.alvin,
        )

        cls.brian = Child.objects.create(
            slug="BrianKimani",
            full_name="Brian Kimani",
            dob="2018-09-23",
            gender="M",
            created_by=cls.christine,
        )

        cls.mother = RelationshipType.objects.create(name="mother")
        cls.father = RelationshipType.objects.create(name="father")

        cls.abigael_father = ParentChildRelationship(
            parent=cls.alvin,
            child=cls.abigael,
            relationship_type=cls.father,
            created_by=cls.alvin,
        )
        cls.abigael_father.save()

        cls.brian_mother = ParentChildRelationship(
            parent=cls.christine,
            child=cls.brian,
            relationship_type=cls.mother,
            created_by=cls.christine,
        )
        cls.brian_mother.save()

    def test_family_member_relationship_type_object_name(self):
        self.assertEqual(f"{self.brian}'s {self.mother}", str(self.brian_mother))

    # child
    def test_child_label(self):
        child__meta = self.abigael_father._meta.get_field("child")
        self.assertEqual(child__meta.verbose_name, "child")

    def test_child_max_length(self):
        child__meta = self.abigael_father._meta.get_field("child")
        self.assertIsNone(child__meta.max_length)

    def test_child_is_null(self):
        child__meta = self.abigael_father._meta.get_field("child")
        self.assertFalse(child__meta.null)

    def test_child_is_blank(self):
        child__meta = self.abigael_father._meta.get_field("child")
        self.assertFalse(child__meta.blank)

    # parent
    def test_parent_label(self):
        parent__meta = self.abigael_father._meta.get_field("parent")
        self.assertEqual(parent__meta.verbose_name, "parent")

    def test_parent_max_length(self):
        parent__meta = self.abigael_father._meta.get_field("parent")
        self.assertIsNone(parent__meta.max_length)

    def test_parent_is_null(self):
        parent__meta = self.abigael_father._meta.get_field("parent")
        self.assertFalse(parent__meta.null)

    def test_parent_is_blank(self):
        parent__meta = self.abigael_father._meta.get_field("parent")
        self.assertFalse(parent__meta.blank)

    # relationship type
    def test_relationship_type_label(self):
        relationship_type__meta = self.abigael_father._meta.get_field(
            "relationship_type"
        )
        self.assertEqual(relationship_type__meta.verbose_name, "relationship type")

    def test_relationship_type_max_length(self):
        relationship_type__meta = self.abigael_father._meta.get_field(
            "relationship_type"
        )
        self.assertIsNone(relationship_type__meta.max_length)

    def test_relationship_type_is_null(self):
        relationship_type__meta = self.abigael_father._meta.get_field(
            "relationship_type"
        )
        self.assertFalse(relationship_type__meta.null)

    def test_relationship_type_is_blank(self):
        relationship_type__meta = self.abigael_father._meta.get_field(
            "relationship_type"
        )
        self.assertFalse(relationship_type__meta.blank)

        # created by

    def test_created_by_label(self):
        created_by__meta = self.abigael_father._meta.get_field("created_by")
        self.assertEqual(created_by__meta.verbose_name, "created by")

    def test_created_by_max_length(self):
        created_by__meta = self.abigael_father._meta.get_field("created_by")
        self.assertIsNone(created_by__meta.max_length)

    def test_created_by_is_null(self):
        created_by__meta = self.abigael_father._meta.get_field("created_by")
        self.assertTrue(created_by__meta.null)

    def test_created_by_is_blank(self):
        created_by__meta = self.abigael_father._meta.get_field("created_by")
        self.assertFalse(created_by__meta.blank)

    # updated by
    def test_updated_by_label(self):
        updated_by__meta = self.abigael_father._meta.get_field("updated_by")
        self.assertEqual(updated_by__meta.verbose_name, "updated by")

    def test_updated_by_max_length(self):
        updated_by__meta = self.abigael_father._meta.get_field("updated_by")
        self.assertIsNone(updated_by__meta.max_length)

    def test_updated_by_is_null(self):
        updated_by__meta = self.abigael_father._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.null)

    def test_updated_by_is_blank(self):
        updated_by__meta = self.abigael_father._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.blank)
