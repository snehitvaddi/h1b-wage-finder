# H1B Wage Finder 💰

Find the lowest H1B prevailing wages for your occupation across US metro areas. Lower wages = Better H1B approval chances.

**Live App**: [h1b-wage-compass.streamlit.app](https://h1b-wage-compass.streamlit.app/)

## Features

- **Salary Recommendations**: Top 20 cities with lowest wages based on your metro area
- **Wage Level Summary**: Filter by state/county, view all 4 wage levels
- **Quick Search**: Fast lookup of lowest wages by occupation
- **Smart Location Search**: Search by city, ZIP code, or county (900+ locations)

## Supported Occupations

- Software Developers
- Data Scientists
- Database Architects/Administrators
- Network/Systems Administrators
- Computer Systems Analysts
- Information Security Analysts
- Civil Engineers

## Quick Start

```bash
# Clone repo
git clone https://github.com/snehitvaddi/h1b-wage-finder.git
cd h1b-wage-finder

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Create new app from this repo
4. Deploy!

## Data Source

- **Source**: OFLC OEWS Wage Data
- **Period**: 2025-2026 (Effective Aug 2025)
- **Coverage**: All US metro areas

## How It Works

- **Level 1**: Entry level
- **Level 2**: Qualified (most common for H1B)
- **Level 3**: Experienced
- **Level 4**: Fully competent

Lower prevailing wages improve H1B approval chances under the wage-based lottery system.

## License

MIT License - For informational purposes only. Verify data independently.

