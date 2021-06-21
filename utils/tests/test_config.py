import unittest

import utils.config


class ConfigUtilsTestCase(unittest.TestCase):
    def test_list_of_tuples(self):
        admins = [("Admin", "admin@example.com"), ("Manager", "manager@example.com")]
        self.assertListEqual(admins, utils.config.list_of_tuples(str(admins)))
