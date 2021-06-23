from django.contrib.auth import get_user_model
from django.test import TestCase

from people.models import Person, RelationshipType, FamilyMemberRelationship


class PersonModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

        self.admin_user = self.User.objects.create_superuser(
            username="Kelvin",
            email="kelvin@murage.com",
            password="kelvinpassword"
        )

        self.person = Person.objects.create(
            username="Kelvin",
            full_name="Kelvin Murage",
            dob="1995-06-05",
            gender="M",
            created_by=self.admin_user
        )

    def test_person_basic(self):
        self.assertEqual(self.person.username, "Kelvin")
        self.assertEqual(self.person.full_name, "Kelvin Murage")
        self.assertEqual(self.person.dob,"1995-06-05")
        self.assertEqual(self.person.gender, "M")
        self.assertEqual(
            self.person.created_by,
            self.admin_user
        )

    # class methods
    def test_person_object_name_is_username(self):
        self.assertEqual(self.person.username, str(self.person))

    # username
    def test_username_label(self):
        username__meta = self.person._meta.get_field('username')
        self.assertEqual(username__meta.verbose_name, 'username')

    def test_username_max_length(self):
        username__meta = self.person._meta.get_field('username')
        self.assertEqual(username__meta.max_length, 150)

    def test_username_is_not_null(self):
        username__meta = self.person._meta.get_field('username')
        self.assertEqual(username__meta.null, False)

    def test_username_is_not_blank(self):
        username__meta = self.person._meta.get_field('username')
        self.assertEqual(username__meta.blank, False)

    # full name
    def test_full_name_label(self):
        full_name__meta = self.person._meta.get_field('full_name')
        self.assertEqual(full_name__meta.verbose_name, 'full name')

    def test_full_name_max_length(self):
        full_name__meta = self.person._meta.get_field('full_name')
        self.assertEqual(full_name__meta.max_length, 300)

    def test_full_name_is_not_null(self):
        full_name__meta = self.person._meta.get_field('full_name')
        self.assertEqual(full_name__meta.null, False)

    def test_full_name_is_not_blank(self):
        full_name__meta = self.person._meta.get_field('full_name')
        self.assertEqual(full_name__meta.blank, False)

    # date of birth
    def test_dob_label(self):
        dob__meta = self.person._meta.get_field('dob')
        self.assertEqual(dob__meta.verbose_name, 'date of birth')

    def test_dob_max_length(self):
        dob__meta = self.person._meta.get_field('dob')
        self.assertIsNone(dob__meta.max_length)

    def test_dob_is_not_null(self):
        dob__meta = self.person._meta.get_field('dob')
        self.assertEqual(dob__meta.null, False)

    def test_dob_is_not_blank(self):
        dob__meta = self.person._meta.get_field('dob')
        self.assertEqual(dob__meta.blank, False)

    # gender
    def test_gender_label(self):
        gender__meta = self.person._meta.get_field('gender')
        self.assertEqual(gender__meta.verbose_name, 'gender')

    def test_gender_max_length(self):
        gender__meta = self.person._meta.get_field('gender')
        self.assertTrue(gender__meta.max_length, 2)

    def test_gender_is_not_null(self):
        gender__meta = self.person._meta.get_field('gender')
        self.assertEqual(gender__meta.null, False)

    def test_gender_is_not_blank(self):
        gender__meta = self.person._meta.get_field('gender')
        self.assertEqual(gender__meta.blank, False)

    # created by
    def test_created_by_label(self):
        created_by__meta = self.person._meta.get_field('created_by')
        self.assertEqual(created_by__meta.verbose_name, 'created by')

    def test_created_by_max_length(self):
        created_by__meta = self.person._meta.get_field('created_by')
        self.assertIsNone(created_by__meta.max_length)

    def test_created_by_is_not_null(self):
        created_by__meta = self.person._meta.get_field('created_by')
        self.assertEqual(created_by__meta.null, False)

    def test_created_by_is_not_blank(self):
        created_by__meta = self.person._meta.get_field('created_by')
        self.assertEqual(created_by__meta.blank, False)


