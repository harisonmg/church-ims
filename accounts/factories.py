from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import factory


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:  # noqa
        model = Group

    name = factory.Sequence(lambda n: f"Group {n}")

    @factory.post_generation
    def permissions(self, create, extracted):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.permissions.add(permission)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:  # noqa
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default `_create` to use the `create_user`
        helper function
        """
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def groups(self, create, extracted):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def user_permissions(self, create, extracted):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.user_permissions.add(permission)


class AdminUserFactory(UserFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default `_create` to use the `create_superuser`
        helper function
        """
        manager = cls._get_manager(model_class)
        return manager.create_superuser(*args, **kwargs)
