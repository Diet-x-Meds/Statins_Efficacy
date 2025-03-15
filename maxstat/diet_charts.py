def diet_charts(df):
    """
    This function generates pie charts for food group distribution, food subgroup distribution,
    and Wikipedia ID distribution using pre-processed data from diet_tables.
    
    """
    # Get the pre-processed tables from diet_tables
    food_group_counts_df, food_subgroup_counts_df, wikipedia_id_counts_df = diet_tables(df)

    # Define the subgroups and the data frames for plotting
    data_frames = [
        (food_group_counts_df, 'food_group', 'count', 'Food Group Distribution'),
        (food_subgroup_counts_df, 'food_subgroup', 'count', 'Food Subgroup Distribution'),
        (wikipedia_id_counts_df, 'wikipedia_id', 'count', 'Wikipedia ID Distribution')
    ]
    
    # Iterate through each dataframe and plot the pie chart
    for data_df, label_col, count_col, title in data_frames:
        # Create the pie chart without the labels
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(data_df[count_col], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, labels=None)
        
        # Add a legend to the pie chart using the labels from the dataframe
        ax.legend(wedges, data_df[label_col], title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Equal aspect ratio ensures that pie chart is drawn as a circle
        ax.axis('equal')  
        ax.set_title(title)  # Title for each pie chart
        
        # Display the pie chart
        plt.show()

    # For the food subgroups, plot each subgroup and its Wikipedia ID distribution as pie charts
    food_subgroups = food_subgroup_counts_df['food_subgroup'].tolist()

    for food_subgroup in food_subgroups:
        # Filter the original dataframe for rows that match this food subgroup
        food_subgroup_df = df[df.filter(like='food_subgroup').apply(lambda row: row.str.contains(food_subgroup, case=False, na=False)).any(axis=1)]
        
        # Extract all the wikipedia_id columns and stack them to get unique wikipedia_ids
        wikipedia_id_counts = food_subgroup_df.filter(like='wikipedia_id').stack().value_counts()

        # Plot pie chart for each food subgroup's Wikipedia ID distribution
        plt.figure(figsize=(7, 7))
        wikipedia_id_counts.plot.pie(autopct='%1.1f%%', startangle=90, legend=True, labels=wikipedia_id_counts.index)
        plt.title(f"Distribution of Wikipedia IDs in {food_subgroup}")
        plt.ylabel('')
        plt.show()
