from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import Person


class PersonFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = Person

    username = Faker("user_name")
    full_name = Faker("name")
