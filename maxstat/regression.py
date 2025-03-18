import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
import pandas as pd
import numpy as np
import os

def linear_regression_results(dependent_features, independent_features,
                              formula_string, df):
    """
    Get a single association (x --> y) for a specific combination of features. 
    --------
    Input: (1) list of dependent features, (2) list of independent
    features, (3) `str` specifying the linear regression formula 
    to use, (4) df of data to use for fitting the model. 
    --------
    Output: df containing summary statistics for our association.
    The df will specify formula, dependent, and independent features
    used. P-values FDR-corrected using Benjamini Hochberg.
    """
    all_results = [] # Initialize an empty list to store the results

    # Unittesting led us to create a check for categorical variables
    # This MUST be done before the regression in run using statsmodels
    # Independent features should not be categorical
    for feature in independent_features:
        if df[feature].dtype == 'object' or isinstance(df[feature].dtype, pd.CategoricalDtype):
            raise ValueError(f"Categorical variable '{feature}' cannot be an independent variable.")
    
    # Iterate through all combinations of dependent and independent features
    for dependent_feature in dependent_features:
        for independent_feature in independent_features:
            # Define the formula using the provided dependent and independent variables
            formula = formula_string.format(dependent_feature = dependent_feature,
                                            independent_feature = independent_feature)
            fitted = ols(formula, data=df).fit()
            # Create a Series with the results
            result_series = pd.Series({
                "dependent_feature": dependent_feature,
                "independent_feature": independent_feature,
                "beta": fitted.params,
                "t_statistic": fitted.tvalues[independent_feature],
                "p": fitted.pvalues[independent_feature],
                "n": fitted.nobs,
                "formula": formula
                })
            all_results.append(result_series)

    # Turn the all_results list into a pandas df
    tests = pd.DataFrame(all_results)
    # Perform multiple testing correction
    tests["q"] = multipletests(tests["p"], method="fdr_bh")[1]
    return tests
