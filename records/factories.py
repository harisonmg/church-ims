from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from people.factories import PersonFactory

from .models import TemperatureRecord


class TemperatureRecordFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = TemperatureRecord

    person = SubFactory(PersonFactory)
    body_temperature = Faker("pydecimal", right_digits=2, min_value=35, max_value=38)
