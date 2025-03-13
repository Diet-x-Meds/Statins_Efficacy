import numpy as np
import pandas as pd
import re

def get_food_info(food_ids=[]):
    """
    This function outputs the name, species, and food group associated with each provided food ID as a dataframe.

    Args:
        food_ids (int/np.integer | str of form "food_id_[int]" | list/array of any mix of ints/np.integers or strs of form "food_id_[int]" | ): A food ID or list of food IDs to retrieve information for. If empty, all valid food IDs will be returned in the output dataframe.

    Returns:
        pd.DataFrame: Dataframe with food information.

    Raises:
        TypeError: Triggered by any input that is not an integer or 1D list/array of integers/strs of form "food_id_[int]"
        ValueError: Triggered by any string inputs not of the form "food_id_[int]" or 1D lists containing invalid strings
        KeyError: Triggered by invalid food IDs
    """
    
    # Check that the provided input is either an integer or a 1D list of integers
    sanitized_food_ids = None
    if isinstance(food_ids, (int, np.integer)):
        sanitized_food_ids = [food_ids]
    elif isinstance(food_ids, str):
        # Check for "food_id_[int]" form and extract the integer if it matches, else throw a ValueError
        if re.match(r"food_id_[0-9]+$", food_ids):
            sanitized_food_ids = [int(food_ids.split('_')[2])]
        else:
            raise ValueError(f'Single inputs must be an integer or string of form "food_id_[int]", but the string you provided: {food_ids} is not of the correct form.')
    elif isinstance(food_ids, (list, np.ndarray)):
        for food_id in food_ids:
            if isinstance(food_id, (int, np.integer)):
                pass
            elif isinstance(food_id, str):
                if re.match(r"food_id_[0-9]+$", food_id):
                    food_id = int(food_id.split('_')[2])
                else:
                    raise ValueError(f'List/array inputs must be 1D with any mix of integers or strings of form "food_id_[int]", but at least one element of the provided list/array: "{food_id}" is a string that does not fit those requirements.')
            else:
                raise TypeError(f'List/array inputs must be 1D with any mix of integers or strings of form "food_id_[int]", but at least one element of the provided list/array is of type {type(food_id)}')
            
            # If no errors are raised, add it to the list of sanitized IDs
            if sanitized_food_ids is None:
                sanitized_food_ids = [food_id]
            else:
                sanitized_food_ids.append(food_id)
        
        # If the list is empty, still pass it through
        if sanitized_food_ids is None:
            sanitized_food_ids = []

    # If the input is not of the right type, throw a TypeError
    if sanitized_food_ids is None:
        raise TypeError(f'Input must be an integer or 1D list/array of integers, but {type(food_ids)} was detected.')
        
    # Read in the CSV with annotated food ID, name, and species data
    df = pd.read_csv('data/annotated_food_matches.csv', index_col=False)
    # Renumber the index to match the food_ids so that rows can be indexed by food_id through loc
    df.index = df['food_id'].values

    # Return the dataframe without filtering if no specific food IDs are specified
    if len(sanitized_food_ids) == 0:
        # Renumber the indices of the df
        df.index = pd.RangeIndex(1, len(df.index) + 1, 1)
        return df

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

    # Filter for the specified food_ids, then sort in ascending order of food ID
    df_filtered = df.loc[list(sanitized_food_id_set), :]
    df_filtered.sort_values(by=['food_id'], inplace=True)
    # Renumber the indices of the filtered df
    df_filtered.index = pd.RangeIndex(1, len(df_filtered.index) + 1, 1)
    
    return df_filtered