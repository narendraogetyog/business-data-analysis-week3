"""
eda_analysis.py
Week 3 - Business Data Analysis | Hashclick Solutions LLC
Author: Narendra Ogety
Task: Exploratory Data Analysis (EDA) - Tasks 3 & 4
"""

import pandas as pd
import numpy as np

# ============================================================
# LOAD CLEAN DATASET
# ============================================================

try:
    df = pd.read_csv('data/sales_data.csv', parse_dates=['Date'])
except FileNotFoundError:
    print("Dataset not found. Please run data_cleaning.py first.")
    print("Generating dataset inline...")
    import subprocess
    subprocess.run(['python', 'data_cleaning.py'])
    df = pd.read_csv('data/sales_data.csv', parse_dates=['Date'])

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)
print(f"Dataset Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# ============================================================
# TASK 3: EDA - Basic Statistics
# ============================================================

print("\n" + "-" * 50)
print("1. BASIC STATISTICS")
print("-" * 50)
print(df[['UnitsSold', 'UnitPrice', 'Revenue', 'Profit', 'MarketingSpend']].describe().round(2))

# ============================================================
# REVENUE ANALYSIS
# ============================================================

print("\n" + "-" * 50)
print("2. REVENUE BY REGION")
print("-" * 50)
revenue_by_region = df.groupby('Region')['Revenue'].agg(['sum', 'mean', 'count']).round(2)
revenue_by_region.columns = ['Total Revenue', 'Avg Revenue', 'Order Count']
revenue_by_region['Revenue %'] = (revenue_by_region['Total Revenue'] / revenue_by_region['Total Revenue'].sum() * 100).round(2)
revenue_by_region = revenue_by_region.sort_values('Total Revenue', ascending=False)
print(revenue_by_region)

print("\n" + "-" * 50)
print("3. REVENUE BY CATEGORY")
print("-" * 50)
revenue_by_cat = df.groupby('Category')['Revenue'].agg(['sum', 'mean', 'count']).round(2)
revenue_by_cat.columns = ['Total Revenue', 'Avg Revenue', 'Order Count']
revenue_by_cat['Revenue %'] = (revenue_by_cat['Total Revenue'] / revenue_by_cat['Total Revenue'].sum() * 100).round(2)
revenue_by_cat = revenue_by_cat.sort_values('Total Revenue', ascending=False)
print(revenue_by_cat)

print("\n" + "-" * 50)
print("4. MONTHLY REVENUE TREND")
print("-" * 50)
monthly = df.groupby('Month').agg(
    Total_Revenue=('Revenue', 'sum'),
    Total_Orders=('OrderID', 'count'),
    Avg_Order_Value=('Revenue', 'mean')
).round(2)
monthly.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
print(monthly)

print("\n" + "-" * 50)
print("5. QUARTERLY PERFORMANCE")
print("-" * 50)
quarterly = df.groupby('Quarter').agg(
    Total_Revenue=('Revenue', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Orders=('OrderID', 'count'),
    Marketing_Spend=('MarketingSpend', 'sum')
).round(2)
print(quarterly)

# ============================================================
# TASK 4: TRENDS, PATTERNS AND KEY INSIGHTS
# ============================================================

print("\n" + "=" * 60)
print("KEY INSIGHTS & PATTERNS")
print("=" * 60)

# Insight 1: Top performing region
top_region = revenue_by_region['Total Revenue'].idxmax()
top_region_pct = revenue_by_region.loc[top_region, 'Revenue %']
print(f"\n[INSIGHT 1] Top Region: {top_region} ({top_region_pct}% of total revenue)")

# Insight 2: Best category
top_category = revenue_by_cat['Total Revenue'].idxmax()
top_cat_pct = revenue_by_cat.loc[top_category, 'Revenue %']
print(f"[INSIGHT 2] Best Category: {top_category} ({top_cat_pct}% revenue share)")

# Insight 3: Peak month
peak_month = monthly['Total_Revenue'].idxmax()
peak_rev = monthly.loc[peak_month, 'Total_Revenue']
print(f"[INSIGHT 3] Peak Month: {peak_month} (Revenue: ${peak_rev:,.2f})")

# Insight 4: Marketing ROI correlation
corr_val = df['MarketingSpend'].corr(df['Revenue']).round(4)
print(f"[INSIGHT 4] Marketing Spend vs Revenue Correlation: {corr_val}")

# Insight 5: Return rate by category
return_by_cat = df.groupby('Category')['ReturnRate'].mean().round(4)
lowest_return_cat = return_by_cat.idxmin()
print(f"[INSIGHT 5] Lowest Return Rate Category: {lowest_return_cat} ({return_by_cat[lowest_return_cat]*100:.2f}%)")

# Insight 6: Customer segment revenue
print("\n[INSIGHT 6] Revenue by Customer Segment:")
seg_rev = df.groupby('CustomerSegment')['Revenue'].sum().sort_values(ascending=False).round(2)
for seg, rev in seg_rev.items():
    print(f"   {seg}: ${rev:,.2f}")

# Insight 7: Best product
print("\n[INSIGHT 7] Top 5 Products by Revenue:")
top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5).round(2)
for prod, rev in top_products.items():
    print(f"   {prod}: ${rev:,.2f}")

# Insight 8: Profit margin analysis
df['ProfitMargin'] = (df['Profit'] / df['Revenue'] * 100).round(2)
print(f"\n[INSIGHT 8] Overall Profit Margin: {df['ProfitMargin'].mean():.2f}%")
print("Profit Margin by Category:")
print(df.groupby('Category')['ProfitMargin'].mean().round(2))

print("\nEDA completed successfully!")
print("Run dashboard.py to generate visual charts.")
