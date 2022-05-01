import unittest
from common_lib import commons


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print("Running Test1")
    def test_distillation_profile_scrape(self):
        actual = commons.retrieveDistProfile("BCL")
        expected = commons.retrieveDistProfile("BCL")
        self.assertEqual(actual["mass_recovered"].tolist(), expected["mass_recovered"].tolist())


if __name__ == '__main__':
    unittest.main()