# Made with help from ChatGPT
def metadata_describe(df):
    '''This function takes in the provided dataframe (in our case, the MEDI-prepared metacardis data) and outputs a dataframe 
       containing descriptive statistics for numerical, categorical, and binary medication columns.
       The output DataFrame has statistics as rows and original column names as columns.'''

    import pandas as pd
    
    # Store original column names for reference
    original_columns = df.columns.copy()
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Remove client ID column if present
    df = df.loc[:, df.nunique() > 1]
    
    # Separate categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    # Identify binary medication columns (0/1 values)
    medication_cols = [col for col in df.select_dtypes(include=['number']).columns if df[col].nunique() == 2]
    numerical_cols = [col for col in df.select_dtypes(include=['number']).columns if col not in medication_cols]

    # Descriptive statistics for numerical columns
    numerical_summary = df[numerical_cols].describe().T

    # Descriptive statistics for categorical columns
    categorical_summary = pd.DataFrame(index=categorical_cols)
    categorical_summary["count"] = df[categorical_cols].count()
    categorical_summary["unique"] = df[categorical_cols].nunique()
    categorical_summary["top"] = df[categorical_cols].mode().iloc[0]  # Most frequent category
    categorical_summary["freq"] = df[categorical_cols].apply(lambda x: x.value_counts().iloc[0] if x.nunique() > 0 else 0)

    # Descriptive statistics for medication columns (binary 0/1)
    medication_summary = pd.DataFrame(index=medication_cols)
    medication_summary["count"] = df[medication_cols].count()
    medication_summary["mean (proportion)"] = df[medication_cols].mean()  # Fraction of patients with 1
    medication_summary["sum (total 1s)"] = df[medication_cols].sum()  # Total number of patients taking medication

    # Combine all summaries
    summary_df = pd.concat([numerical_summary, categorical_summary, medication_summary], axis=0)

    return summary_df.T  # Transpose so statistics become rows and column names become variables
