import pandas as pd
import matplotlib.pyplot as plt
from maxstat.diet_tables import diet_tables

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
    
    for data_df, label_col, count_col, title in data_frames:
        # Select top 20 categories
        top_20_df = data_df.nlargest(20, count_col)  # Get top 20 based on the 'count' column

        # Create the pie chart without the labels
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(top_20_df[count_col], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, labels=None)
        
        # Add a legend to the pie chart using the labels from the dataframe
        ax.legend(wedges, top_20_df[label_col], title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Equal aspect ratio ensures that pie chart is drawn as a circle
        ax.axis('equal')  
        ax.set_title(f"Top 20 - {title}")  # Title for each pie chart
        
        plt.tight_layout()  # Adjust layout for better spacing
        plt.show()
        
        
    # For the food subgroups, plot each subgroup and its Wikipedia ID distribution as pie charts in subplots
    food_subgroups = food_subgroup_counts_df['food_subgroup'].tolist()

    # Determine the number of subplots (adjust the number of rows and columns as needed)
    num_subgroups = len(food_subgroups)
    rows = (num_subgroups // 3) + (num_subgroups % 3 > 0)  # Adjust the number of rows dynamically
    cols = 3  # Set the number of columns in the grid of subplots

    # Create subplots (rows x cols grid)
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()  # Flatten axes array to make indexing easier
    
    # Plot each food subgroup's Wikipedia ID distribution
    for i, food_subgroup in enumerate(food_subgroups):
        # Filter the original dataframe for rows that match this food subgroup
        food_subgroup_df = df[df.filter(like='food_subgroup').apply(lambda row: row.str.contains(food_subgroup, case=False, na=False)).any(axis=1)]
        
        # Extract all the wikipedia_id columns and stack them to get unique wikipedia_ids
        wikipedia_id_counts = food_subgroup_df.filter(like='wikipedia_id').stack().value_counts()

        # Calculate the percentages for each Wikipedia ID count
        total_count = wikipedia_id_counts.sum()
        wikipedia_id_percentages = (wikipedia_id_counts / total_count) * 100
        
        # Create legend labels including the percentage values
        legend_labels = [f"{idx} ({percent:.1f}%)" for idx, percent in zip(wikipedia_id_counts.index, wikipedia_id_percentages)]
        
        # Plot pie chart for the current food subgroup's Wikipedia ID distribution
        wedges, texts = axes[i].pie(wikipedia_id_counts, startangle=90, colors=plt.cm.Paired.colors, labels=None)
        
        # Add a legend to the pie chart with percentages in the labels
        axes[i].legend(wedges, legend_labels, title="Wikipedia IDs", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Title for each subplot
        axes[i].set_title(f"Distribution of Wikipedia IDs in {food_subgroup}")
        axes[i].axis('equal')  # Equal aspect ratio ensures pie chart is a circle

    # Hide any empty subplots (if num_subgroups < rows * cols)
    for j in range(num_subgroups, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()

    ### New section: Plot distribution of subgroups within each food group as pie charts in subplots ###

    # Plot food group distribution and its subgroups in subplots
    food_groups = food_group_counts_df['food_group'].tolist()

    # Determine the number of subplots (adjust the number of rows and columns as needed)
    num_food_groups = len(food_groups)
    rows = (num_food_groups // 3) + (num_food_groups % 3 > 0)  # Adjust the number of rows dynamically
    cols = 3  # Set the number of columns in the grid of subplots

    # Create subplots (rows x cols grid)
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()  # Flatten axes array to make indexing easier

    # Plot each food group's subgroups distribution
    for i, food_group in enumerate(food_groups):
        # Filter the original dataframe for rows that match this food group
        food_group_df = df[df['food_group'] == food_group]
        
        # Get the distribution of subgroups within this food group
        food_group_subgroup_counts = food_group_df['food_subgroup'].value_counts()

        # Calculate the percentages for each subgroup count
        total_count = food_group_subgroup_counts.sum()
        food_group_subgroup_percentages = (food_group_subgroup_counts / total_count) * 100
        
        # Create legend labels including the percentage values
        legend_labels = [f"{subgroup} ({percent:.1f}%)" for subgroup, percent in zip(food_group_subgroup_counts.index, food_group_subgroup_percentages)]
        
        # Plot pie chart for the current food group's subgroups distribution
        wedges, texts = axes[i].pie(food_group_subgroup_counts, startangle=90, colors=plt.cm.Paired.colors, labels=None)
        
        # Add a legend to the pie chart with percentages in the labels
        axes[i].legend(wedges, legend_labels, title="Subgroups", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Title for each subplot
        axes[i].set_title(f"Distribution of Subgroups in {food_group}")
        axes[i].axis('equal')  # Equal aspect ratio ensures pie chart is a circle

    # Hide any empty subplots (if num_food_groups < rows * cols)
    for j in range(num_food_groups, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()
