# maxstat
`maxstat` is a Python package that aims to streamline the analysis of large, patient-derived datasets involving drug usage, and/or diet. It allows users to easily identify biomarkers, foods, and drugs that are linked to a variable of interest, such as statin usage. Support for microbiome-based analyses will be added at a later date.
* Users that don't have their own datasets can use the processed [METACARDIS drug dataset](https://www.nature.com/articles/s41586-021-04177-9) that ships with `maxstat`, which contains data from hundreds of European patients. Users can also access a METACARDIS-derived diet dataset that was generated using [MEDI](https://www.nature.com/articles/s42255-025-01220-1), a pipeline that extracts diet and nutrient information from human stool genomic data. 
* Users with their own datasets can use the same pipelines to process their data, provided that they are formatted similarly to METACARDIS. Support for other formats will be expanded at a later time.

Authors:
Mia Giallorenzi, Melissa Hopkins, Avery Yang, Crystal Perez, Anika O'Brian

## Usage

The `maxstat` package contains several modules, each of which contains a function of a related name. **In future versions, these modules will be merged into a single module**.

### Data visualization modules
`metadata_describe.metadata_describe`: This function is intended to be used with the METACARDIS medication dataset. It takes in a dataframe and outputs a dataframe containing descriptive statistics for numerical, categorical, and binary medication columns. The output DataFrame has statistics as rows and original column names as `columns.Medication`<br>
> Parameters<br> - `df`: `pd.DataFrame` of the medication dataset.

> Returns<br> - `pd.DataFrame` with medication dataset statistics

`plot_metadata.plot_metadata`: This function is intended to be used with the METACARDIS medication dataset. It takes in a dataframe and outputs plots graphs of various descriptive statistics for the dataframe, such as medication distribution and usage.
> Parameters<br> - `df`: `pd.DataFrame` of the medication dataset.

> Returns<br> - Nothing

`diet_distr.diet_distr`: This function is intended to be used with the METACARDIS-derived diet dataset. It takes in a dataframe, reformats it to make it easier to work with, and outputs the reformatted dataframe.
> Parameters<br> - `df`: `pd.DataFrame` of the diet dataset.

> Returns<br> - `pd.DataFrame` of reshaped diet data

`diet_tables.diet_tables`: This function is intended to be used with the `diet_distr`-reformatted version of the METACARDIS-derived diet dataset. It takes a reshaped dataframe and outputs 3 dataframes about the foods in the dataset in the following order: counts by food group, counts by food subgroup, and counts by Wikipedia ID.
> Parameters<br> - `df`: `pd.DataFrame` of the reshaped diet data.

> Returns<br> - 3x `pd.DataFrame` including food group, subgroup, and Wikipedia ID counts in reshaped diet data

`diet_charts.diet_charts`: This function is intended to be used with the `diet_tables`-processed version of the METACARDIS-derived diet dataset. It generates pie charts for food group distribution, food subgroup distribution, and Wikipedia ID distribution depending on which pre-processed dataframe from `diet_tables` is provided.
> Parameters<br> - `df`: `pd.DataFrame` of the reshaped and analyzed diet data.

> Returns<br> - Nothing

### Data processing modules
`load_metacardis.load_and_merge_csvs`: This function is intended to be used with processed METACARDIS datasets. It merges selected datasets (at least 2, up to 4) based on the patient 'ID' column using an inner merge, applies a CLR transformation to microbes and food_abundance datasets, and filters features that are non-zero in at least 90% of the microbes and 95% foods.
> Parameters<br> - `*choices`: 2-4x `str`. Allowed values are `clients`, `microbes`, `metabolites`, and `food_abundance`.

> Returns<br> - `pd.DataFrame` of merged METACARDIS datasets

`choose_covars.plot_impact_covariate_clustermap`: This function is intended to be used with merged METACARDIS datasets. It creates a clustermap based on how covariates impact a specified dependent variable by using Spearman correlation for numeric variables and eta-squared for categorical variables.
> Parameters<br> - `df`: `pd.DataFrame` containing covariates and the dependent variable.<br> - `dependent_var`: `str` specifying the dependent variable, eg. 'hba1c'<br> - `covariates`: 1D `list` of `str`, where each `str` is a covariate to analyze

> Returns<br> - `mpl.figure` with an `sns.clustermap` of correlation between the specified dependent variable and covariates

`regression.linear_regression_results`: This function is intended to be used with merged METACARDIS datasets. It takes in dependent and independent features of interest, a regression formula, and data in the form of a dataframe, computes the specified regression, and outputs a dataframe containing summary statistics for the desired associations. P-values are FDR-corrected using Benjamini Hochberg.
> Parameters<br> - `dependent_features`: 1D `list` of `str`, where each `str` is the name of a dependent feature to analyze<br> - `independent_features`: 1D `list` of `str`, where each `str` is the name of an independent feature to analyze<br> `formula_string`: `str` specifying the linear regression formula in a `statsmodels.regression.linear_model.ols`-compatible form<br> - `df`: `pd.DataFrame` containing data to use for fitting the model. Must contain all specified dependent and independent variables as columns.

`get_food_info.get_food_info`: This function takes a food ID or list of food IDs and generates a 1-indexed dataframe with food IDs and information about the food, including its name, genus, species, food group, and food subgroup. A blank input outputs all valid foods.
> Parameters<br> - `food_ids`: `int`, `str` of form `food_id_[int]`, or 1D `list` or `np.ndarray` containing only the former two data types 

> Returns<br>- `pd.DataFrame`