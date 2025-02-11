import pandas as pd
import numpy as np


# example data - hard-coded
def load_example_data(file = None):
    if file:
        try:
            df = pd.read_csv(file)  
            print("HELLO")
            return df
        except Exception as e:
            raise Exception(e)
    else:
        data = {'Region': ['North', 'North', 'East', 'East', 'West', 'West', 'North', 'East', 'West'],
                'Product': ['A', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A'],
                'Month': ['Jan', 'Feb', 'Jan', 'Feb', 'Jan', 'Feb', 'Mar', 'Mar', 'Mar'],
                'Sales': [100, 150, 200, 250, 120, 180, 220, 280, 150]}
        df = pd.DataFrame(data)
    return df


# Aggregations with multiple aggregation functions
# Showing count, sum, mean & max for each product in each region
# 1. group by Region and Product
# 2. apply multiple aggregation functions (sum, mean, max) to the Sales column
def example_agg(df):
    #print('-'*12, "Aggregations by Region and Product", '-'*12)
    result = df.groupby(['Region', 'Product']).agg({'Sales': ['count', 'sum', 'mean', 'max']})
    print(result)


# Transformation - Feature Engineering
# Calculating percentage of total sales within each region (uses transform() and lambda())
# 1. group by region
# 2. apply a transform to each group (returns series of same length as dataframe)
def example_transform(df):
    #print('-'*12, "Percentage of Total Regional Sales", '-'*12)
    # add the "percentage of total sales within the region" metric
    # apply round(n,2) for 2DP formatting
    df['Sales_Pct_Region'] = df.groupby('Region')['Sales'].transform(lambda x: round(x / x.sum() * 100, 2))
    print(df.sort_values(by=['Region','Product','Month']).set_index('Region'))


# Filtering Data
def example_filter(df):
    #print('-'*12, "Sales Within High Sales Regions", '-'*12)
    filtered_df = df.groupby('Region').filter(lambda x: x['Sales'].mean() > 200)
    print(filtered_df.sort_values(by=['Region','Product','Month']).set_index('Region'))


def sales_category(group):
    mean_sales = group['Sales'].mean()
    categories = []  # Create an empty list to store categories for each row
    for _ in range(len(group)):  # Iterate through the rows of the group
        if mean_sales > 200:
            categories.append('High Sales')
        elif mean_sales > 150:
            categories.append('Medium Sales')
        else:
            categories.append('Low Sales')
    return pd.Series(categories, index=group.index)  # Return Series with correct length


# apply() VERSION:
def example_regional_sales_category_apply(df):
    #print('-'*12, "Regional Sales Category - APPLY()", '-'*12)
    # First we need to re-order the dataframe NOT IN-SITU (required to apply reset_index)
    df = df.sort_values(by=['Region'], inplace=False).reset_index()
    # NB: agg() and/or transform() are usually preferred over apply() because they are more efficient
    df['Regional_Sales_Category'] = df.groupby('Region').apply(sales_category).reset_index(name='Category')['Category']
    return(df.sort_values(by=['Region','Product','Month']).set_index('Region'))
#    print(df.sort_values(by=['Region','Product','Month']).set_index('Region'))


# transform() VERSION - works without the re-ordering
def example_regional_sales_category_transform(df):
    #print('-'*12, "Regional Sales Category - TRANSFORM()", '-'*12)
    df['Regional_Sales_Category'] = df.groupby('Region')['Sales'].transform(lambda x: sales_category(df.loc[x.index]))
    print(df.sort_values(by=['Region','Product','Month']).set_index('Region'))


def example_complex_groupby_constraints(df: pd.DataFrame) -> pd.DataFrame:
    """Demonstrates complex constraints with concatenated groupby operations.

    Q. What are the top selling products in regions with average sales over 150?
    
    Args:
        df: A Pandas DataFrame 

    Returns:
        A Pandas DataFrame containing the top-selling product in each qualifying region.
        The index of the returned DataFrame will be the 'Region'.

    Raises:
        TypeError: If the input `df` is not a Pandas DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input 'df' must be a Pandas DataFrame.")

    return (                                        # QUERY EXPLANATION:
        df.groupby('Region')                        # Group by Region
        .filter(lambda x: x['Sales'].mean() > 150)  # Filter for high average Sales Regions
        .groupby(['Region', 'Product'])['Sales']    # Group by Region and Product
        .sum()                                      # Sum the Product Sales in each Region
        .reset_index()                              # Flatten back to a tabular format
        .sort_values(['Region', 'Sales'], 
                     ascending=[True, False])       # Sort by Region (alphabetic) and then Sales (most to least)
        .groupby('Region')                          # Group By Region again
        .first()                                    # Select the first (top selling) Product within each Region
    )



def example_multiindex_groupby_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Demonstration of how to perform aggregations on hierarchical data structures

    Q. What are the product sales numbers in each region?

    Args:
        data: A dictionary representing the data for the DataFrame.

    Returns:
        A Pandas DataFrame resulting from the groupby and aggregation.
        The index will be the levels that were grouped by.

    Raises:
        TypeError: If the input `df` is not a DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input 'df' must be a Pandas DataFrame.")
                                                                # QUERY EXPLANATION:
    df.set_index(["Region", "Product", "Month"], inplace=True)  # Set a multi-index (Region, Product & Month)
    levels_to_group_by = df.index.names.difference(["Month"])   # Construct a list of all index levels EXCEPT Month
    return (
        df.groupby(level=levels_to_group_by)                    # Group by all levels in the list (i.e. Region & Product)
        .sum()                                                  # Calculate sales totals for each Product & Region
    )

