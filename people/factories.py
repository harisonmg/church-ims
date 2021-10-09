from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from factory.faker import Faker
import faker

from .constants import GENDER_CHOICES
from .models import Person


class PersonFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = Person

    username = Sequence(lambda n: faker.Faker().user_name() + str(n))
    full_name = Faker("name")
    gender = FuzzyChoice(GENDER_CHOICES, getter=lambda c: c[0])
    dob = Faker("date_of_birth")
