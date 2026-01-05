# H1B Wage Dashboard - Usage Guide

## Dashboard Overview

This guide walks you through using each feature of the H1B Wage Analysis Dashboard.

## Getting Started

After running `streamlit run app.py`, you'll see the main dashboard with:
- **Title**: "H1B Wage Analysis Dashboard"
- **Navigation Sidebar** (left): Choose between 3 main views
- **Main Content Area** (center/right): Interactive visualizations and data

## Navigation Sidebar

The sidebar contains:

### View Selection
- Overall Statistics
- City Comparison
- Occupation Insights

### About the Data Section
Shows:
- Data source (OFLC OEWS)
- Time period (2025-2026)
- Number of cities (200)
- Covered occupations

### Wage Levels Explanation
- **Level 1**: Entry level
- **Level 2**: Qualified (most common)
- **Level 3**: Experienced
- **Level 4**: Fully competent

💡 **Tip**: Lower wages = Better H1B approval chances

---

## View 1: Overall Statistics

**Purpose**: Get a high-level overview of the entire dataset

### What You'll See:

#### 1. Key Metrics (4 cards across the top)
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Total Cities    │ Total Counties  │ States Covered  │ Total Records   │
│    200          │    ~500         │      50         │    ~50,000      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### 2. Top 20 Cities Table
Shows cities ranked by employment data volume:
- City name (e.g., "New York-Newark-Jersey City")
- Full area name with states
- Record count

**Example**:
| # | City Name | Area Name | Record Count |
|---|-----------|-----------|--------------|
| 1 | New York-Newark-Jersey City | New York-Newark-Jersey City, NY-NJ-PA | 1,234 |
| 2 | Los Angeles | Los Angeles-Long Beach-Anaheim, CA | 1,156 |
| 3 | Chicago | Chicago-Naperville-Elgin, IL-IN-WI | 987 |

#### 3. Occupation Distribution Bar Chart
- X-axis: Occupation names
- Y-axis: Number of wage records
- Color gradient: Darker = more records

**Insight**: Shows which occupations have the most data coverage

#### 4. Average Wages by Occupation (Grouped Bar Chart)
- Compares all 4 wage levels across occupations
- Each occupation has 4 bars (Level 1-4)
- Hover to see exact wage amounts

**Insight**: Identify which occupations pay more/less overall

---

## View 2: City Comparison (Most Important!)

**Purpose**: Compare specific cities to find the best location for your H1B

### Step-by-Step Usage:

#### Step 1: Select Cities
```
┌─────────────────────────────────────────────────────────────┐
│ Select Cities to Compare (select 2-10 cities)               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [x] New York                                             │ │
│ │ [x] San Francisco                                        │ │
│ │ [x] Seattle                                              │ │
│ │ [ ] Austin                                               │ │
│ │ [ ] Boston                                               │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Tips**:
- Start with 3-5 cities you're considering
- You can select up to 10 cities
- Cities are sorted alphabetically

#### Step 2: Select Occupation
```
┌────────────────────────────────────────┐
│ Select Occupation                       │
│ ┌────────────────────────────────────┐ │
│ │ Software Developers              ▼ │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

Options:
- Software Developers
- Data Scientists
- Database Architects
- Network/Systems Administrators
- Computer Systems Analysts
- Information Security Analysts
- Civil Engineers

#### Step 3: View Results

**A. Lowest Wage Counties (Two Tables Side-by-Side)**

Left Table: **Lowest Level 1 Wages (Best for Entry)**
| # | City | County | State | Level 1 |
|---|------|--------|-------|---------|
| 1 | Austin | Hays County | TX | $28.50/hr |
| 2 | Seattle | Snohomish County | WA | $29.15/hr |
| 3 | New York | Nassau County | NY | $30.25/hr |

Right Table: **Lowest Level 2 Wages (Best for Qualified)**
| # | City | County | State | Level 2 |
|---|------|--------|-------|---------|
| 1 | Austin | Williamson County | TX | $35.20/hr |
| 2 | Seattle | Pierce County | WA | $36.80/hr |
| 3 | New York | Westchester County | NY | $38.50/hr |

