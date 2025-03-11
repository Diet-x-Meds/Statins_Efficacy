import pandas as pd

def load_and_merge_csvs(choice1: str, choice2: str):
    """
    Load clients.csv, microbes.csv, metabolites.csv, and transformed_diet_df.csv.
    Merge two selected datasets based on the 'ID' column using an inner merge.
    
    Parameters:
        choice1 (str): First dataset to merge ('clients', 'microbes', 'metabolites', 'food_abundance').
        choice2 (str): Second dataset to merge ('clients', 'microbes', 'metabolites', 'food_abundance').
        
    Returns:
        pd.DataFrame: Merged DataFrame organized by the 'ID' column.
    """
    
    # Load datasets
    clients = pd.read_csv("clients.csv")
    microbes = pd.read_csv("microbes.csv")
    metabolites = pd.read_csv("metabolites.csv")
    food_abundance = pd.read_csv("transformed_diet_df.csv")

    # get rid of whole column that have names food_id_* columns from food_abundance.columns
    #food_abundance = food_abundance.loc[:, ~food_abundance.columns.str.contains('food_id_')]
    
    # Process food_abundance dataset
    
    # Dictionary to map names to DataFrames
    datasets = {
        'clients': clients,
        'microbes': microbes,
        'metabolites': metabolites,
        'food_abundance': food_abundance
    }
    
    # Ensure valid choices
    if choice1 not in datasets or choice2 not in datasets:
        raise ValueError("Invalid dataset choices. Choose from 'clients', 'microbes', 'metabolites', 'food_abundance'.")
    
    # Merge chosen datasets on 'ID' using an inner merge
    merged_df = pd.merge(datasets[choice1], datasets[choice2], on='ID', how='inner')
    
    return merged_df

# Example usage:
# merged_df = load_and_merge_csvs('clients', 'food_abundance')

