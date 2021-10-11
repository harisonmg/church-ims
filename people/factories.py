import faker
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice

from .constants import GENDER_CHOICES, MAX_HUMAN_AGE
from .models import Person


class PersonFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = Person

    username = Sequence(lambda n: faker.Faker().user_name() + str(n))
    full_name = Faker("name")
    gender = FuzzyChoice(GENDER_CHOICES, getter=lambda c: c[0])
    dob = Faker("date_of_birth", maximum_age=MAX_HUMAN_AGE)
