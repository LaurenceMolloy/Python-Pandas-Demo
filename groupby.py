from src.GroupBy import *

df = load_example_data()
#example_agg(df)
#example_transform(df)
#example_filter(df)
print(example_regional_sales_category_apply(df))
#example_regional_sales_category_transform(df)

#print("-" * 12, "TOP PRODUCTS IN REGIONS WHERE AVERAGE SALES > 150", "-" * 12)
#print(example_complex_groupby_constraints(df))

#print("-" * 12, "PRODUCT SALES BY REGION", "-" * 12)
#print(example_multiindex_groupby_aggregation(df))