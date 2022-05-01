import unittest

import numpy as np

from common_lib import commons


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print("Running Test")
    def test_distillation_profile_scrape(self):
        actual = commons.retrieve_distillation_profile("BCL")
        expected = ['IBP','5','10','20','30','40','50','60','70','80','90','95','99']
        self.assertEqual(actual["mass_recovered"].tolist(), expected, "Failure to scrape distillation profile")

    def test_distillation_profile_calculation(self):
        crude_one = commons.retrieve_distillation_profile("BCL","2014-11-30")
        crude_two = commons.retrieve_distillation_profile("MBL","2020-07-10")

        df_crude_one = crude_one.replace('-', np.nan)
        df_crude_two = crude_two.replace('-', np.nan)

        actual = commons.calculate_distillation_profile(df_crude_one, df_crude_two)
        expected = [52.60,77.15,122.30,160.70,211.55,276.05,340.60,408.30,499.65,640.65]
        self.assertEqual(actual["temperature"].dropna().tolist(), expected, "distillation profile calculation went "
                                                                            "wrong")


if __name__ == '__main__':
    unittest.main()