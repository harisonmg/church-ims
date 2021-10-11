from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from faker import Faker

from accounts import factories


class GroupFactoryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_name(self):
        group = factories.GroupFactory()
        saved_group = Group.objects.first()
        self.assertEqual(saved_group.name, group.name)

    def test_permissions(self):
        add_permissions = Permission.objects.filter(name__icontains="can add")
        group = factories.GroupFactory(permissions=tuple(add_permissions))
        self.assertQuerysetEqual(group.permissions.all(), add_permissions)


class UserFactoryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.fake = Faker()
        cls.user_password = cls.fake.password()
        cls.user = factories.UserFactory(password=cls.user_password)

    def test_username(self):
        saved_user = get_user_model().objects.first()
        self.assertEqual(saved_user.username, self.user.username)

    def test_email(self):
        saved_user = get_user_model().objects.first()
        self.assertEqual(saved_user.email, self.user.email)

    def test_password(self):
        saved_user = get_user_model().objects.first()
        self.assertEqual(saved_user.password, self.user.password)
        self.assertNotEqual(saved_user.password, self.user_password)

    def test_is_superuser(self):
        saved_user = get_user_model().objects.first()
        self.assertFalse(saved_user.is_superuser)

    def test_is_staff(self):
        saved_user = get_user_model().objects.first()
        self.assertFalse(saved_user.is_staff)

    def test_is_active(self):
        saved_user = get_user_model().objects.first()
        self.assertTrue(saved_user.is_active)

    def test_groups(self):
        # get permissions
        add_permissions = Permission.objects.filter(name__icontains="can add")
        change_permissions = Permission.objects.filter(name__icontains="can change")
        delete_permissions = Permission.objects.filter(name__icontains="can delete")
        editor_permissions = add_permissions | change_permissions

        # create groups
        admins_group = factories.GroupFactory(permissions=tuple(delete_permissions))
        editors_group = factories.GroupFactory(permissions=tuple(editor_permissions))
        all_groups = [admins_group, editors_group]

        # create user
        user = factories.UserFactory(groups=(admins_group, editors_group))
        user_groups = sorted(list(user.groups.all()), key=lambda g: g.name)
        self.assertEqual(user_groups, all_groups)

    def test_user_permissions(self):
        change_permissions = Permission.objects.filter(name__icontains="can change")
        user = factories.UserFactory(user_permissions=tuple(change_permissions))
        self.assertQuerysetEqual(user.user_permissions.all(), change_permissions)


class AdminUserFactoryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = factories.AdminUserFactory()

    def test_is_superuser(self):
        saved_user = get_user_model().objects.first()
        self.assertTrue(saved_user.is_superuser)

    def test_is_staff(self):
        saved_user = get_user_model().objects.first()
        self.assertTrue(saved_user.is_staff)
