# Quick Start Guide

## Prerequisites

- Python 3.8 or higher installed on your system
- Terminal/Command Line access

## Step-by-Step Installation

### Option 1: Automated Setup (Recommended)

1. Open Terminal and navigate to the project directory:
```bash
cd /Users/vsneh/Downloads/Drive-D/H1B-Wages
```

2. Run the setup script:
```bash
./setup.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Process the data:
```bash
python data_processor.py
```

5. Launch the dashboard:
```bash
streamlit run app.py
```

### Option 2: Manual Setup

1. Navigate to the project directory:
```bash
cd /Users/vsneh/Downloads/Drive-D/H1B-Wages
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Process the data:
```bash
python data_processor.py
```

This will take a few minutes to:
- Load ~449,000 wage records
- Filter for top 200 US cities
- Process occupation and geography data
- Generate two output files:
  - `OFLC_Wages_2025-26_Updated/processed_wage_data.csv`
  - `OFLC_Wages_2025-26_Updated/top_200_cities.csv`

6. Launch the dashboard:
```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Using the Dashboard

### 1. Overall Statistics Tab
- View key metrics across all 200 cities
- See top 20 cities by employment data
- Analyze wage records by occupation
- Compare average wages across occupations

### 2. City Comparison Tab
- **Select Cities**: Choose 2-10 cities from the dropdown
- **Select Occupation**: Pick your target occupation
- **View Results**:
  - Lowest Level 1 wages by county
  - Lowest Level 2 wages by county
  - Interactive wage distribution charts
  - Detailed county wage table
- **Download Data**: Export results as CSV

### 3. Occupation Insights Tab
- Select specific occupation
- View top 10 counties with lowest wages
- Analyze geographic distribution by state

## Tips for H1B Applicants

1. **Focus on Level 2 Wages**: Most H1B positions fall under Level 2 (Qualified)

2. **Lower is Better**: Counties with lower prevailing wages have better approval chances

3. **Compare Multiple Cities**: Use the city comparison tool to find optimal locations

4. **Consider County Variations**: Wages can vary significantly between counties in the same metro area

5. **Download Data**: Export comparison data for offline analysis and decision making

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### "Processed data not found"
Run the data processor first:
```bash
python data_processor.py
```

### Dashboard won't open
Check if streamlit is running:
```bash
streamlit --version
```

If not installed, run:
```bash
pip install -r requirements.txt
```

### Port already in use
If port 8501 is busy, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Next Steps

Once the basic dashboard is working, we can add:
- RAG-based chatbot for natural language queries
- Additional occupations
- Historical wage trends
- H1B filing statistics
- PDF report generation

## Support

For questions or issues, refer to the main README.md or create an issue.
