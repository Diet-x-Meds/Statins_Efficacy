def plot_metadata(df):
    '''This function plots graphs describing the metadata (in our case, Metacardis)'''

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.ticker as mticker  

    # come back and divide up things between here and metadata_describe
    # Store original column names for reference
    original_columns = df.columns.copy()
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    # drugs_of_interest = [s.lower() for s in drugs_of_interest]
    # drugs_of_interest = [s.replace(" ", "_") for s in drugs_of_interest]
    
    # Remove client ID column if present
    df = df.loc[:, df.nunique() > 1]
    
    # Separate categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    # Identify binary medication columns (0/1 values)
    medication_cols = [col for col in df.select_dtypes(include=['number']).columns if df[col].nunique() == 2]
    numerical_cols = [col for col in df.select_dtypes(include=['number']).columns if col not in medication_cols]
    
    # Mapping standardized names back to original names for labeling purposes
    col_name_map = dict(zip(df.columns, original_columns.str.replace("_"," ")))

    # Bar chart for medication usage
    medication_usage = df[medication_cols].mean() * 100
    plt.figure(figsize=(12,6))
    colors = ['steelblue' for col in medication_usage.index]
    medication_usage.sort_values().plot(kind='barh', color=colors, edgecolor='black', alpha=0.8)
    plt.xlabel('Percentage of Patients Taking Medication', fontsize=12)
    plt.title('Medication Usage Among Patients', fontsize=14)
    plt.xticks(rotation=0)
    plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter())
    plt.yticks(ticks=range(len(medication_usage)), labels=[col_name_map.get(col, col) for col in medication_usage.index])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

    # histograms
    for col in numerical_cols:
        if col != 'id':
            plt.figure(figsize=(6,4))
            sns.histplot(df[col].dropna(), kde=True, bins=30, color="royalblue", alpha=0.7)
            plt.title(f'Distribution of {col_name_map.get(col, col)}', fontsize=14)
            plt.xlabel(col_name_map.get(col, col))
            plt.ylabel('Frequency')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
    # pie charts 
    for col in categorical_cols:
        if col != 'id':
            plt.figure(figsize=(6,4))
            df[col].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3', wedgeprops={'edgecolor': 'black'}) # cmap='Set3')
            plt.title(f'Distribution of {col_name_map.get(col, col)}', fontsize=14)
            plt.ylabel('')
            plt.show()
            
    