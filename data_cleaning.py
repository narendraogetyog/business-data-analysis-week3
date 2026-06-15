"""
data_cleaning.py
Week 3 - Business Data Analysis | Hashclick Solutions LLC
Author: Narendra Ogety
Task: Data Cleaning and Preprocessing
"""

import pandas as pd
import numpy as np
import os

# ============================================================
# STEP 1: Generate Synthetic Sales Dataset
# ============================================================

np.random.seed(42)
n = 500

regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Operations', 'Marketing']
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones'],
    'Clothing': ['Shirt', 'Pants', 'Jacket', 'Shoes'],
    'Operations': ['Printer', 'Scanner', 'Office Chair', 'Desk'],
    'Marketing': ['Banner', 'Brochure', 'Ad Campaign', 'Signage']
}
customer_segments = ['Retail', 'Wholesale', 'Online', 'Corporate']

dates = pd.date_range(start='2024-01-01', end='2024-12-31', periods=n)
category_list = np.random.choice(categories, n)
product_list = [np.random.choice(products[c]) for c in category_list]
units_sold = np.random.randint(1, 100, n)
unit_price = np.round(np.random.uniform(10, 500, n), 2)
revenue = np.round(units_sold * unit_price, 2)
marketing_spend = np.round(revenue * np.random.uniform(0.05, 0.20, n), 2)
return_rate = np.round(np.random.uniform(0.01, 0.10, n), 4)

# Introduce nulls and dirty data for cleaning exercise
null_idx = np.random.choice(n, 30, replace=False)
revenue_arr = revenue.astype(object)
revenue_arr[null_idx[:10]] = np.nan

units_arr = units_sold.astype(object)
units_arr[null_idx[10:20]] = np.nan

price_arr = unit_price.astype(object)
price_arr[null_idx[20:]] = np.nan

df_raw = pd.DataFrame({
    'OrderID': ['ORD' + str(i).zfill(4) for i in range(1, n+1)],
    'Date': dates,
    'Region': np.random.choice(regions, n),
    'Category': category_list,
    'Product': product_list,
    'UnitsSold': units_arr,
    'UnitPrice': price_arr,
    'Revenue': revenue_arr,
    'CustomerSegment': np.random.choice(customer_segments, n),
    'MarketingSpend': marketing_spend,
    'ReturnRate': return_rate
})

# Add duplicate rows
duplicates = df_raw.sample(5, random_state=1)
df_raw = pd.concat([df_raw, duplicates], ignore_index=True)

print("=" * 60)
print("RAW DATASET SUMMARY")
print("=" * 60)
print(f"Shape: {df_raw.shape}")
print(f"\nMissing Values:\n{df_raw.isnull().sum()}")
print(f"\nDuplicate Rows: {df_raw.duplicated().sum()}")
print(f"\nData Types:\n{df_raw.dtypes}")

# ============================================================
# STEP 2: Data Cleaning
# ============================================================

df = df_raw.copy()

# 2.1 Remove duplicates
df.drop_duplicates(inplace=True)
print(f"\nAfter removing duplicates: {df.shape}")

# 2.2 Handle missing values
# UnitsSold: fill with median
df['UnitsSold'] = pd.to_numeric(df['UnitsSold'], errors='coerce')
df['UnitsSold'].fillna(df['UnitsSold'].median(), inplace=True)
df['UnitsSold'] = df['UnitsSold'].astype(int)

# UnitPrice: fill with mean per Category
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
df['UnitPrice'] = df.groupby('Category')['UnitPrice'].transform(
    lambda x: x.fillna(x.mean())
)
df['UnitPrice'] = df['UnitPrice'].round(2)

# Revenue: recalculate where missing
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
missing_rev = df['Revenue'].isnull()
df.loc[missing_rev, 'Revenue'] = (
    df.loc[missing_rev, 'UnitsSold'] * df.loc[missing_rev, 'UnitPrice']
).round(2)

# 2.3 Type conversions
df['Date'] = pd.to_datetime(df['Date'])
df['MarketingSpend'] = pd.to_numeric(df['MarketingSpend'], errors='coerce').fillna(0)
df['ReturnRate'] = pd.to_numeric(df['ReturnRate'], errors='coerce').fillna(0)

# 2.4 Add derived columns
df['Month'] = df['Date'].dt.month
df['MonthName'] = df['Date'].dt.strftime('%b')
df['Quarter'] = df['Date'].dt.quarter
df['Profit'] = (df['Revenue'] - df['MarketingSpend']).round(2)
df['ReturnAmount'] = (df['Revenue'] * df['ReturnRate']).round(2)

# 2.5 Remove negative values
df = df[df['Revenue'] > 0]
df = df[df['UnitsSold'] > 0]

# ============================================================
# STEP 3: Save Clean Dataset
# ============================================================

os.makedirs('data', exist_ok=True)
df.to_csv('data/sales_data.csv', index=False)

print("\n" + "=" * 60)
print("CLEAN DATASET SUMMARY")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nSample Records:")
print(df.head())
print(f"\nDescriptive Statistics:")
print(df[['UnitsSold', 'UnitPrice', 'Revenue', 'MarketingSpend', 'Profit']].describe().round(2))

print("\nClean dataset saved to: data/sales_data.csv")
print("Data cleaning completed successfully!")
