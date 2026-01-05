"""
Location Search Utility for H1B Wage Dashboard
Helps users find areas by city, county, state, or ZIP code
"""

import pandas as pd
from pathlib import Path
from fuzzywuzzy import fuzz, process
from typing import List, Dict, Tuple, Optional
import requests
import json


class LocationSearchEngine:
    """Search and match user location inputs to OFLC area codes"""

    def __init__(self, geography_df: pd.DataFrame):
        """
        Initialize with geography dataframe

        Args:
            geography_df: DataFrame with Area, AreaName, State, CountyTownName columns
        """
        self.geo_df = geography_df
        self._build_search_index()

    def _build_search_index(self):
        """Build searchable indices for fast lookups"""
        # Create searchable text combining all location info
        self.geo_df['SearchText'] = (
            self.geo_df['AreaName'].fillna('') + ' ' +
            self.geo_df['State'].fillna('') + ' ' +
            self.geo_df['CountyTownName'].fillna('')
        ).str.lower()

        # Extract just city names (remove state abbreviations)
        self.geo_df['CityOnly'] = self.geo_df['AreaName'].str.replace(
            r',\s*[A-Z]{2}(-[A-Z]{2})*$', '', regex=True
        ).str.lower()

        # Create unique area lookup
        self.unique_areas = self.geo_df.groupby('Area').first().reset_index()

        # Build state abbreviation to full name mapping
        self.state_map = dict(zip(
            self.geo_df['StateAb'].str.lower(),
            self.geo_df['State'].str.lower()
        ))

    def search_by_city(self, city_name: str, state: Optional[str] = None,
                       limit: int = 10) -> pd.DataFrame:
        """
        Search for areas by city name

        Args:
            city_name: City name (e.g., "Austin", "San Francisco")
            state: Optional state filter (e.g., "TX", "Texas")
            limit: Maximum number of results

        Returns:
            DataFrame with matching areas
        """
        city_lower = city_name.lower().strip()

        # Filter by state if provided
        df = self.geo_df.copy()
        if state:
            state_lower = state.lower().strip()
            df = df[
                (df['StateAb'].str.lower() == state_lower) |
                (df['State'].str.lower() == state_lower)
            ]

        # Exact match on city name
        exact_matches = df[df['CityOnly'] == city_lower]
        if not exact_matches.empty:
            return exact_matches.groupby('Area').first().reset_index().head(limit)

        # Fuzzy match on city name
        city_options = df['CityOnly'].unique()
        matches = process.extract(city_lower, city_options, limit=limit)

        # Filter matches with score > 70
        good_matches = [m[0] for m in matches if m[1] > 70]

        if good_matches:
            result = df[df['CityOnly'].isin(good_matches)]
            return result.groupby('Area').first().reset_index().head(limit)

        return pd.DataFrame()

    def search_by_county(self, county_name: str, state: Optional[str] = None,
                        limit: int = 10) -> pd.DataFrame:
        """
        Search for areas by county name

        Args:
            county_name: County name (e.g., "Travis County", "Travis")
            state: Optional state filter
            limit: Maximum number of results

        Returns:
            DataFrame with matching areas
        """
        county_lower = county_name.lower().strip()

        # Normalize county name (add "county" if not present)
        if 'county' not in county_lower and 'parish' not in county_lower:
            county_lower_with_suffix = county_lower + ' county'
        else:
            county_lower_with_suffix = county_lower

        df = self.geo_df.copy()

        # Filter by state if provided
        if state:
            state_lower = state.lower().strip()
            df = df[
                (df['StateAb'].str.lower() == state_lower) |
                (df['State'].str.lower() == state_lower)
            ]

        # Search in CountyTownName
        exact_matches = df[
            df['CountyTownName'].str.lower().str.contains(county_lower, na=False)
        ]

        if not exact_matches.empty:
            return exact_matches.head(limit)

        # Fuzzy match
        county_options = df['CountyTownName'].dropna().unique()
        matches = process.extract(county_lower_with_suffix, county_options, limit=limit)

        good_matches = [m[0] for m in matches if m[1] > 70]

        if good_matches:
            return df[df['CountyTownName'].isin(good_matches)].head(limit)

        return pd.DataFrame()

    def search_by_zip(self, zip_code: str) -> pd.DataFrame:
        """
        Search for areas by ZIP code using free geocoding API

        Args:
            zip_code: 5-digit ZIP code

        Returns:
            DataFrame with matching area(s)
        """
        try:
            # Use free Zippopotam API
            response = requests.get(
                f"http://api.zippopotam.us/us/{zip_code}",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()

                # Extract city and state
                if 'places' in data and len(data['places']) > 0:
                    place = data['places'][0]
                    city = place.get('place name', '')
                    state_abbr = place.get('state abbreviation', '')

                    # Search by city and state
                    return self.search_by_city(city, state_abbr, limit=5)

        except Exception as e:
            print(f"ZIP code lookup failed: {e}")

        return pd.DataFrame()

    def smart_search(self, query: str, limit: int = 10) -> pd.DataFrame:
        """
        Intelligent search that handles multiple input types

        Args:
            query: User query (city, county, state, ZIP, or combination)
            limit: Maximum number of results

        Returns:
            DataFrame with matching areas
        """
        query = query.strip()

        # Check if it's a ZIP code (5 digits)
        if query.isdigit() and len(query) == 5:
            return self.search_by_zip(query)

        # Check if query contains state (e.g., "Austin, TX" or "Austin Texas")
        parts = [p.strip() for p in query.replace(',', ' ').split()]

        state = None
        search_term = query

        # Try to identify state in query
        if len(parts) >= 2:
            # Check if last part is a state
            last_part = parts[-1].lower()
            if last_part in self.state_map or last_part in self.state_map.values():
                state = parts[-1]
                search_term = ' '.join(parts[:-1])

        # Try city search first
        city_results = self.search_by_city(search_term, state, limit)
        if not city_results.empty:
            return city_results

        # Try county search
        county_results = self.search_by_county(search_term, state, limit)
        if not county_results.empty:
            return county_results

        # Fallback: fuzzy search on all text
        df = self.geo_df.copy()
        if state:
            state_lower = state.lower()
            df = df[
                (df['StateAb'].str.lower() == state_lower) |
                (df['State'].str.lower() == state_lower)
            ]

        # Fuzzy match on search text
        search_options = df['SearchText'].unique()
        matches = process.extract(query.lower(), search_options, limit=limit)

        good_matches = [m[0] for m in matches if m[1] > 60]

        if good_matches:
            results = df[df['SearchText'].isin(good_matches)]
            return results.groupby('Area').first().reset_index().head(limit)

        return pd.DataFrame()

    def get_area_details(self, area_code: str) -> Dict:
        """
        Get detailed information about an area

        Args:
            area_code: OFLC area code

        Returns:
            Dictionary with area details
        """
        area_data = self.geo_df[self.geo_df['Area'] == area_code]

        if area_data.empty:
            return {}

        counties = area_data['CountyTownName'].unique().tolist()
        area_name = area_data.iloc[0]['AreaName']

        # Extract city name (remove state suffix from AreaName)
        # e.g., "Miami-Fort Lauderdale-West Palm Beach, FL" -> "Miami-Fort Lauderdale-West Palm Beach"
        city_name = area_name.split(',')[0].strip() if ',' in area_name else area_name

        return {
            'area_code': area_code,
            'area_name': area_name,
            'city_name': city_name,
            'state': area_data.iloc[0]['State'],
            'state_abbr': area_data.iloc[0]['StateAb'],
            'counties': counties,
            'num_counties': len(counties)
        }


def format_search_results(results_df: pd.DataFrame) -> List[Dict]:
    """
    Format search results for display

    Args:
        results_df: DataFrame from search

    Returns:
        List of formatted result dictionaries
    """
    if results_df.empty:
        return []

    formatted = []
    for _, row in results_df.iterrows():
        formatted.append({
            'area_code': row['Area'],
            'display_name': row['AreaName'],
            'state': row.get('State', ''),
            'county': row.get('CountyTownName', '')
        })

    return formatted


# Example usage
if __name__ == "__main__":
    # Load geography data
    DATA_DIR = Path("OFLC_Wages_2025-26_Updated")
    geo_df = pd.read_csv(DATA_DIR / "Geography.csv")

    # Initialize search engine
    search_engine = LocationSearchEngine(geo_df)

    # Test searches
    print("=" * 60)
    print("Location Search Examples")
    print("=" * 60)

    # Search by city
    print("\n1. Search by city: 'Austin'")
    results = search_engine.search_by_city("Austin", "TX")
    if not results.empty:
        print(f"   Found: {results.iloc[0]['AreaName']}")
        print(f"   Area Code: {results.iloc[0]['Area']}")

    # Search by county
    print("\n2. Search by county: 'Travis County'")
    results = search_engine.search_by_county("Travis County", "TX")
    if not results.empty:
        print(f"   Found in: {results.iloc[0]['AreaName']}")

    # Smart search
    print("\n3. Smart search: 'San Francisco, CA'")
    results = search_engine.smart_search("San Francisco, CA")
    if not results.empty:
        print(f"   Found: {results.iloc[0]['AreaName']}")

    # ZIP code search
    print("\n4. ZIP code search: '78701' (Austin, TX)")
    results = search_engine.search_by_zip("78701")
    if not results.empty:
        print(f"   Found: {results.iloc[0]['AreaName']}")

    # Fuzzy search
    print("\n5. Fuzzy search: 'San Fran'")
    results = search_engine.smart_search("San Fran")
    if not results.empty:
        print(f"   Found: {results.iloc[0]['AreaName']}")

    print("\n" + "=" * 60)
