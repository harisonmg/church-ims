from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory
from factory.faker import Faker


class UserFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = get_user_model()

    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default `_create` to use the `create_user`
        helper function
        """
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class AdminUserFactory(UserFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default `_create` to use the `create_superuser`
        helper function
        """
        manager = cls._get_manager(model_class)
        return manager.create_superuser(*args, **kwargs)
