import pandas as pd

def diet_distr(df):
    """ This is a function that takes in a dataframe of diet distribution data, reformats it, 
    and outputs some tables with counts"""
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

    #Dynamically create the list of columns for food_group, food_subgroup, and wikipedia_id
    food_group_columns = [f'food_group_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of food groups
    food_subgroup_columns = [f'food_subgroup_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of subgroups
    wikipedia_id_columns = [f'wikipedia_id_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of IDs
    
    #Select only the relevant columns
    food_group_data = reshaped_df[food_group_columns]
    food_subgroup_data = reshaped_df[food_subgroup_columns]
    wikipedia_id_data = reshaped_df[wikipedia_id_columns]
    
    #Flatten the food group data
    flattened_food_groups = food_group_data.values.flatten()
    flattened_food_subgroups = food_subgroup_data.values.flatten()
    flattened_wikipedia_id = wikipedia_id_data.values.flatten()
    
    #Count how many times each food group appears
    food_group_counts = pd.Series(flattened_food_groups).value_counts()
    food_subgroup_counts = pd.Series(flattened_food_subgroups).value_counts()
    wikipedia_id_counts = pd.Series(flattened_wikipedia_id).value_counts()

    food_group_counts_df = food_group_counts.reset_index()
    food_group_counts_df.columns = ['food_group', 'count']  # Rename columns for clarity
    
    food_subgroup_counts_df = food_subgroup_counts.reset_index()
    food_subgroup_counts_df.columns = ['food_subgroup', 'count']  # Rename columns for clarity
    
    wikipedia_id_counts_df = wikipedia_id_counts.reset_index()
    wikipedia_id_counts_df.columns = ['wikipedia_id', 'count']

    food_group_counts_df['percentage_of_total'] = (food_group_counts_df['count'] / food_group_counts_df['count'].sum()) * 100
    food_subgroup_counts_df['percentage_of_total'] = (food_subgroup_counts_df['count']/food_subgroup_counts_df['count'].sum()) * 100
    wikipedia_id_counts_df['percentage_of_total'] = (wikipedia_id_counts_df['count'] / wikipedia_id_counts_df['count'].sum()) * 100

    return food_group_counts_df
