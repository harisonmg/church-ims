from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from allauth.account.models import EmailAddress
from factory import Faker, SelfAttribute, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice


class GroupFactory(DjangoModelFactory):
    class Meta:  # noqa
        model = Group

    name = Sequence(lambda n: f"Group {n}")

    @post_generation
    def permissions(self, create, extracted):
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.permissions.add(permission)


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

    @post_generation
    def groups(self, create, extracted):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    @post_generation
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


class EmailAddressFactory(DjangoModelFactory):
    class Meta:
        model = EmailAddress

    email = SelfAttribute("user.email")
    verified = FuzzyChoice(choices=[True, False])
    primary = FuzzyChoice(choices=[True, False])
    user = SubFactory(UserFactory)


class VerifiedEmailAddressFactory(EmailAddressFactory):
    verified = True
