import faker
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice

from . import constants
from .models import InterpersonalRelationship, Person


class PersonFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = Person

    username = Sequence(lambda n: faker.Faker().user_name() + str(n))
    full_name = Faker("name")
    gender = FuzzyChoice(choices=constants.GENDER_CHOICES, getter=lambda c: c[0])
    dob = Faker("date_of_birth", maximum_age=constants.MAX_HUMAN_AGE)


class AdultFactory(PersonFactory):
    dob = Faker("date_of_birth", minimum_age=constants.AGE_OF_MAJORITY)


class ChildFactory(PersonFactory):
    dob = Faker("date_of_birth", maximum_age=constants.AGE_OF_MAJORITY - 1)


class InterpersonalRelationshipFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = InterpersonalRelationship

    person = SubFactory(PersonFactory)
    relative = SubFactory(PersonFactory)
    relation = FuzzyChoice(
        choices=constants.INTERPERSONAL_RELATIONSHIP_CHOICES, getter=lambda c: c[0]
    )
