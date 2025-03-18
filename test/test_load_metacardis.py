import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
from functools import reduce
from maxstat.load_metacardis import load_and_merge_csvs

class TestDescribeDataframe(unittest.TestCase):

    def test_smoke(self):
        """Smoke Test: Ensure function runs without crashing."""
        try:
            result = load_and_merge_csvs("clients", "microbes")
        except Exception as e:
            self.fail(f"Function raised an unexpected exception: {e}")

    def test_one_shot(self):
        """One-Shot Test: Validate expected merge output."""
        result = load_and_merge_csvs("clients", "microbes")
        self.assertGreater(result.shape[0], 0)  # Ensure at least some rows exist
        self.assertIn("ID", result.columns)  # Merged output should retain 'ID' column
        self.assertIn("Age", result.columns)  # Clients columns should exist

    def test_edge_case_invalid_choices(self):
        """Edge Test: Ensure an exception is raised for invalid dataset choices."""
        with self.assertRaises(ValueError) as context:
            load_and_merge_csvs("clients", "invalid_dataset")
        self.assertIn("Invalid dataset choices", str(context.exception))

    def test_edge_case_too_few_datasets(self):
        """Edge Test: Ensure an exception is raised for fewer than two datasets."""
        with self.assertRaises(ValueError):
            load_and_merge_csvs("clients")

    def test_edge_case_too_many_datasets(self):
        """Edge Test: Ensure an exception is raised for more than four datasets."""
        with self.assertRaises(ValueError):
            load_and_merge_csvs("clients", "microbes", "metabolites", "food_abundance", "extra")

if __name__ == "__main__":
    unittest.main()

