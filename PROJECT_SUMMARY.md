# H1B Wage Analysis Dashboard - Project Summary

## Overview

A comprehensive, interactive Streamlit dashboard designed to help H1B visa applicants identify optimal US locations (cities and counties) with the lowest prevailing wage requirements, thereby improving their chances of H1B approval under the new wage-based selection system.

## What We Built

### 1. Data Processing Pipeline ([data_processor.py](data_processor.py))

**Key Features:**
- Loads and processes 449,441+ wage records from OFLC OEWS data
- Identifies top 200 US Metropolitan Statistical Areas (MSAs)
- Filters data for 7 key tech and engineering occupations
- Merges wage data with geographic information (counties, states)
- Generates optimized CSV files for dashboard consumption

**Core Functionality:**
```python
class H1BWageDataProcessor:
    - load_data()              # Load wage, geography, occupation data
    - process_geography()      # Filter MSAs, extract city names
    - filter_occupations()     # Filter for target SOC codes
    - merge_data()            # Combine all data sources
    - get_top_cities()        # Identify top 200 cities
    - analyze_county_wages()  # County-level wage analysis
    - get_lowest_wage_counties() # Find best locations
```

**Output Files:**
- `processed_wage_data.csv` - Complete merged dataset
- `top_200_cities.csv` - Top 200 cities by employment data

### 2. Interactive Streamlit Dashboard ([app.py](app.py))

**Three Main Sections:**

#### A. Overall Statistics View
- **Key Metrics Dashboard**
  - Total cities analyzed (200)
  - Total counties covered
  - States represented
  - Total wage records

- **Top 20 Cities Display**
  - Ranked by employment data
  - Interactive table with city names and record counts

- **Occupation Distribution**
  - Bar chart showing wage records per occupation
  - Color-coded visualization

- **Average Wages Analysis**
  - Grouped bar chart comparing all 4 wage levels
  - Across all occupations
  - Helps identify high-paying vs low-paying roles

#### B. City Comparison Tool
- **Multi-Select Filters**
  - Select 2-10 cities simultaneously
  - Choose specific occupation
  - Real-time data filtering

- **County-Level Insights**
  - Side-by-side comparison of:
    - Top 15 counties with lowest Level 1 wages
    - Top 15 counties with lowest Level 2 wages
  - Critical for H1B decision-making

- **Interactive Visualizations**
  - Box plots showing wage distribution across cities
  - Displays all 4 wage levels
  - Statistical mean and standard deviation

- **Detailed Data Table**
  - Complete county-level wage breakdown
  - Sortable by any wage level
  - Formatted currency display

- **Export Functionality**
  - Download comparison data as CSV
  - Custom filename with selected cities and occupation

#### C. Occupation Insights
- **Occupation-Specific Analysis**
  - Top 10 counties with lowest Level 1 wages
  - Top 10 counties with lowest Level 2 wages
  - Ranked tables with location details

- **Geographic Distribution**
  - State-level wage comparison
  - Top 20 states displayed
  - Bar chart for Level 1 and Level 2 wages

### 3. Supported Occupations

| SOC Code | Occupation Title |
|----------|-----------------|
| 15-1252 | Software Developers |
| 15-2051 | Data Scientists |
| 15-1243 | Database Architects |
| 15-1244 | Network/Systems Administrators |
| 15-1211 | Computer Systems Analysts |
| 15-1212 | Information Security Analysts |
| 17-2051 | Civil Engineers |

### 4. Supporting Files

- [**requirements.txt**](requirements.txt) - Python dependencies
- [**setup.sh**](setup.sh) - Automated installation script
- [**README.md**](README.md) - Comprehensive documentation
- [**QUICKSTART.md**](QUICKSTART.md) - Step-by-step usage guide

## Technical Architecture

### Data Flow
```
OFLC Raw Data (CSV files)
    ↓
data_processor.py
    ↓
Processed CSVs (filtered, merged, optimized)
    ↓
Streamlit Dashboard (app.py)
    ↓
Interactive Visualizations & Tables
```

### Technology Stack
- **Python 3.8+**: Core language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web dashboard framework
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

## Key Features & Benefits

### For H1B Applicants
1. **Strategic Location Selection**
   - Identify counties with lowest wage requirements
   - Compare multiple cities simultaneously
   - Make data-driven relocation decisions

2. **Improved Approval Chances**
   - Lower prevailing wages = better H1B odds
   - Critical under new wage-based selection system
   - County-level granularity for precision

3. **User-Friendly Interface**
   - No coding required
   - Interactive filters and selections
   - Visual charts and tables
   - Export data for offline analysis

