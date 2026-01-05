"""
H1B Wage Data Processor
Processes OFLC wage data to identify top cities and analyze county-level wages
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Define data paths
DATA_DIR = Path("OFLC_Wages_2025-26_Updated")
WAGE_FILE = DATA_DIR / "ALC_Export.csv"
GEO_FILE = DATA_DIR / "Geography.csv"
OCC_FILE = DATA_DIR / "oes_soc_occs.csv"

# Define occupation codes of interest
OCCUPATIONS = {
    '15-1252': 'Software Developers',
    '15-2051': 'Data Scientists',
    '15-1243': 'Database Architects',
    '15-1244': 'Network and Computer Systems Administrators',
    '15-1211': 'Computer Systems Analysts',
    '15-1212': 'Information Security Analysts',
    '17-2051': 'Civil Engineers',
}


class H1BWageDataProcessor:
    """Process and analyze H1B wage data"""

    def __init__(self):
        self.wages_df = None
        self.geo_df = None
        self.occ_df = None
        self.merged_df = None

    def load_data(self):
        """Load all required data files"""
        print("Loading wage data...")
        self.wages_df = pd.read_csv(WAGE_FILE)

        print("Loading geography data...")
        self.geo_df = pd.read_csv(GEO_FILE)

        print("Loading occupation data...")
        self.occ_df = pd.read_csv(OCC_FILE)

        print(f"Loaded {len(self.wages_df):,} wage records")
        print(f"Loaded {len(self.geo_df):,} geography records")
        print(f"Loaded {len(self.occ_df):,} occupation records")

    def process_geography(self):
        """Process geography data to identify MSAs and counties"""
        # Filter for MSA areas (not non-metropolitan)
        self.geo_df['IsMSA'] = ~self.geo_df['AreaName'].str.contains(
            'nonmetropolitan',
            case=False,
            na=False
        )

        # Clean area codes
        self.geo_df['Area'] = self.geo_df['Area'].astype(str)
        self.wages_df['Area'] = self.wages_df['Area'].astype(str)

        # Extract city name from area name (remove state abbreviations)
        self.geo_df['CityName'] = self.geo_df['AreaName'].str.replace(
            r',\s*[A-Z]{2}(-[A-Z]{2})*$', '', regex=True
        )

        return self.geo_df

    def filter_occupations(self):
        """Filter wage data for specific occupations"""
        occ_codes = list(OCCUPATIONS.keys())
        self.wages_df = self.wages_df[
            self.wages_df['SocCode'].isin(occ_codes)
        ]

        print(f"Filtered to {len(self.wages_df):,} records for target occupations")
        return self.wages_df

    def merge_data(self):
        """Merge wage and geography data"""
        self.merged_df = self.wages_df.merge(
            self.geo_df,
            on='Area',
            how='inner'
        )

        # Add occupation titles
        self.merged_df['OccupationTitle'] = self.merged_df['SocCode'].map(OCCUPATIONS)

        # Convert wage columns to numeric
        wage_cols = ['Level1', 'Level2', 'Level3', 'Level4', 'Average']
        for col in wage_cols:
            self.merged_df[col] = pd.to_numeric(self.merged_df[col], errors='coerce')

        # Calculate annual salaries (hourly rate × 2080 hours/year)
        for col in wage_cols:
            annual_col = f'{col}_Annual'
            self.merged_df[annual_col] = (self.merged_df[col] * 2080).round(2)

        print(f"Merged data contains {len(self.merged_df):,} records")
        return self.merged_df

    def get_top_cities(self, n=200):
        """
        Get top N cities by number of wage records (proxy for employment size)
        Filters for MSAs only
        """
        # Filter for MSAs only
        msa_data = self.merged_df[self.merged_df['IsMSA'] == True].copy()

        # Count records per city
        city_counts = msa_data.groupby(['Area', 'AreaName', 'CityName']).size()
        city_counts = city_counts.reset_index(name='RecordCount')

        # Sort and get top N
        top_cities = city_counts.nlargest(n, 'RecordCount')

        print(f"Identified top {n} cities")
        return top_cities

    def analyze_county_wages(self, city_areas=None, occupation=None):
        """
        Analyze wages at county level for specified cities and occupation

        Args:
            city_areas: List of area codes to filter by (None = all top cities)
            occupation: SOC code to filter by (None = all occupations)
        """
        df = self.merged_df.copy()

        # Filter by cities if specified
        if city_areas is not None:
            df = df[df['Area'].isin(city_areas)]

        # Filter by occupation if specified
        if occupation is not None:
            df = df[df['SocCode'] == occupation]

        # Group by area, city, county, and occupation
        county_analysis = df.groupby([
            'Area', 'AreaName', 'CityName', 'State',
            'CountyTownName', 'SocCode', 'OccupationTitle'
        ]).agg({
            'Level1': 'mean',
            'Level2': 'mean',
            'Level3': 'mean',
            'Level4': 'mean',
            'Average': 'mean',
            'Level1_Annual': 'mean',
            'Level2_Annual': 'mean',
            'Level3_Annual': 'mean',
            'Level4_Annual': 'mean',
            'Average_Annual': 'mean'
        }).reset_index()

        # Round wages to 2 decimal places
        wage_cols = ['Level1', 'Level2', 'Level3', 'Level4', 'Average']
        annual_cols = ['Level1_Annual', 'Level2_Annual', 'Level3_Annual', 'Level4_Annual', 'Average_Annual']
        county_analysis[wage_cols] = county_analysis[wage_cols].round(2)
        county_analysis[annual_cols] = county_analysis[annual_cols].round(0)  # Round to whole dollars

        return county_analysis

    def get_lowest_wage_counties(self, top_city_areas, occupation, wage_level='Level1', n=20):
        """
        Get counties with lowest wages for a specific occupation and wage level

        Args:
            top_city_areas: List of area codes for top cities
            occupation: SOC code
            wage_level: Which wage level to analyze (Level1, Level2, etc.)
            n: Number of counties to return
        """
        county_data = self.analyze_county_wages(
            city_areas=top_city_areas,
            occupation=occupation
        )

        # Sort by wage level and get lowest N
        lowest = county_data.nsmallest(n, wage_level)

        return lowest

    def process_all(self):
        """Run complete data processing pipeline"""
        print("\n" + "="*60)
        print("H1B Wage Data Processing Pipeline")
        print("="*60 + "\n")

        self.load_data()
        print()

        self.process_geography()
        self.filter_occupations()
        self.merge_data()
        print()

        # Get top 200 cities
        top_cities = self.get_top_cities(200)

        # Save processed data
        print("\nSaving processed data...")
        self.merged_df.to_csv(DATA_DIR / 'processed_wage_data.csv', index=False)
        top_cities.to_csv(DATA_DIR / 'top_200_cities.csv', index=False)

        print(f"Saved processed data to {DATA_DIR}")
        print("\n" + "="*60)
        print("Processing Complete!")
        print("="*60)

        return self.merged_df, top_cities


if __name__ == "__main__":
    processor = H1BWageDataProcessor()
    merged_df, top_cities = processor.process_all()

    # Display sample statistics
    print("\n\nSample Statistics:")
    print("-" * 60)
    print(f"\nTop 10 Cities by Record Count:")
    print(top_cities.head(10).to_string(index=False))

    print("\n\nSample Wage Data (Software Developers in Top City):")
    sample = merged_df[
        (merged_df['SocCode'] == '15-1252') &
        (merged_df['Area'] == top_cities.iloc[0]['Area'])
    ].head()
    print(sample[['AreaName', 'CountyTownName', 'Level1', 'Level2', 'Level3', 'Level4']].to_string(index=False))
