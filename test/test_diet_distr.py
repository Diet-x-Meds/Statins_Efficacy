import pandas as pd
import unittest
from maxstat.diet_distr import diet_distr

class TestDescribeDataframe(unittest.TestCase):

    def test_smoke(self):
        """ smoke test to make sure function runs"""
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe and ensure it doesn't go up in smoke
        diet_distr(df)

    def test_one_shot(self):
        """ test to see if expected column in outputed dataframe"""
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe and check that it gives the requested column
        diet_df = diet_distr(df, ["count"])
        self.assertTrue("count" in diet_df.index)

    def test_edge(self):
        """test for unexpected column in dataframe; should fail""" 
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe and check that it throws a ValueError when an invalid column is requested
        with self.assertRaises(ValueError):
            diet_df = diet_distr(df, ["dratini"])

if __name__ == '__main__':
    unittest.main()
