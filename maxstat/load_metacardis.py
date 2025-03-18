import pandas as pd
import numpy as np
import scipy.stats
from functools import reduce

def load_and_merge_csvs(*choices):
    """
    Load clients.csv, microbes.csv, metabolites.csv, and transformed_diet_df.csv.
    Merge selected datasets (at least 2, up to 4) based on the 'ID' column using an inner merge.
    Apply CLR transformation to microbes and food_abundance datasets.
    Filter features that are non-zero in at least 90% of the microbes and 95% foods.
    
    Parameters:
        *choices (str): Names of datasets to merge ('clients', 'microbes', 'metabolites', 'food_abundance').
                        Must provide at least 2 and no more than 4.
        
    Returns:
        pd.DataFrame: Merged DataFrame organized by the 'ID' column.
    """
    
    # Validate the number of choices
    if len(choices) < 2 or len(choices) > 4:
        raise ValueError("You must provide at least 2 and no more than 4 dataset choices.")
    
    # Load datasets
    clients = pd.read_csv("data/clients.csv")
    microbes = pd.read_csv("data/microbes.csv")
    metabolites = pd.read_csv("data/metabolites.csv")
    food_abundance = pd.read_csv("data/transformed_diet_df.csv")

    # Function to apply CLR transformation after handling zeros
    def apply_clr(df, features, zero_threshold):
        # Add a small pseudo-count to avoid zeros
        df[features] = df[features] + 0.0000001
        
        # Calculate geometric mean
        df['gmean'] = df[features].apply(scipy.stats.mstats.gmean, axis=1, nan_policy='omit')
        
        # Apply CLR transformation: divide by gmean and log transform
        df[features] = np.log(df[features].divide(df['gmean'], axis=0))
        df.drop(columns='gmean', inplace=True)
        
        # Replace originally zero values with NaN
        zero_mask = df[features] == np.log(0.0000001)
        df[features] = df[features].mask(zero_mask, np.nan)
        
        # Filter features with more than the threshold proportion of zeros
        bad = df[features].isna().sum() / df.shape[0] > zero_threshold
        columns_to_drop = [col for col, to_drop in zip(features, bad) if to_drop]
        df = df.drop(columns=columns_to_drop)
        
        return df

    # Prep microbes dataframe
    microbes.columns = microbes.columns.str.replace('.', '_')
    microbes = microbes.dropna()
    microbe_features = microbes.columns[3:].tolist()
    microbes = microbes.rename(columns={col: col.lower() for col in microbe_features})
    microbe_features = [microbe.lower() for microbe in microbe_features]
    microbes = microbes.drop_duplicates(subset=['ID'])

    # Apply CLR transformation to microbes
    microbes = apply_clr(microbes, microbe_features, zero_threshold=0.90)

    # Prep food abundance dataframe
    foods = food_abundance.fillna(0)
    food_features = [col for col in foods.columns if col.startswith("food_id_")]

    # Apply CLR transformation to food abundance
    foods = apply_clr(foods, food_features, zero_threshold=0.95)

    print("Microbes shape:", microbes.shape)
    print("Food abundance shape:", foods.shape)
    
    # Dictionary to map names to DataFrames
    datasets = {
        'clients': clients,
        'microbes': microbes,
        'metabolites': metabolites,
        'food_abundance': foods
    }
    
    # Ensure valid choices
    invalid_choices = set(choices) - set(datasets.keys())
    if invalid_choices:
        raise ValueError(f"Invalid dataset choices: {invalid_choices}. Choose from 'clients', 'microbes', 'metabolites', 'food_abundance'.")
    
    # Merge all selected datasets on 'ID' using an inner merge
    selected_dfs = [datasets[choice] for choice in choices]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='ID', how='inner'), selected_dfs)
    
    return merged_df

# Example usage:
# merged_df = load_and_merge_csvs('clients', 'microbes', 'food_abundance')
# merged_df = load_and_merge_csvs('clients', 'metabolites')
