import pandas as pd
import unittest
from maxstat.diet_tables import diet_tables

class TestDescribeDataframe(unittest.TestCase):

    def test_smoke(self):
        """ smoke test to make sure function runs"""
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe and ensure it doesn't go up in smoke
        diet_tables(df)

    def test_one_shot(self):
        """ test to see outputted dataframe is expected shape"""
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe to the function
        food_group_counts_df, food_subgroup_counts_df, wikipedia_id_counts_df = diet_tables(df)
        # Assert that food_group_counts_df has the expected shape 
        expected_shape = (13, 3)  
        self.assertEqual(food_group_counts_df.shape, expected_shape)
        
    def test_edge(self):
        """test for unexpected column in dataframe; should fail""" 
        # Load dataframe
        df = pd.read_csv('./data/combined_food_abundance.csv')
        # Feed in the dataframe and check that it throws a ValueError when an invalid column is requested
        with self.assertRaises(KeyError):
            food_group_counts_df, food_subgroup_counts_df, wikipedia_id_counts_df = diet_tables(df)
            food_group = wikipedia_id_counts_df["food_group"].tolist()

if __name__ == '__main__':
    unittest.main()
