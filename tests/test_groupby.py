import pandas as pd
import numpy as np
import pytest

# import all functions from my module for testing
from src.GroupBy import *   


# Fixture for test data (good practice to avoid repeating data setup)
@pytest.fixture
def sample_sales_data():
    data = {'Region': ['North', 'North', 'East', 'East', 'West', 'West', 'North', 'East', 'West'],
            'Product': ['A', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A'],
            'Month': ['Jan', 'Feb', 'Jan', 'Feb', 'Jan', 'Feb', 'Mar', 'Mar', 'Mar'],
            'Sales': [100, 150, 200, 250, 120, 180, 220, 280, 150]}
    return pd.DataFrame(data)


# PyTest Functionality not yet covered here:
# Fixture Scoping:
# Exception Testing (pytest.raises):
# Conditional Test Skipping (@pytest.mark.skipif):
# Custom Assertion Functions:


# custom markers for selective test execution (runs ONLY with -m fail)
#@pytest.mark.skipif(lambda item: not hasattr(item, "fail"), reason="Test only runs with -m fail")
@pytest.mark.fail
def test_fail():
    assert False


# custom marker for selective skipping of tests
@pytest.mark.skip
def test_skip():
    assert False


# using request fixture to access test context
# (don't foregt -s flag on pytest for preventing print capture)
def test_multiindex_groupby_aggregation(sample_sales_data, request):
    print("\n")
    print(f"Running test: {request.node.name}")
    print(f"Markers: {[mark.name for mark in request.node.own_markers]}")
    df = sample_sales_data.copy()
    result_df = example_multiindex_groupby_aggregation(df)

    # Get the 'Sales' values for 'East' region and 'Product' 'A'

    # ...where Region & Product are index levels
    assert result_df.loc[('East', 'A'), 'Sales'] == 480 

    # ...if we reset the index back to a set of columns
    result_df = result_df.reset_index()
    sales = result_df.loc[(result_df['Region'] == 'East') & (result_df['Product'] == 'A'), 'Sales']
    # using '.values'
    assert len(sales.values) == 1  # there is only record matching the filter
    assert sales.values[0] == 480  # the sales value of that record
    # using '.item()' 
    assert sales.item() == 480     # we can do use this if we are sure there is only one record


def test_regional_sales_category_apply(sample_sales_data):
    df = sample_sales_data.copy()
    result_df = example_regional_sales_category_apply(df)
    
    result_df = result_df.reset_index()

    # Test Regional Sales Category for 'East' region records
    sales = result_df.loc[(result_df['Region'] == 'East'), 'Regional_Sales_Category'] 
    assert len(sales.values) == 3 # there are 3 East Region records
    # All East Region records must show its Region's Sales Category (which is High)
    assert list(sales.values) == ['High Sales']*len(sales.values) 
    
    # Test Regional Sales Category for 'North' region records
    sales = result_df.loc[(result_df['Region'] == 'North'), 'Regional_Sales_Category'] 
    assert len(sales.values) == 3 # there are 3 North Region records
    # All North Region records must show its Region's Sales Category (which is Medium)
    assert list(sales.values) == ['Medium Sales']*len(sales.values)


# parameterize the above regional sales category test
# this tests for all correct answers for all three regions without repeating code
@pytest.mark.parametrize("region, category", [
    ("East", "High Sales"),
    ("North", "Medium Sales"),
    ("West", "Low Sales")
])
def test_regional_sales_category_apply_parameterized(sample_sales_data, region, category):
    df = sample_sales_data.copy()
    result_df = example_regional_sales_category_apply(df)
    
    result_df = result_df.reset_index()

    # Test Regional Sales Category for <region> records
    sales = result_df.loc[(result_df['Region'] == region), 'Regional_Sales_Category'] 
    assert len(sales.values) == 3 # there are 3 East Region records
    # All East Region records must show its Region's Sales Category (which is <category>)
    assert list(sales.values) == [category]*len(sales.values)


# NB: pytest-mock also exists - it provides more control over the mock object's behavior 
# but monkeypatch is simpler if you just want to replace a function or a value
# (monkeypatch auto-reverts the object after the test function completes)
def test_regional_sales_category_apply_monkeypatch(sample_sales_data, monkeypatch):

    def mock_sales_category(group):
        # Always return "Monkeypatched" regardless of sales
        return pd.Series(["Monkeypatched"] * len(group), index=group.index)

    # Monkeypatch the original function with the mock
    monkeypatch.setattr("src.GroupBy.sales_category", mock_sales_category)

    df = sample_sales_data.copy()
    result_df = example_regional_sales_category_apply(df)
    result_df = result_df.reset_index()

    # Test Regional Sales Category for 'East' region records
    sales = result_df.loc[(result_df['Region'] == 'East'), 'Regional_Sales_Category'] 
    assert len(sales.values) == 3 # there are 3 East Region records
    # All East Region records must show its Region's *monkeypatched* Sales Category
    assert list(sales.values) == ['Monkeypatched']*len(sales.values)  

    # Restore the original function (NB: this is optional, pytest handles this automatically)
    monkeypatch.undo()

    # re-run the analysis WITH MONKEYPATCHING NOW REVERTED
    result_df = example_regional_sales_category_apply(df)
    result_df = result_df.reset_index()

    # Show that Regional Sales Category for 'East' region records is back to normal
    sales = result_df.loc[(result_df['Region'] == 'East'), 'Regional_Sales_Category'] 
    assert len(sales.values) == 3 # there are 3 East Region records
    # All East Region records must show its Region's Sales Category (which is High)
    assert list(sales.values) == ['High Sales']*len(sales.values)  