class RelationshipTypeTestCase(TestCase):
    def setUp(self):
        self.son = RelationshipType.objects.create(name='son')

    def test_relationship_type_basic(self):
        self.assertEqual(self.son.name, 'son')

    def test_relationship_type_object_name_is_name(self):
        self.assertEqual(self.son.name, str(self.son))

    # name
    def test_name_label(self):
        name__meta = self.son._meta.get_field('name')
        self.assertEqual(name__meta.verbose_name, 'name')

    def test_name_max_length(self):
        name__meta = self.son._meta.get_field('name')
        self.assertEqual(name__meta.max_length, 50)

    def test_name_is_not_null(self):
        name__meta = self.son._meta.get_field('name')
        self.assertEqual(name__meta.null, False)

    def test_name_is_not_blank(self):
        name__meta = self.son._meta.get_field('name')
        self.assertEqual(name__meta.blank, False)


class FamilyMemberRelationshipModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

        self.admin_user = self.User.objects.create_superuser(
            username="Kelvin",
            email="kelvin@murage.com",
            password="kelvinpassword"
        )

        self.alvin_user = self.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword"
        )

        self.christine_user = self.User.objects.create_user(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword"
        )

        self.kelvin_person = Person.objects.create(
            username="Kelvin",
            full_name="Kelvin Murage",
            dob="1995-06-05",
            gender="M",
            created_by=self.admin_user,
        )

        self.alvin_person = Person.objects.create(
            username="AlvinMukuna",
            full_name="Alvin Mukuna",
            dob="1984-12-12",
            gender="M",
            created_by=self.alvin_user,
        )

        self.abigael_person = Person.objects.create(
            username="AbigaelAuma",
            full_name="Abigael Auma",
            dob="2015-05-14",
            gender="F",
            created_by=self.alvin_user,
        )

        self.christine_person = Person.objects.create(
            username="ChristineKyalo",
            full_name="Christine Kyalo",
            dob="1992-03-21",
            gender="F",
            created_by=self.christine_user,
        )

        self.brian_person = Person.objects.create(
            username="BrianKimani",
            full_name="Brian Kimani",
            dob="2018-09-23",
            gender="M",
            created_by=self.christine_user,
        )

        self.son = RelationshipType.objects.create(name='son')
        self.daughter = RelationshipType.objects.create(name='daughter')

        self.alvin_daughter = FamilyMemberRelationship(
            person=self.alvin_person,
            relative=self.abigael_person,
            relationship_type=self.daughter
        )
        self.alvin_daughter.save()

        self.christine_son = FamilyMemberRelationship(
            person=self.christine_person,
            relative=self.brian_person,
            relationship_type=self.son
        )
        self.christine_son.save()

    def test_family_member_relationship_type_object_name(self):
        self.assertEqual(
            f"{self.christine_person}'s {self.son}",
            str(self.christine_son)
        )

    # person
    def test_person_label(self):
        person__meta = self.alvin_daughter._meta.get_field('person')
        self.assertEqual(person__meta.verbose_name, 'person')

    def test_person_max_length(self):
        person__meta = self.alvin_daughter._meta.get_field('person')
        self.assertIsNone(person__meta.max_length)

    def test_person_is_not_null(self):
        person__meta = self.alvin_daughter._meta.get_field('person')
        self.assertEqual(person__meta.null, False)

    def test_person_is_not_blank(self):
        person__meta = self.alvin_daughter._meta.get_field('person')
        self.assertEqual(person__meta.blank, False)

    # relative
    def test_relative_label(self):
        relative__meta = self.alvin_daughter._meta.get_field('relative')
        self.assertEqual(relative__meta.verbose_name, 'relative')

    def test_relative_max_length(self):
        relative__meta = self.alvin_daughter._meta.get_field('relative')
        self.assertIsNone(relative__meta.max_length)

    def test_relative_is_not_null(self):
        relative__meta = self.alvin_daughter._meta.get_field('relative')
        self.assertEqual(relative__meta.null, False)

    def test_relative_is_not_blank(self):
        relative__meta = self.alvin_daughter._meta.get_field('relative')
        self.assertEqual(relative__meta.blank, False)

    # relationship type
    def test_relationship_type_label(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field('relationship_type')
        self.assertEqual(relationship_type__meta.verbose_name, 'relationship type')

    def test_relationship_type_max_length(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field('relationship_type')
        self.assertIsNone(relationship_type__meta.max_length)

    def test_relationship_type_is_not_null(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field('relationship_type')
        self.assertEqual(relationship_type__meta.null, False)

    def test_relationship_type_is_not_blank(self):
        relationship_type__meta = self.alvin_daughter._meta.get_field('relationship_type')
        self.assertEqual(relationship_type__meta.blank, False)