**What This Means**:
- These counties have the LOWEST wage requirements
- Lower wages = easier to meet prevailing wage threshold
- Better chance of H1B approval

**B. Wage Distribution Box Plot**

Interactive chart showing:
- X-axis: Cities you selected
- Y-axis: Hourly wage
- 4 boxes per city (one for each wage level)
- Shows median, quartiles, and outliers

**How to Read**:
- Box bottom = 25th percentile
- Line in box = median
- Box top = 75th percentile
- Whiskers = min/max (excluding outliers)

**C. Detailed County Wage Table**

Scrollable table with ALL counties in selected cities:
| City | State | County | Level 1 | Level 2 | Level 3 | Level 4 |
|------|-------|--------|---------|---------|---------|---------|
| Austin | TX | Travis County | $32.10 | $41.48 | $50.85 | $60.23 |
| Austin | TX | Williamson County | $30.50 | $39.20 | $48.15 | $57.00 |

**Features**:
- Sort by clicking column headers
- Scroll to see all counties
- Formatted as currency

#### Step 4: Download Data

```
┌────────────────────────────────────────┐
│ 📥 Download County Data as CSV          │
└────────────────────────────────────────┘
```

Downloads a CSV file with:
- All counties from selected cities
- All wage levels (numeric format)
- Ready for Excel or further analysis

**Filename format**: `h1b_wages_15-1252_New-York-San-Francisco-Seattle.csv`

---

## View 3: Occupation Insights

**Purpose**: Deep dive into a single occupation across ALL 200 cities

### Step 1: Select Occupation
```
┌────────────────────────────────────────┐
│ Select Occupation for Detailed Analysis│
│ ┌────────────────────────────────────┐ │
│ │ Data Scientists                  ▼ │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Step 2: View Top Counties Nationwide

**A. Top 10 Counties: Lowest Level 1 Wages**
| # | City | State | County | Level 1 |
|---|------|-------|--------|---------|
| 1 | McAllen | TX | Hidalgo County | $25.00/hr |
| 2 | El Paso | TX | El Paso County | $26.71/hr |
| 3 | Corpus Christi | TX | Nueces County | $27.15/hr |

**B. Top 10 Counties: Lowest Level 2 Wages**
| # | City | State | County | Level 2 |
|---|------|-------|--------|---------|
| 1 | McAllen | TX | Hidalgo County | $34.00/hr |
| 2 | Brownsville | TX | Cameron County | $35.24/hr |
| 3 | El Paso | TX | El Paso County | $37.00/hr |

**Insight**: Identifies the absolute best counties nationwide for this occupation

### Step 3: Geographic Distribution

**State-Level Wage Comparison Bar Chart**
- Shows top 20 states by lowest average wages
- Compares Level 1 and Level 2 side-by-side
- Sorted by Level 2 wages (ascending)

**Example**:
```
Texas         ████████░ $35.50
Oklahoma      █████████░ $36.20
Arkansas      ██████████ $37.80
...
```

**Use Case**: Identify states with consistently lower wages

---

## Common Workflows

### Workflow 1: "I want to work in a specific city"

1. Go to **City Comparison**
2. Select your target city + 2-3 alternatives
3. Select your occupation
4. Check "Lowest Level 2 Wages" table
5. Identify specific counties with best wages
6. Download data for reference

### Workflow 2: "I'm flexible on location, just want best H1B odds"

1. Go to **Occupation Insights**
2. Select your occupation
3. View "Top 10 Counties: Lowest Level 2 Wages"
4. Note the top 3-5 counties
5. Go to **City Comparison**
6. Select those cities
7. Deep dive into county data

### Workflow 3: "I want to compare my occupation against others"

1. Go to **Overall Statistics**
2. View "Average Wages by Occupation" chart
3. Identify where your occupation ranks
4. Note occupations with similar wages
5. Use **Occupation Insights** for each occupation
6. Compare geographic distributions

### Workflow 4: "I need data for multiple cities and occupations"

1. Go to **City Comparison**
2. Select first set of cities
3. Select occupation A
4. Download CSV
5. Change occupation to B
6. Download CSV
7. Repeat for all combinations
8. Merge CSVs in Excel for analysis

---

## Tips & Best Practices

### For H1B Applicants

1. **Focus on Level 2**: Most H1B positions are classified as Level 2 (Qualified)

2. **County Matters**: Within the same metro area, counties can have significantly different wages

3. **Multiple Options**: Compare at least 5 cities to find optimal location

4. **Consider Cost of Living**: Low wages are good for H1B, but check if you can afford to live there

5. **Verify with Employer**: Your employer must post your position at the prevailing wage or higher

### For Data Analysis

1. **Download Data**: Export CSVs for offline analysis in Excel/Python

2. **Sort Tables**: Click column headers to sort by different wage levels

3. **Use Box Plots**: Great for understanding wage variance within cities

4. **Cross-Reference**: Use all 3 views together for comprehensive analysis

### For Decision Making

1. **Start Broad**: Use Overall Statistics to understand landscape

2. **Narrow Down**: Use Occupation Insights to identify promising states/cities

3. **Deep Dive**: Use City Comparison to analyze specific counties

4. **Export & Share**: Download data to discuss with family/employer

---

## Understanding the Data

### Wage Levels Explained

| Level | Title | Description | Typical Experience |
|-------|-------|-------------|-------------------|
| 1 | Entry | Basic understanding | 0-2 years |
| 2 | Qualified | Moderate skills | 2-4 years |
| 3 | Experienced | Advanced skills | 4-6 years |
| 4 | Fully Competent | Expert | 6+ years |

### Geographic Hierarchy

```
United States
    └── State (e.g., Texas)
        └── Metropolitan Statistical Area (MSA) (e.g., Austin, TX)
            └── County (e.g., Travis County, Williamson County)
