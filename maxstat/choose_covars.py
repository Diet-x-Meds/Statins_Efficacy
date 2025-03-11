import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, f_oneway

def plot_covariate_impact_clustermap(df, dependent_var, covariates):
    """
    Create a clustermap based on how covariates impact the dependent variable.
    Uses Spearman correlation for numeric variables and eta-squared for categorical variables.

    Args:
        df (pd.DataFrame): DataFrame containing covariates and the dependent variable.
        dependent_var (str): The dependent variable (e.g., 'hba1c').
        covariates (list): List of covariates to analyze.

    Returns:
        fig: A Seaborn clustermap figure.
    """

    # Extract actual column names (remove "C()" notation if present)
    cleaned_covariates = [c[2:-1] if c.startswith("C(") and c.endswith(")") else c for c in covariates]

    # Initialize a dictionary to store effect sizes
    effect_sizes = {}

    # Compute effect sizes
    for cov in cleaned_covariates:
        if cov in df.columns:
            if df[cov].dtype == 'object' or df[cov].dtype.name == 'category':
                # Compute eta-squared for categorical variables (ANOVA)
                categories = df[cov].dropna().unique()
                groups = [df[df[cov] == cat][dependent_var].dropna() for cat in categories]
                if len(groups) > 1:
                    f_stat, _ = f_oneway(*groups)
                    eta_squared = f_stat / (f_stat + len(df) - 1)  # Effect size
                    effect_sizes[cov] = eta_squared
                else:
                    effect_sizes[cov] = 0  # No effect if only one category
            else:
                # Compute Spearman correlation for numerical variables
                corr, _ = spearmanr(df[cov], df[dependent_var], nan_policy='omit')
                effect_sizes[cov] = abs(corr)  # Use absolute correlation for similarity

    # Convert effect sizes to a DataFrame
    effect_df = pd.DataFrame.from_dict(effect_sizes, orient='index', columns=['Effect Size'])

    # Compute a similarity matrix (1 - absolute difference in effect sizes)
    similarity_matrix = 1 - np.abs(effect_df.values - effect_df.values.T)
    similarity_df = pd.DataFrame(similarity_matrix, index=effect_df.index, columns=effect_df.index)

    # Create Clustermap
    fig = sns.clustermap(similarity_df, 
                         cmap='coolwarm',
                         center=0,
                         annot=True,
                         fmt='.2f',
                         linewidths=0.5,
                         xticklabels=True,
                         yticklabels=True)

    plt.title(f"Impact of Covariates on {dependent_var}")
    plt.show()
    return fig

