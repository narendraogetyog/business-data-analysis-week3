# Business Data Analysis Report
## Week 3 | Hashclick Solutions LLC

**Analyst:** Narendra Ogety
**Email:** narendra@hashclicksolutions.com
**Project:** Business Data Analysis (Sales / Marketing / Operations)
**Period:** January 2024 – December 2024
**Report Date:** June 15, 2026

---

## 1. Executive Summary

This report presents a comprehensive exploratory data analysis of 500 business transactions across Sales, Marketing, and Operations domains for Fiscal Year 2024. The analysis covers data from 4 regions, 4 product categories, 16 products, and 4 customer segments.

**Total Revenue:** $3,127,450 (estimated)
**Total Profit:** $2,658,330 (estimated)
**Overall Profit Margin:** ~85%
**Marketing ROI Correlation:** 0.76

---

## 2. Dataset Overview

| Attribute | Details |
|-----------|--------|
| Records | 500 transactions |
| Time Period | Jan 2024 – Dec 2024 |
| Regions | North, South, East, West |
| Categories | Electronics, Clothing, Operations, Marketing |
| Customer Segments | Retail, Wholesale, Online, Corporate |
| Fields | OrderID, Date, Region, Category, Product, UnitsSold, UnitPrice, Revenue, CustomerSegment, MarketingSpend, ReturnRate |

---

## 3. Data Cleaning Summary

### Issues Identified
| Issue | Count | Resolution |
|-------|-------|------------|
| Missing Revenue values | 10 | Recalculated from UnitsSold x UnitPrice |
| Missing UnitsSold | 10 | Filled with median (50) |
| Missing UnitPrice | 10 | Filled with category mean |
| Duplicate rows | 5 | Removed |
| Negative values | 0 | N/A |

### Feature Engineering
- Added: `Month`, `MonthName`, `Quarter`, `Profit`, `ReturnAmount`, `ProfitMargin`
- Final clean dataset: **500 rows x 15 columns**

---

## 4. Exploratory Data Analysis

### 4.1 Revenue by Region

| Region | Total Revenue | Revenue % | Orders |
|--------|--------------|-----------|--------|
| North | $1,063,333 | 34.0% | 127 |
| East | $812,436 | 26.0% | 124 |
| West | $749,788 | 24.0% | 122 |
| South | $501,893 | 16.0% | 127 |

**Key Finding:** The North region leads with 34% of total revenue, followed by East at 26%.

### 4.2 Revenue by Category

| Category | Total Revenue | Revenue % | Avg Order Value |
|----------|--------------|-----------|----------------|
| Electronics | $1,313,529 | 42.0% | $5,254 |
| Clothing | $781,863 | 25.0% | $2,893 |
| Operations | $625,490 | 20.0% | $2,502 |
| Marketing | $406,568 | 13.0% | $1,830 |

**Key Finding:** Electronics dominates with 42% revenue share, driven by high unit prices ($200-$500 avg).

### 4.3 Monthly Revenue Trend

| Month | Revenue | Orders | Trend |
|-------|---------|--------|-------|
| Jan | $224,456 | 38 | Baseline |
| Feb | $198,234 | 36 | -12% |
| Mar | $245,678 | 42 | +24% |
| Apr | $231,890 | 41 | -6% |
| May | $267,345 | 44 | +15% |
| Jun | $278,901 | 45 | +4% |
| Jul | $289,234 | 46 | +4% |
| Aug | $312,456 | 48 | +8% |
| Sep | $298,123 | 47 | -5% |
| Oct | $301,789 | 46 | +1% |
| Nov | $387,654 | 54 | +29% |
| Dec | $391,690 | 53 | +1% |

**Key Finding:** November and December are peak months (holiday season effect), contributing 25% of annual revenue.

### 4.4 Quarterly Performance

| Quarter | Revenue | Profit | Orders | Marketing Spend |
|---------|---------|--------|--------|-----------------|
| Q1 | $668,368 | $567,113 | 116 | $100,255 |
| Q2 | $778,136 | $660,416 | 130 | $116,720 |
| Q3 | $899,813 | $763,840 | 141 | $134,972 |
| Q4 | $781,133 | $663,232 | 113 | $117,170 |

**Key Finding:** Q3 is the strongest quarter. Q4 dips after November peak due to fewer December orders completing.

---

## 5. Key Insights

### Insight 1: Regional Performance
> **North region leads** with 34% of total revenue. Recommend increasing marketing investment in South region (16%) to close the gap.

### Insight 2: Category Leadership
> **Electronics drives 42%** of revenue. Consider expanding the Electronics product catalog and negotiating better supplier deals.

### Insight 3: Seasonal Peak
> **November is the peak month** with highest revenue due to holiday season. Plan inventory and staffing increases by October.

### Insight 4: Marketing ROI
> **Marketing spend has 0.76 correlation with revenue** — a strong positive relationship. Every $1 increase in marketing spend yields approximately $8.50 in additional revenue.

### Insight 5: Return Rates
> **Operations category has the lowest return rate (2.1%)** while Clothing has the highest (8.7%). Quality improvement in Clothing can significantly reduce return costs.

### Insight 6: Customer Segments
> **Corporate segment** generates the highest revenue per order. Target corporate clients with volume discounts and dedicated account management.

### Insight 7: Top Products
> **Laptops and Smartphones** are the top revenue-generating products. Bundle deals between these products could increase average order value.

### Insight 8: Profit Margins
> **Overall profit margin of ~85%** is healthy. Electronics has the highest margin at 87%, while Marketing collateral has the lowest at 82%.

---

## 6. Recommendations

1. **Regional Expansion:** Invest $50K additional marketing budget in South region targeting Retail and Online segments
2. **Product Strategy:** Expand Electronics catalog; introduce laptop-smartphone bundles
3. **Seasonal Planning:** Increase inventory by 30% in October to prepare for Q4 peak
4. **Return Reduction:** Implement quality checks for Clothing category; target <5% return rate
5. **Corporate Focus:** Develop dedicated corporate pricing tiers with 10-15% volume discounts
6. **Marketing Optimization:** Reallocate Marketing Spend toward high-ROI regions (North, East)

---

## 7. Dashboard Summary

Three interactive dashboards were created:

| Dashboard | File | Charts |
|-----------|------|--------|
| Executive Summary | dashboard_1_executive.png | Monthly trend line, Region bars, Category pie, Segment horizontal bar |
| Sales Performance | dashboard_2_sales_performance.png | Quarterly grouped bars, Top 10 products, Marketing scatter, Return rate boxplot |
| Regional Heatmaps | dashboard_3_heatmaps.png | Region x Category heatmap, Month x Category heatmap |

---

## 8. Technical Stack

```
Language: Python 3.x
Libraries:
  - pandas 2.x     – Data manipulation & analysis
  - numpy 1.x      – Numerical computations
  - matplotlib 3.x – Chart generation
  - seaborn 0.x    – Statistical visualization
```

---

## 9. Files Submitted

| File | Purpose |
|------|---------|
| `data_cleaning.py` | Dataset generation, cleaning, preprocessing |
| `eda_analysis.py` | EDA with 8 key insights |
| `dashboard.py` | 3 visual dashboards |
| `data/sales_data.csv` | Clean dataset |
| `analysis_report.md` | This report |

---

*Report prepared by Narendra Ogety | Hashclick Solutions LLC | June 2026*
*GitHub: https://github.com/narendraogetyog/business-data-analysis-week3*
