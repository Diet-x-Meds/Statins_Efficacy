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


if __name__ == "__main__":
    unittest.main()

