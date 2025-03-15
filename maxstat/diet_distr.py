import pandas as pd

def diet_distr(df):
    """ This is a function that takes in a dataframe of diet distribution data, reformats it, 
    and outputs the reformatted dataframe"""
    # Replace 'Herbs and spices' with 'Herbs and Spices'
    df['food_group'] = df['food_group'].replace('Herbs and spices', 'Herbs and Spices')

    # Create a food index based on the sample_id
    df['food_idx'] = df.groupby('sample_id').cumcount() + 1

    # Aggregate the data based on sample_id and food_idx
    agg_df = df.groupby(['sample_id', 'food_idx'], as_index=False).agg({
        'food_id': 'first',
        'food_subgroup': 'first',
        'wikipedia_id': 'first',
        'food_group': 'first',
        'relative_abundance': 'mean',
        'total_reads': 'sum'
    })

    # Reshape the aggregated DataFrame using pivot
    reshaped_df = agg_df.pivot(index='sample_id', columns='food_idx', 
                               values=['food_id', 'wikipedia_id', 'food_group', 'food_subgroup', 'relative_abundance', 'total_reads'])

    # Flatten the multi-level columns from pivot
    reshaped_df.columns = [f"{col[0]}_{col[1]}" for col in reshaped_df.columns]

    # Reset index to make sample_id a column again
    reshaped_df = reshaped_df.reset_index()

    return reshaped_df
