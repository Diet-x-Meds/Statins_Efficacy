import pandas as pd
import unittest
from regression import linear_regression_results

class TestRegression(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to check that function runs without error"""
        df = pd.read_csv('./data/microbes_cov.csv')
        try:
            formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "C(Status) + Activity + Microbial_load + Statin*{independent_feature}"
            result = linear_regression_results(['HMG'], ['clostridium_bolteae_cag00008'],
                              formula_string, df)
        except Exception as e:
            self.fail(f"linear_regression_results raised an exception: {e}")

    def test_one_shot(self):
        """Test that output DataFrame contains expected columns"""
        df = pd.read_csv('./data/microbes_cov.csv')
        expected_cols = ["dependent_feature", "independent_feature",
                         "beta", "t_statistic", "p", "n","formula"]

        formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "C(Status) + Activity + Microbial_load + Statin*{independent_feature}"

        associations = linear_regression_results(['HMG'], ['clostridium_bolteae_cag00008'],
                              formula_string, df)
        
        # Check if all expected columns exist in associations DataFrame
        self.assertTrue(set(expected_cols).issubset(set(associations.columns)),
                        "Not all expected columns are present in output DataFrame.")

    def test_edge(self):
        """Test that categorical independent variable raises an appropriate error"""
        df = pd.read_csv('./data/microbes_cov.csv')

        formula_string = "{dependent_feature} ~ C(Gender) + Age + BMI + C(Nationality) +" \
            "+ Activity + Microbial_load + Statin*{independent_feature}"

        with self.assertRaises(ValueError):
            # Status is a categorical variable
            # Passing it in as the independent feature will raise error
            linear_regression_results(['HMG'], ['Status'],
                                      formula_string, df)

if __name__ == '__main__':
    unittest.main()
