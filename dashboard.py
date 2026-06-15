"""
dashboard.py
Week 3 - Business Data Analysis | Hashclick Solutions LLC
Author: Narendra Ogety
Task 5: Create Visual Dashboards using Matplotlib and Seaborn
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server use
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

# ============================================================
# SETUP
# ============================================================

sns.set_theme(style='darkgrid', palette='muted')
PLOT_DIR = 'plots'
os.makedirs(PLOT_DIR, exist_ok=True)

# Load data (generate if needed)
try:
    df = pd.read_csv('data/sales_data.csv', parse_dates=['Date'])
except FileNotFoundError:
    import subprocess
    subprocess.run(['python', 'data_cleaning.py'])
    df = pd.read_csv('data/sales_data.csv', parse_dates=['Date'])

print("Generating dashboards...")

# ============================================================
# DASHBOARD 1: EXECUTIVE SUMMARY (2x3 grid)
# ============================================================

fig = plt.figure(figsize=(18, 12))
fig.suptitle('Business Data Analysis - Executive Dashboard\nHashclick Solutions LLC | Week 3 | Narendra Ogety',
             fontsize=16, fontweight='bold', y=0.98)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# Plot 1: Monthly Revenue Trend (Line Chart)
ax1 = fig.add_subplot(gs[0, :])
monthly_rev = df.groupby('Month')['Revenue'].sum()
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax1.plot(month_names, monthly_rev.values, marker='o', linewidth=2.5,
         color='steelblue', markersize=8)
ax1.fill_between(range(12), monthly_rev.values, alpha=0.2, color='steelblue')
ax1.set_title('Monthly Revenue Trend (2024)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($)')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
for i, v in enumerate(monthly_rev.values):
    ax1.annotate(f'${v:,.0f}', (i, v), textcoords='offset points',
                 xytext=(0, 8), ha='center', fontsize=7)

# Plot 2: Revenue by Region (Bar Chart)
ax2 = fig.add_subplot(gs[1, 0])
reg_rev = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
colors = sns.color_palette('Blues_d', len(reg_rev))
bars = ax2.bar(reg_rev.index, reg_rev.values, color=colors, edgecolor='white')
ax2.set_title('Revenue by Region', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Revenue ($)')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
for bar, val in zip(bars, reg_rev.values):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 500,
             f'${val:,.0f}', ha='center', va='bottom', fontsize=8)

# Plot 3: Revenue by Category (Pie Chart)
ax3 = fig.add_subplot(gs[1, 1])
cat_rev = df.groupby('Category')['Revenue'].sum()
wedge_props = dict(width=0.6, edgecolor='white')
ax3.pie(cat_rev.values, labels=cat_rev.index,
        autopct='%1.1f%%', startangle=90,
        colors=sns.color_palette('Set2', len(cat_rev)),
        wedgeprops=wedge_props)
ax3.set_title('Revenue Share by Category', fontsize=12, fontweight='bold')

# Plot 4: Customer Segment Revenue (Horizontal Bar)
ax4 = fig.add_subplot(gs[1, 2])
seg_rev = df.groupby('CustomerSegment')['Revenue'].sum().sort_values()
ax4.barh(seg_rev.index, seg_rev.values,
         color=sns.color_palette('Greens_d', len(seg_rev)))
ax4.set_title('Revenue by Customer Segment', fontsize=12, fontweight='bold')
ax4.set_xlabel('Total Revenue ($)')
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

plt.savefig(f'{PLOT_DIR}/dashboard_1_executive.png', dpi=150, bbox_inches='tight')
print(f"Saved: {PLOT_DIR}/dashboard_1_executive.png")
plt.close()

# ============================================================
# DASHBOARD 2: SALES PERFORMANCE ANALYSIS
# ============================================================

fig2, axes = plt.subplots(2, 2, figsize=(16, 12))
fig2.suptitle('Sales Performance Analysis Dashboard',
              fontsize=15, fontweight='bold')

# Plot 1: Quarterly Revenue vs Profit
quarterly = df.groupby('Quarter')[['Revenue', 'Profit', 'MarketingSpend']].sum()
ax = axes[0, 0]
width = 0.3
x = np.arange(4)
ax.bar(x - width, quarterly['Revenue'], width, label='Revenue', color='steelblue')
ax.bar(x, quarterly['Profit'], width, label='Profit', color='seagreen')
ax.bar(x + width, quarterly['MarketingSpend'], width, label='Marketing Spend', color='coral')
ax.set_title('Quarterly: Revenue vs Profit vs Marketing', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Plot 2: Top 10 Products by Revenue
ax = axes[0, 1]
top10 = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(10)
ax.barh(top10.index[::-1], top10.values[::-1],
        color=sns.color_palette('viridis', 10))
ax.set_title('Top 10 Products by Revenue', fontweight='bold')
ax.set_xlabel('Total Revenue ($)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Plot 3: Marketing Spend vs Revenue Scatter
ax = axes[1, 0]
for cat, grp in df.groupby('Category'):
    ax.scatter(grp['MarketingSpend'], grp['Revenue'],
               label=cat, alpha=0.5, s=20)
m, b = np.polyfit(df['MarketingSpend'], df['Revenue'], 1)
x_line = np.linspace(df['MarketingSpend'].min(), df['MarketingSpend'].max(), 100)
ax.plot(x_line, m * x_line + b, 'r--', linewidth=1.5, label='Trend Line')
ax.set_title('Marketing Spend vs Revenue Correlation', fontweight='bold')
ax.set_xlabel('Marketing Spend ($)')
ax.set_ylabel('Revenue ($)')
ax.legend(fontsize=8)

# Plot 4: Return Rate by Category (Box plot)
ax = axes[1, 1]
df.boxplot(column='ReturnRate', by='Category', ax=ax,
           patch_artist=True)
ax.set_title('Return Rate Distribution by Category', fontweight='bold')
plt.sca(ax)
plt.title('Return Rate Distribution by Category')
plt.suptitle('')
ax.set_xlabel('Category')
ax.set_ylabel('Return Rate')

plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/dashboard_2_sales_performance.png', dpi=150, bbox_inches='tight')
print(f"Saved: {PLOT_DIR}/dashboard_2_sales_performance.png")
plt.close()

# ============================================================
# DASHBOARD 3: HEATMAP - Regional Category Performance
# ============================================================

fig3, axes3 = plt.subplots(1, 2, figsize=(16, 6))
fig3.suptitle('Regional & Seasonal Analysis Dashboard', fontsize=14, fontweight='bold')

# Heatmap: Revenue by Region x Category
pivot = df.pivot_table(values='Revenue', index='Region',
                        columns='Category', aggfunc='sum')
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.5, ax=axes3[0])
axes3[0].set_title('Revenue Heatmap: Region x Category', fontweight='bold')

# Heatmap: Monthly x Category Revenue
pivot2 = df.pivot_table(values='Revenue', index='MonthName',
                         columns='Category', aggfunc='sum')
month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
pivot2 = pivot2.reindex([m for m in month_order if m in pivot2.index])
sns.heatmap(pivot2, annot=True, fmt='.0f', cmap='Blues',
            linewidths=0.3, ax=axes3[1])
axes3[1].set_title('Monthly Revenue Heatmap: Month x Category', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/dashboard_3_heatmaps.png', dpi=150, bbox_inches='tight')
print(f"Saved: {PLOT_DIR}/dashboard_3_heatmaps.png")
plt.close()

print("\nAll dashboards generated successfully!")
print(f"Files saved in '{PLOT_DIR}/' directory:")
for f in os.listdir(PLOT_DIR):
    print(f"  - {f}")
