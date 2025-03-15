import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
from functools import reduce

class TestLoadAndMergeCSVs(unittest.TestCase):

    @patch("pandas.read_csv")
    def setUp(self, mock_read_csv):
        """Mock CSV loading to avoid dependency on actual files."""

        # Create sample mock DataFrames
        self.clients_df = pd.DataFrame({
            "ID": [1, 2, 3, 4, 5],
            "Age": [25, 30, 35, 40, 45],
            "Gender": ["M", "F", "M", "F", "M"]
        })

        self.microbes_df = pd.DataFrame({
            "ID": [1, 2, 3, 4, 5],
            "microbe_1": [0.1, 0.2, 0.3, 0.4, 0.5],
            "microbe_2": [0.5, 0.4, 0.3, 0.2, 0.1]
        })

        self.metabolites_df = pd.DataFrame({
            "ID": [1, 2, 3, 4, 5],
            "metabolite_1": [10, 20, 30, 40, 50]
        })

        self.food_abundance_df = pd.DataFrame({
            "ID": [1, 2, 3, 4, 5],
            "food_id_1": [0.05, 0.06, 0.07, 0.08, 0.09],
            "food_id_2": [0.10, 0.09, 0.08, 0.07, 0.06]
        })

        # Mock pandas read_csv return values
        mock_read_csv.side_effect = [
            self.clients_df, self.microbes_df, self.metabolites_df, self.food_abundance_df
        ]

    def test_smoke(self):
        """Smoke Test: Ensure function runs without crashing."""
        try:
            result = load_and_merge_csvs("clients", "microbes")
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")

    def test_one_shot(self):
        """One-Shot Test: Check expected merge output."""
        result = load_and_merge_csvs("clients", "microbes")
        self.assertEqual(result.shape[0], 5)  # Expecting 5 merged rows
        self.assertTrue("Age" in result.columns)  # Clients columns should exist
        self.assertTrue("microbe_1" in result.columns)  # Microbes columns should exist

    def test_edge_case_invalid_choices(self):
        """Edge Test: Ensure an exception is raised for invalid dataset choices."""
        with self.assertRaises(ValueError) as context:
            load_and_merge_csvs("clients", "invalid_dataset")
        self.assertIn("Invalid dataset choices", str(context.exception))

    def test_edge_case_too_few_datasets(self):
        """Edge Test: Ensure an exception is raised for less than two datasets."""
        with self.assertRaises(ValueError):
            load_and_merge_csvs("clients")

    def test_edge_case_too_many_datasets(self):
        """Edge Test: Ensure an exception is raised for more than four datasets."""
        with self.assertRaises(ValueError):
            load_and_merge_csvs("clients", "microbes", "metabolites", "food_abundance", "extra")

    def test_pattern_merge_consistency(self):
        """Pattern Test: Ensure merging the same datasets always returns the same IDs."""
        result1 = load_and_merge_csvs("clients", "microbes")
        result2 = load_and_merge_csvs("clients", "microbes")
        pd.testing.assert_frame_equal(result1, result2)  # Should always return the same result

    def test_pattern_clr_transformation(self):
        """Pattern Test: Ensure CLR transformation follows a known pattern."""
        result = load_and_merge_csvs("microbes", "food_abundance")
        
        # Since CLR transforms the data, values should not be exactly zero
        self.assertFalse((result.filter(like="microbe_") == 0).any().any())
        self.assertFalse((result.filter(like="food_id_") == 0).any().any())

        # Expect transformed values to be negative for low-abundance microbes
        self.assertTrue((result["microbe_1"] < 0).any())

if __name__ == "__main__":
    unittest.main()

