import unittest

from utils.config import list_of_tuples


class ConfigUtilsTestCase(unittest.TestCase):
    def test_list_of_tuples_with_valid_input(self):
        admins = [("Admin", "admin@example.com"), ("Manager", "manager@example.com")]
        self.assertListEqual(admins, list_of_tuples(str(admins)))
