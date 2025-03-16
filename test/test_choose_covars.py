import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, f_oneway

class TestPlotCovariateImpactClustermap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the actual dataset for testing."""
        cls.df = pd.read_csv('./data/food_cov.csv')
        cls.dependent_var = "hba1c"
        cls.covariates = ["Age", "BMI", "C(Gender)", "Microbial_load"]

    def test_smoke(self):
        """Smoke Test: Ensure function runs without crashing."""
        try:
            plot_covariate_impact_clustermap(self.df, self.dependent_var, self.covariates)
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")

    def test_one_shot(self):
        """One-Shot Test: Ensure output is a Seaborn ClusterGrid."""
        fig = plot_covariate_impact_clustermap(self.df, self.dependent_var, self.covariates)
        self.assertIsInstance(fig, sns.matrix.ClusterGrid)

    def test_edge_case_no_covariates(self):
        """Edge Test: Function should handle an empty list of covariates gracefully."""
        with self.assertRaises(ValueError):
            plot_covariate_impact_clustermap(self.df, self.dependent_var, [])

    def test_edge_case_invalid_column(self):
        """Edge Test: Function should raise an error if given a non-existent column."""
        with self.assertRaises(KeyError):
            plot_covariate_impact_clustermap(self.df, self.dependent_var, ["Age", "non_existent_col"])
if __name__ == "__main__":
    unittest.main()
