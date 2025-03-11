import numpy as np
import pandas as pd

def get_food_info(food_ids):
    """
    This function outputs the name, species, and food group associated with each provided food ID as a dataframe.

    Args:
        food_ids (required, int/np.integer | list/array of ints/np.integers): A food ID or list of food IDs to retrieve information for.

    Returns:
        pd.DataFrame: Dataframe with food information.

    Raises:
        TypeError: Triggered by any input that is not an integer or 1D list/array of integers
        KeyError: Triggered by invalid food IDs
    """
    
    # Check that the provided input is either an integer or a 1D list of integers
    sanitized_food_ids = None
    if isinstance(food_ids, (int, np.integer)):
        sanitized_food_ids = [food_ids]
    elif isinstance(food_ids, (list, np.ndarray)):
        if all(isinstance(x, (int, np.integer)) for x in food_ids):
            sanitized_food_ids = food_ids
        else:
            raise TypeError(f'Input must be an integer or 1D list/array of integers, but at least one element of the provided list is not an integer.')
    # If the input is not of the right type, throw a TypeError
    if sanitized_food_ids is None:
        raise TypeError(f'Input must be an integer or 1D list/array of integers, but {type(food_ids)} was detected.')
        
    # Read in the CSV with annotated food ID, name, and species data
    df = pd.read_csv('data/annotated_food_matches.csv', index_col=False)
    # Renumber the index to match the food_ids so that rows can be indexed by food_id through loc
    df.index = df['food_id'].values

    # Check that the specified food IDs actually exist, and store the ones that don't
    sanitized_food_id_set = set(sanitized_food_ids)
    invalid_food_ids = sanitized_food_id_set.difference(df.index)
    # Raise a ValueError if any invalid IDs are detected
    if invalid_food_ids:
        invalid_food_ids = list(map(str, invalid_food_ids))
        if len(invalid_food_ids) == 1:
            raise KeyError(f'{invalid_food_ids[0]} is not a valid food ID')
        elif len(invalid_food_ids) >= 2:
            raise KeyError(f'{", ".join(invalid_food_ids[:-1])} and {invalid_food_ids[-1]} are not valid food IDs')

    # Filter for the specified food_ids
    df_filtered = df.loc[list(sanitized_food_id_set), :]
    # Renumber the indices of the filtered df
    df_filtered.index = pd.RangeIndex(1, len(df_filtered.index) + 1, 1)
    
    return df_filtered