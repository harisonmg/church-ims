from django.contrib.auth import get_user_model
from django.test import TestCase
from people.models import FamilyRelationship, Person, RelationshipType


class PersonModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

        cls.admin_user = cls.User.objects.create_superuser(
            username="Kelvin", email="kelvin@murage.com", password="kelvinpassword"
        )

        cls.person = Person.objects.create(
            slug="Kelvin",
            full_name="Kelvin Murage",
            dob="1995-06-05",
            gender="M",
            created_by=cls.admin_user,
        )

    def test_person_basic(self):
        self.assertEqual(self.person.slug, "Kelvin")
        self.assertEqual(self.person.full_name, "Kelvin Murage")
        self.assertEqual(self.person.dob, "1995-06-05")
        self.assertEqual(self.person.gender, "M")
        self.assertEqual(self.person.created_by, self.admin_user)

    # class methods
    def test_person_object_name_is_slug(self):
        self.assertEqual(self.person.slug, str(self.person))

    # slug
    def test_slug_label(self):
        slug__meta = self.person._meta.get_field("slug")
        self.assertEqual(slug__meta.verbose_name, "username")

    def test_slug_max_length(self):
        slug__meta = self.person._meta.get_field("slug")
        self.assertEqual(slug__meta.max_length, 50)

    def test_slug_is_null(self):
        slug__meta = self.person._meta.get_field("slug")
        self.assertFalse(slug__meta.null)

    def test_slug_is_blank(self):
        slug__meta = self.person._meta.get_field("slug")
        self.assertFalse(slug__meta.blank)

    # full name
    def test_full_name_label(self):
        full_name__meta = self.person._meta.get_field("full_name")
        self.assertEqual(full_name__meta.verbose_name, "full name")

    def test_full_name_max_length(self):
        full_name__meta = self.person._meta.get_field("full_name")
        self.assertEqual(full_name__meta.max_length, 300)

    def test_full_name_is_null(self):
        full_name__meta = self.person._meta.get_field("full_name")
        self.assertFalse(full_name__meta.null)

    def test_full_name_is_blank(self):
        full_name__meta = self.person._meta.get_field("full_name")
        self.assertFalse(full_name__meta.blank)

    # date of birth
    def test_dob_label(self):
        dob__meta = self.person._meta.get_field("dob")
        self.assertEqual(dob__meta.verbose_name, "date of birth")

    def test_dob_max_length(self):
        dob__meta = self.person._meta.get_field("dob")
        self.assertIsNone(dob__meta.max_length)

    def test_dob_is_null(self):
        dob__meta = self.person._meta.get_field("dob")
        self.assertFalse(dob__meta.null)

    def test_dob_is_blank(self):
        dob__meta = self.person._meta.get_field("dob")
        self.assertFalse(dob__meta.blank)

    # gender
    def test_gender_label(self):
        gender__meta = self.person._meta.get_field("gender")
        self.assertEqual(gender__meta.verbose_name, "gender")

    def test_gender_max_length(self):
        gender__meta = self.person._meta.get_field("gender")
        self.assertTrue(gender__meta.max_length, 2)

    def test_gender_is_null(self):
        gender__meta = self.person._meta.get_field("gender")
        self.assertFalse(gender__meta.null)

    def test_gender_is_blank(self):
        gender__meta = self.person._meta.get_field("gender")
        self.assertFalse(gender__meta.blank)

    # created by
    def test_created_by_label(self):
        created_by__meta = self.person._meta.get_field("created_by")
        self.assertEqual(created_by__meta.verbose_name, "created by")

    def test_created_by_max_length(self):
        created_by__meta = self.person._meta.get_field("created_by")
        self.assertIsNone(created_by__meta.max_length)

    def test_created_by_is_null(self):
        created_by__meta = self.person._meta.get_field("created_by")
        self.assertTrue(created_by__meta.null)

    def test_created_by_is_blank(self):
        created_by__meta = self.person._meta.get_field("created_by")
        self.assertFalse(created_by__meta.blank)

    # updated by
    def test_updated_by_label(self):
        updated_by__meta = self.person._meta.get_field("updated_by")
        self.assertEqual(updated_by__meta.verbose_name, "updated by")

    def test_updated_by_max_length(self):
        updated_by__meta = self.person._meta.get_field("updated_by")
        self.assertIsNone(updated_by__meta.max_length)

    def test_updated_by_is_null(self):
        updated_by__meta = self.person._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.null)

    def test_updated_by_is_blank(self):
        updated_by__meta = self.person._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.blank)


class RelationshipTypeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.son = RelationshipType.objects.create(name="son")

    def test_relationship_type_basic(self):
        self.assertEqual(self.son.name, "son")

    def test_relationship_type_object_name_is_name(self):
        self.assertEqual(self.son.name, str(self.son))

    # name
    def test_name_label(self):
        name__meta = self.son._meta.get_field("name")
        self.assertEqual(name__meta.verbose_name, "name")

    def test_name_max_length(self):
        name__meta = self.son._meta.get_field("name")
        self.assertEqual(name__meta.max_length, 50)

    def test_name_is_null(self):
        name__meta = self.son._meta.get_field("name")
        self.assertFalse(name__meta.null)

    def test_name_is_blank(self):
        name__meta = self.son._meta.get_field("name")
        self.assertFalse(name__meta.blank)


class FamilyRelationshipModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User = get_user_model()

        cls.admin_user = cls.User.objects.create_superuser(
            username="Kelvin", email="kelvin@murage.com", password="kelvinpassword"
        )

        cls.alvin_user = cls.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword",
        )

        cls.christine_user = cls.User.objects.create_user(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword",
        )

        cls.kelvin_person = Person.objects.create(
            slug="Kelvin",
            full_name="Kelvin Murage",
            dob="1995-06-05",
            gender="M",
            created_by=cls.admin_user,
        )

        cls.alvin_person = Person.objects.create(
            slug="AlvinMukuna",
            full_name="Alvin Mukuna",
            dob="1984-12-12",
            gender="M",
            created_by=cls.alvin_user,
        )

        cls.abigael_person = Person.objects.create(
            slug="AbigaelAuma",
            full_name="Abigael Auma",
            dob="2015-05-14",
            gender="F",
            created_by=cls.alvin_user,
        )

        cls.christine_person = Person.objects.create(
            slug="ChristineKyalo",
            full_name="Christine Kyalo",
            dob="1992-03-21",
            gender="F",
            created_by=cls.christine_user,
        )

        cls.brian_person = Person.objects.create(
            slug="BrianKimani",
            full_name="Brian Kimani",
            dob="2018-09-23",
            gender="M",
            created_by=cls.christine_user,
        )

        cls.son = RelationshipType.objects.create(name="son")
        cls.daughter = RelationshipType.objects.create(name="daughter")

        cls.alvin_daughter = FamilyRelationship(
            person=cls.alvin_person,
            relative=cls.abigael_person,
            relationship_type=cls.daughter,
            created_by=cls.alvin_user,
        )
        cls.alvin_daughter.save()

        cls.christine_son = FamilyRelationship(
            person=cls.christine_person,
            relative=cls.brian_person,
            relationship_type=cls.son,
            created_by=cls.christine_user,
        )
        cls.christine_son.save()

    def test_family_member_relationship_type_object_name(self):
        self.assertEqual(
            f"{self.christine_person}'s {self.son}", str(self.christine_son)
        )

    # person
    def test_person_label(self):
        person__meta = self.alvin_daughter._meta.get_field("person")
        self.assertEqual(person__meta.verbose_name, "person")

    def test_person_max_length(self):
        person__meta = self.alvin_daughter._meta.get_field("person")
        self.assertIsNone(person__meta.max_length)

    def test_person_is_null(self):
        person__meta = self.alvin_daughter._meta.get_field("person")
        self.assertFalse(person__meta.null)

    def test_person_is_blank(self):
        person__meta = self.alvin_daughter._meta.get_field("person")
        self.assertFalse(person__meta.blank)

    # relative
    def test_relative_label(self):
        relative__meta = self.alvin_daughter._meta.get_field("relative")
        self.assertEqual(relative__meta.verbose_name, "relative")

    def test_relative_max_length(self):
        relative__meta = self.alvin_daughter._meta.get_field("relative")
        self.assertIsNone(relative__meta.max_length)

    def test_relative_is_null(self):
        relative__meta = self.alvin_daughter._meta.get_field("relative")
        self.assertFalse(relative__meta.null)

    def test_relative_is_blank(self):
        relative__meta = self.alvin_daughter._meta.get_field("relative")
        self.assertFalse(relative__meta.blank)

    # relationship type
    def test_relationship_type_label(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field(
            "relationship_type"
        )
        self.assertEqual(relationship_type__meta.verbose_name, "relationship type")

    def test_relationship_type_max_length(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field(
            "relationship_type"
        )
        self.assertIsNone(relationship_type__meta.max_length)

    def test_relationship_type_is_null(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field(
            "relationship_type"
        )
        self.assertFalse(relationship_type__meta.null)

    def test_relationship_type_is_blank(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field(
            "relationship_type"
        )
        self.assertFalse(relationship_type__meta.blank)

        # created by

    def test_created_by_label(self):
        created_by__meta = self.alvin_daughter._meta.get_field("created_by")
        self.assertEqual(created_by__meta.verbose_name, "created by")

    def test_created_by_max_length(self):
        created_by__meta = self.alvin_daughter._meta.get_field("created_by")
        self.assertIsNone(created_by__meta.max_length)

    def test_created_by_is_null(self):
        created_by__meta = self.alvin_daughter._meta.get_field("created_by")
        self.assertTrue(created_by__meta.null)

    def test_created_by_is_blank(self):
        created_by__meta = self.alvin_daughter._meta.get_field("created_by")
        self.assertFalse(created_by__meta.blank)

    # updated by
    def test_updated_by_label(self):
        updated_by__meta = self.alvin_daughter._meta.get_field("updated_by")
        self.assertEqual(updated_by__meta.verbose_name, "updated by")

    def test_updated_by_max_length(self):
        updated_by__meta = self.alvin_daughter._meta.get_field("updated_by")
        self.assertIsNone(updated_by__meta.max_length)

    def test_updated_by_is_null(self):
        updated_by__meta = self.alvin_daughter._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.null)

    def test_updated_by_is_blank(self):
        updated_by__meta = self.alvin_daughter._meta.get_field("updated_by")
        self.assertTrue(updated_by__meta.blank)