```

The dashboard shows MSAs (cities) and their component counties.

### Why Lower Wages Are Better for H1B

Under the new wage-based H1B selection system:
- Applications are sorted by offered wage
- Higher wages get priority in lottery
- BUT: Your wage must meet prevailing wage minimum
- Lower prevailing wage = easier to exceed threshold
- Exceeding by higher % = better lottery odds

**Example**:
- County A: Level 2 = $40/hr (prevailing wage)
- County B: Level 2 = $35/hr (prevailing wage)

If offered $50/hr:
- County A: $50/$40 = 125% of prevailing (25% above)
- County B: $50/$35 = 143% of prevailing (43% above)

**County B gives better H1B odds!**

---

## Troubleshooting

### "No data available for selected filters"
- Try different city combinations
- Check if occupation is available in those cities
- Try broader selection (more cities)

### Dashboard is slow
- Select fewer cities (5 instead of 10)
- Refresh the page
- Check internet connection

### Data looks wrong
- Verify you ran `data_processor.py` first
- Check that processed CSV files exist
- Re-run data processor if needed

### Can't find my city
- Dashboard only shows top 200 MSAs
- Try nearby larger cities
- Check if your city is part of a larger MSA

---

## Next Steps

After using the dashboard:

1. **Shortlist Locations**: Identify 3-5 optimal counties

2. **Research Further**:
   - Cost of living
   - Job market for your occupation
   - Quality of life factors

3. **Contact Employers**: Look for jobs in identified counties

4. **Prepare Application**: Use wage data to negotiate fair compensation

5. **Stay Updated**: Wages update annually (July-June cycle)

---

## Future Features (Coming Soon)

- **AI Chatbot**: Ask questions in natural language
- **Trend Analysis**: See how wages change year-over-year
- **Approval Predictions**: Estimate H1B approval probability
- **Cost of Living Overlay**: Adjust wages for local costs
- **PDF Reports**: Generate shareable reports

---

For technical documentation, see [README.md](README.md)

For quick installation, see [QUICKSTART.md](QUICKSTART.md)

For project details, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
