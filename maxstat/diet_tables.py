import pandas as pd
from maxstat.diet_distr import diet_distr

def diet_tables(df):
    """ takes reshaped dataframe and outputs some tables about the foods"""

    #gets the re_shaped food dataframe using the diet_distr function
    reshaped_df = diet_distr(df)

    #create the list of columns for food_group, food_subgroup, and wikipedia_id
    food_group_columns = [f'food_group_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of food groups
    food_subgroup_columns = [f'food_subgroup_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of subgroups
    wikipedia_id_columns = [f'wikipedia_id_{i:.1f}' for i in range(1, 32)]  # Adjust according to the actual number of IDs
    
    # Select only the relevant columns, ensuring the names are correct
    food_group_data = reshaped_df[food_group_columns]
    food_subgroup_data = reshaped_df[food_subgroup_columns]
    wikipedia_id_data = reshaped_df[wikipedia_id_columns]
    
    # Flatten the food group data
    flattened_food_groups = food_group_data.values.flatten()
    flattened_food_subgroups = food_subgroup_data.values.flatten()
    flattened_wikipedia_id = wikipedia_id_data.values.flatten()
    
    # Count how many times each food group appears
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

    return food_group_counts_df, food_subgroup_counts_df, wikipedia_id_counts_df
