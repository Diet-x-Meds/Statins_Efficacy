# Specification of Components

### Load Metacardis

**What it does**: Loads the already cleaned and MEDI-prepared csv files. These include:
- Clients (cols on: ID, age, sex, BMI, nationality, medication cols (binary))
- Microbes
- Metabolites
- Diet transformed

**Inputs** (with type information): User just has to input 2 to 4 strings depending on how many csv they want to merge. The function will tell them their string options.

**Outputs** (with type information): 
- New shape of microbes and food data if chosen after clr transformation. This can come as a shock to some since you’re left with only 30 food ids after the transformation
- There will also be a new variable that is a data frame and the user can save this as a csv or just use it in the next functions as is

**Components used**: 
- Files from github repo in the data folder
- Knowledge about what data they need to merge for the regression

**Primary effect**: Imports csv files of metacardis metadata and MEDI-prepared data 

**Side effects**: Data sets are too large to visualize easily

---

### Choose Covariates

**What it does**: User selects a dependent variable to generate a cluster map to visualize how different covariates affect their biomarker of interest

**Inputs** (with type information): A merged csv from load metacardis, a dependent variable and a list of covariables such as Age, Sex, BMI

**Outputs** (with type information): A cluster map with labels and correlation values

**Components used**: 
- Output from load metacardis and some intuition and knowledge about covariables and gut microbiome research

**Side effects**: Doesn’t tell the whole story, choosing covariable is much more complicated in practice

---

### Regression

**What it does**: Runs a linear regression model with merged data

**Inputs** (with type information): List of dependent variables, list of independent variables, dataframe containing all data, and a formula string

**Outputs** (with type information): Dataframe with significant features, beta coefficients, t-statistics, p-values, and FDR adj. q-values. 

**Components used**: Merged dataset from load_metacardis, statsmodels ols, and statsmodels multipletests

**Main effects**: Runs regression function and creates a new dataframe with test information

**Side effects**: Can increase memory usage and computational overhead if dataset is large

---

### diet_dist

**What it does**: Reshapes the food_abundance dataframe to group together all the foods found for each patient 

**Inputs** (with type information): Food_abundance csv file where each row is a different wiki id food for a patient 

**Outputs** (with type information): Reshaped dataframe in csv format where each patient has one row and multiple columns for the different foods

**Components used**: pandas

**Side effects**: Might increase memory usage if a large dataframe is used, as it reshapes that and saves it as a new dataframe

---

### diet_tables

**What it does**: Creates dataframes of counts and percentages of how often different foods_groups, food_subgroups, and wikipedia_ids are found in the dataset

**Inputs** (with type information): Food_abundance csv file where each row is a different wiki id food for a patient 

**Outputs** (with type information): 3 dataframes for food_groups, food_subgroups, and wikipedia_ids with

**Components used**: pandas, diet_distr

**Side effects**: Can take a lot of time to run as it uses value_counts(), which might take a long time on large datasets. 

---

### diet_charts

**What it does**: Creates pie charts of how often different  foods_groups, food_subgroups, and food wikipedia_ids are found in the dataset

**Inputs** (with type information): Food_abundance csv file where each row is a different wiki id food for a patient 

**Outputs** (with type information): 3 groups of pie charts: one that contains a pie chart of the different food_groups, top 20 food_subgroups, and top 20 wikipedia_ids; one subplot of the counts of food_subgroups in each food_group; and one subplot of the counts of wikipedia_ids in each food_subgroup

**Components used**: pandas, matplotlib, diet_distr, diet_tables

**Side effects**: Can take a lot of time to run as it outputs a lot of charts, especially if it takes in a large dataframe.

---

### metadata_describe()

**What it does**: Outputs tables of statistics about the data (from the metacardis data)

**Inputs** (with type information): Data of interest (pandas dataframe)

**Outputs** (with type information): Pandas dataframe containing concatenated .describe() functions ran on metadata columns of metacardis data. Some columns will include age, sex (% F), BMI, Nationality, health status, and medication use. 

**Components used**: Pandas

**Side effects**: Can increase memory usage and computational overhead if dataset is large

---

### plot_metadata()

**What it does**: Displays some plots of metadata (from the metacardis data)

**Inputs** (with type information): Data of interest (pandas dataframe) 

**Outputs** (with type information): Matplotlib plots (bar chart, histograms and pie charts)

**Components used**: Pandas, Matplotlib, Seaborn

**Side effects**: Can increase memory usage and computational overhead if the dataset is large and outputs many charts. Uses the display.

---

### get_food_info()

**What it does**: Converts food IDs to names and other information

**Inputs** (with type information): Food IDs of interest (integers, strings of form “food_id_[int]”, or 1D lists/arrays with any assortment of the 2 data types)

**Outputs** (with type information): Food information of interest (as a pandas dataframe)

**Components used**: Numpy, Pandas

**Side effects**: Temporarily loads the entire food database into a dataframe, which contains several hundred rows.
