import pandas as pd
import unittest
from maxstat.metadata_describe import metadata_describe

class TestDescribeDataframe(unittest.TestCase):

    def test_smoke(self):
        # Load dataframe
        df = pd.read_csv('./data/clients.csv')
        # Feed in the dataframe and ensure it doesn't go up in smoke
        metadata_describe(df)

    def test_one_shot(self):
        # Load dataframe
        df = pd.read_csv('./data/clients.csv')
        # Feed in the dataframe and check that it gives the requested medication summary data
        summary_df = metadata_describe(df)
        self.assertTrue("statin" in summary_df.columns)

    def test_edge(self):
        # Load dataframe
        df = pd.read_csv('./data/clients.csv')
        # Feed in the dataframe and check that it throws a ValueError when an invalid medication is requested
        with self.assertRaises(KeyError):
            summary_df = metadata_describe(df)
            flareon = summary_df["Flareon"].tolist()

if __name__ == '__main__':
    unittest.main()