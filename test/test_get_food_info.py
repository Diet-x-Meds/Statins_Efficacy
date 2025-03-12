import numpy as np
import pandas as pd
import unittest
from maxstat.get_food_info import get_food_info

class TestGetFoodInfo(unittest.TestCase):

    def test_smoke(self):
        # Feed in an empty input and ensure nothing goes wrong
        df = get_food_info([])

    def test_one_shot(self):
        # Generate reference dataframe
        ref_df = pd.DataFrame({
            'food_id': [5],
            'food_name': ['Red-skinned Onion'],
            'genus': ['Allium'],
            'species': ['haematochiton'],
            'food_group': ['Vegetables'],
            'food_subgroup': ['Onion-family vegetables'],
        })
        ref_df.index = range(1, len(ref_df) + 1)

        # Test a valid integer input and check that the output is as expected
        df = get_food_info(5)
        self.assertTrue(df.equals(ref_df))
    
    def test_one_shot_2(self):
        # Generate reference dataframe
        ref_df = pd.DataFrame({
            'food_id': [444, 918],
            'food_name': ['Plantain', 'Kabocha'],
            'genus': ['Musa', 'Cucurbita'],
            'species': ['Musa x paradisiaca', 'maxima'],
            'food_group': ['Fruits', 'Gourds'],
            'food_subgroup': ['Tropical fruits', 'Gourds'],
        })
        ref_df.index = range(1, len(ref_df) + 1)

        # Test a valid list input and check that the output is as expected
        df = get_food_info([444, 918])
        self.assertTrue(df.equals(ref_df))

    def test_one_shot_3(self):
        # Generate reference dataframe
        ref_df = pd.DataFrame({
            'food_id': [5],
            'food_name': ['Red-skinned Onion'],
            'genus': ['Allium'],
            'species': ['haematochiton'],
            'food_group': ['Vegetables'],
            'food_subgroup': ['Onion-family vegetables'],
        })
        ref_df.index = range(1, len(ref_df) + 1)

        # Test a valid 1D np.ndarray with duplicate IDs and check that the output is not duplicate
        df = get_food_info(np.array([5, 5]))
        self.assertTrue(df.equals(ref_df))

    def test_one_shot_4(self):
        # Load the entire dataset and check that an empty input gives the desired outcome
        ref_df = pd.read_csv('data/annotated_food_matches.csv', index_col=False)
        ref_df.index = range(1, len(ref_df) + 1)

        df = get_food_info(np.array([]))
        self.assertTrue(df.equals(ref_df))

    def test_one_shot_5(self):
        # Generate reference dataframe
        ref_df = pd.DataFrame({
            'food_id': [5],
            'food_name': ['Red-skinned Onion'],
            'genus': ['Allium'],
            'species': ['haematochiton'],
            'food_group': ['Vegetables'],
            'food_subgroup': ['Onion-family vegetables'],
        })
        ref_df.index = range(1, len(ref_df) + 1)

        # Test a valid 1D array with a single string input
        df = get_food_info(np.array(['food_id_5']))
        self.assertTrue(df.equals(ref_df))

    def test_one_shot_6(self):
        # Generate reference dataframe
        ref_df = pd.DataFrame({
            'food_id': [444, 918],
            'food_name': ['Plantain', 'Kabocha'],
            'genus': ['Musa', 'Cucurbita'],
            'species': ['Musa x paradisiaca', 'maxima'],
            'food_group': ['Fruits', 'Gourds'],
            'food_subgroup': ['Tropical fruits', 'Gourds'],
        })
        ref_df.index = range(1, len(ref_df) + 1)

        # Test a valid list input with mixed valid types and check that the output is as expected
        df = get_food_info([444, 'food_id_918'])
        self.assertTrue(df.equals(ref_df))

    def test_edge(self):
        # Test a non-int, str, or list input and check that a TypeError is thrown
        with self.assertRaises(TypeError):
            df = get_food_info({'hi': 'hello'})
    
    def test_edge_2(self):
        # Test a jagged (non-1D) array and check that a TypeError is thrown
        with self.assertRaises(TypeError):
            df = get_food_info([[123], 123])
    
    def test_edge_3(self):
        # Test a valid integer that is not a valid food ID and check that KeyError is thrown
        with self.assertRaises(KeyError):
            df = get_food_info(1234)
    
    def test_edge_4(self):
        # Test a 1D np array with valid integers where only 1 is not a valid food ID and check that KeyError is thrown
        with self.assertRaises(KeyError):
            df = get_food_info(np.array([123, 917, 919]))
    
    def test_edge_5(self):
        # Test a float and check that TypeError is thrown
        with self.assertRaises(TypeError):
            df = get_food_info(123.0)

    def test_edge_6(self):
        # Test a string not of form "food_id_[int]" and check that TypeError is thrown
        with self.assertRaises(ValueError):
            df = get_food_info('foods_id_5')

    def test_pattern(self):
        # Test every consecutive pair of valid food IDs
        data_df = pd.read_csv('data/annotated_food_matches.csv', index_col=False)

        for i in range(len(data_df['food_id']) - 1):
            # Generate reference dataframe
            ref_df = pd.DataFrame({
                'food_id': data_df.loc[i:i+1, 'food_id'],
                'food_name': data_df.loc[i:i+1, 'food_name'],
                'genus': data_df.loc[i:i+1, 'genus'],
                'species': data_df.loc[i:i+1, 'species'],
                'food_group': data_df.loc[i:i+1, 'food_group'],
                'food_subgroup': data_df.loc[i:i+1, 'food_subgroup'],
            })
            ref_df.index = range(1, len(ref_df) + 1)

            # Test a valid 1D np.ndarray with duplicate IDs and check that the output is not duplicate
            df = get_food_info(data_df.loc[i:i+1, 'food_id'].values)
            self.assertTrue(df.equals(ref_df))
    
    def test_pattern_2(self):
        # Test every consecutive pair of valid food IDs, this time using string type inputs
        data_df = pd.read_csv('data/annotated_food_matches.csv', index_col=False)

        for i in range(len(data_df['food_id']) - 1):
            # Generate reference dataframe
            ref_df = pd.DataFrame({
                'food_id': data_df.loc[i:i+1, 'food_id'],
                'food_name': data_df.loc[i:i+1, 'food_name'],
                'genus': data_df.loc[i:i+1, 'genus'],
                'species': data_df.loc[i:i+1, 'species'],
                'food_group': data_df.loc[i:i+1, 'food_group'],
                'food_subgroup': data_df.loc[i:i+1, 'food_subgroup'],
            })
            ref_df.index = range(1, len(ref_df) + 1)

            # Test a valid 1D np.ndarray with duplicate IDs and check that the output is not duplicate
            df = get_food_info([f'food_id_{str(food_id)}' for food_id in data_df.loc[i:i+1, 'food_id'].values])
            self.assertTrue(df.equals(ref_df))

if __name__ == '__main__':
    unittest.main()