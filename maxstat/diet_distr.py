import pandas as pd

def diet_distr(df):
    """ This is a function that takes in a dataframe of food abundance data and reformats it for better downstream processing. 
    Each patient now has one row with a columns for new foods"""

    #Replaces 'Herbs and spices' with 'Herbs and Spices' because there are a few mislabeled 'Herbs and spices' in this dataset
    df['food_group'] = df['food_group'].replace('Herbs and spices', 'Herbs and Spices')

    #Creates a food index based on the sample_id
    df['food_idx'] = df.groupby('sample_id').cumcount() + 1

    #Aggregates the data based on sample_id and food_idx
    agg_df = df.groupby(['sample_id', 'food_idx'], as_index=False).agg({
        'food_id': 'first',
        'food_subgroup': 'first',
        'wikipedia_id': 'first',
        'food_group': 'first',
        'relative_abundance': 'mean',
        'total_reads': 'sum'
    })

    #Reshapes the aggregated DataFrame using pivot
    reshaped_df = agg_df.pivot(index='sample_id', columns='food_idx', 
                               values=['food_id', 'wikipedia_id', 'food_group', 'food_subgroup', 'relative_abundance', 'total_reads'])

    #Flattens the multi-level columns from pivot
    reshaped_df.columns = [f"{col[0]}_{col[1]}" for col in reshaped_df.columns]

    #Resets index to make sample_id a column again
    reshaped_df = reshaped_df.reset_index()
    
    #Returns the re-shaped dataframe
    return reshaped_df