### Technical Highlights
1. **Performance Optimized**
   - Cached data loading (`@st.cache_data`)
   - Efficient pandas operations
   - Minimal memory footprint

2. **Scalable Design**
   - Modular code structure
   - Easy to add new occupations
   - Extensible for additional features

3. **Professional UI/UX**
   - Clean, intuitive navigation
   - Responsive layouts
   - Informative tooltips and help text

## Usage Workflow

1. **Installation**
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

2. **Data Processing**
   ```bash
   python data_processor.py
   ```
   - Takes 2-5 minutes
   - Processes 449K+ records
   - Generates optimized files

3. **Launch Dashboard**
   ```bash
   streamlit run app.py
   ```
   - Opens at localhost:8501
   - Ready for analysis

4. **Analyze & Export**
   - Navigate through 3 main views
   - Filter and compare locations
   - Download results as CSV

## Example Use Cases

### Use Case 1: Software Developer Seeking H1B
**Goal**: Find counties with lowest Level 2 wages for Software Developers

**Steps**:
1. Go to "City Comparison"
2. Select cities: San Francisco, Austin, Seattle, Boston, Denver
3. Select occupation: Software Developers
4. Review "Lowest Level 2 Wages" table
5. Identify optimal county
6. Download data for reference

### Use Case 2: Data Scientist Comparing Multiple Locations
**Goal**: Compare wage requirements across top tech hubs

**Steps**:
1. Go to "Occupation Insights"
2. Select "Data Scientists"
3. View top 10 counties nationwide
4. Check state-level distribution
5. Cross-reference with "City Comparison" for specific cities

### Use Case 3: Civil Engineer Finding Opportunities
**Goal**: Identify non-tech cities with good wage profiles

**Steps**:
1. Go to "Overall Statistics"
2. Review top 20 cities
3. Switch to "City Comparison"
4. Select Civil Engineers
5. Compare 5-10 mid-size cities
6. Export results

## Future Roadmap

### Phase 2: AI Integration (Planned)
- **RAG-based Chatbot**
  - Natural language queries
  - "Show me counties with lowest wages for Data Scientists in California"
  - Context-aware responses

- **LLM Integration**
  - Personalized recommendations
  - Conversational interface
  - Multi-turn dialogue

### Phase 3: Enhanced Features
- Additional occupations (30+ SOC codes)
- Historical wage trend analysis
- H1B filing statistics overlay
- Cost of living adjustments
- PDF report generation
- Email alerts for wage changes

### Phase 4: Advanced Analytics
- Machine learning predictions
- Approval probability calculator
- Custom scoring algorithms
- Clustering similar locations

## File Structure
```
H1B-Wages/
├── app.py                          # Main Streamlit dashboard
├── data_processor.py               # Data processing pipeline
├── requirements.txt                # Python dependencies
├── setup.sh                        # Installation script
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_SUMMARY.md              # This file
└── OFLC_Wages_2025-26_Updated/    # Data directory
    ├── ALC_Export.csv             # Raw wage data (449K records)
    ├── Geography.csv              # Geographic mappings
    ├── oes_soc_occs.csv          # Occupation definitions
    ├── Revised 2025-2026 Technical Release Notes.pdf
    ├── processed_wage_data.csv   # ← Generated by processor
    └── top_200_cities.csv        # ← Generated by processor
```

## Success Metrics

✅ **Functionality**
- Processes 449,441 wage records successfully
- Identifies 200+ metropolitan areas
- Covers 7 key occupations
- Provides county-level granularity

✅ **User Experience**
- Interactive multi-select filters
- Real-time data filtering
- Visual charts and tables
- CSV export capability

✅ **Performance**
- Fast data loading with caching
- Responsive UI interactions
- Efficient memory usage

✅ **Documentation**
- Comprehensive README
- Quick start guide
- Inline code comments
- Usage examples

## Getting Started

1. Read [QUICKSTART.md](QUICKSTART.md) for installation instructions
2. Run `./setup.sh` to install dependencies
3. Execute `python data_processor.py` to process data
4. Launch `streamlit run app.py` to start dashboard
5. Explore the three main sections
6. Export your findings

## Support & Contribution

This is version 1.0 of the dashboard. Future versions will include:
- AI-powered chatbot
- More occupations
- Advanced filtering
- Predictive analytics

For questions or feature requests, refer to the documentation or create an issue.

---

**Built with**: Python, Streamlit, Pandas, Plotly
**Data Source**: OFLC OEWS 2025-2026
**Purpose**: Help H1B applicants make informed location decisions
