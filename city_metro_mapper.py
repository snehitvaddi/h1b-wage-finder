"""
City to Metro Area Mapper
Maps individual city names to their Metropolitan Statistical Areas
"""

import pandas as pd
import re
from typing import Dict, List


class CityMetroMapper:
    """Maps individual cities to their metro areas"""

    # Manual mappings for common cities not in metro names
    MANUAL_CITY_MAPPINGS = {
        # Florida
        'Boca Raton': 'Miami-Fort Lauderdale-West Palm Beach',
        'Delray Beach': 'Miami-Fort Lauderdale-West Palm Beach',
        'Boynton Beach': 'Miami-Fort Lauderdale-West Palm Beach',
        'Deerfield Beach': 'Miami-Fort Lauderdale-West Palm Beach',
        'Pompano Beach': 'Miami-Fort Lauderdale-West Palm Beach',
        'Coral Springs': 'Miami-Fort Lauderdale-West Palm Beach',
        'Pembroke Pines': 'Miami-Fort Lauderdale-West Palm Beach',
        'Miramar': 'Miami-Fort Lauderdale-West Palm Beach',
        'Hialeah': 'Miami-Fort Lauderdale-West Palm Beach',
        'Kendall': 'Miami-Fort Lauderdale-West Palm Beach',
        'Homestead': 'Miami-Fort Lauderdale-West Palm Beach',

        # New York
        'Brooklyn': 'New York-Newark-Jersey City',
        'Queens': 'New York-Newark-Jersey City',
        'Bronx': 'New York-Newark-Jersey City',
        'Manhattan': 'New York-Newark-Jersey City',
        'Staten Island': 'New York-Newark-Jersey City',

        # California - Bay Area
        'Palo Alto': 'San Jose-Sunnyvale-Santa Clara',
        'Mountain View': 'San Jose-Sunnyvale-Santa Clara',
        'Cupertino': 'San Jose-Sunnyvale-Santa Clara',
        'Milpitas': 'San Jose-Sunnyvale-Santa Clara',
        'Campbell': 'San Jose-Sunnyvale-Santa Clara',
        'Los Gatos': 'San Jose-Sunnyvale-Santa Clara',
        'Saratoga': 'San Jose-Sunnyvale-Santa Clara',

        'San Francisco': 'San Francisco-Oakland-Hayward',
        'Oakland': 'San Francisco-Oakland-Hayward',
        'Berkeley': 'San Francisco-Oakland-Hayward',
        'Hayward': 'San Francisco-Oakland-Hayward',
        'Fremont': 'San Francisco-Oakland-Hayward',
        'San Mateo': 'San Francisco-Oakland-Hayward',
        'Redwood City': 'San Francisco-Oakland-Hayward',

        # Texas
        'Plano': 'Dallas-Fort Worth-Arlington',
        'Irving': 'Dallas-Fort Worth-Arlington',
        'Frisco': 'Dallas-Fort Worth-Arlington',
        'McKinney': 'Dallas-Fort Worth-Arlington',
        'Richardson': 'Dallas-Fort Worth-Arlington',

        'Sugar Land': 'Houston-The Woodlands-Sugar Land',
        'Pearland': 'Houston-The Woodlands-Sugar Land',
        'The Woodlands': 'Houston-The Woodlands-Sugar Land',

        'Round Rock': 'Austin-Round Rock',
        'Cedar Park': 'Austin-Round Rock',
        'Georgetown': 'Austin-Round Rock',

        # Washington
        'Bellevue': 'Seattle-Tacoma-Bellevue',
        'Redmond': 'Seattle-Tacoma-Bellevue',
        'Kirkland': 'Seattle-Tacoma-Bellevue',
        'Renton': 'Seattle-Tacoma-Bellevue',
        'Kent': 'Seattle-Tacoma-Bellevue',

        # Illinois
        'Naperville': 'Chicago-Naperville-Elgin',
        'Aurora': 'Chicago-Naperville-Elgin',
        'Joliet': 'Chicago-Naperville-Elgin',
        'Evanston': 'Chicago-Naperville-Elgin',
    }

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with processed wage dataframe

        Args:
            df: DataFrame with CityName column (metro area names)
        """
        self.df = df
        self.city_to_metro = {}
        self.metro_to_cities = {}
        self._build_mappings()

    def _build_mappings(self):
        """Build bidirectional mappings between cities and metros"""
        unique_metros = self.df['CityName'].unique()

        # First, add manual mappings
        for city, metro in self.MANUAL_CITY_MAPPINGS.items():
            if city not in self.city_to_metro:
                self.city_to_metro[city] = []
            if metro in unique_metros and metro not in self.city_to_metro[city]:
                self.city_to_metro[city].append(metro)

        # Then, extract cities from metro names
        for metro in unique_metros:
            # Extract individual city names from metro area name
            cities = self._extract_cities(metro)

            # Map each city to this metro
            for city in cities:
                # Store mapping (handle duplicates by keeping all metros)
                if city not in self.city_to_metro:
                    self.city_to_metro[city] = []
                if metro not in self.city_to_metro[city]:
                    self.city_to_metro[city].append(metro)

            # Store reverse mapping
            self.metro_to_cities[metro] = cities

    def _extract_cities(self, metro_name: str) -> List[str]:
        """
        Extract individual city names from metro area name

        Examples:
            "Miami-Fort Lauderdale-West Palm Beach" → ["Miami", "Fort Lauderdale", "West Palm Beach"]
            "New York-Newark-Jersey City" → ["New York", "Newark", "Jersey City"]
            "San Jose-Sunnyvale-Santa Clara" → ["San Jose", "Sunnyvale", "Santa Clara"]
        """
        # Remove state suffix if present (e.g., ", FL" or ", NY-NJ-PA")
        metro_clean = re.sub(r',\s*[A-Z]{2}(-[A-Z]{2})*$', '', metro_name)

        # Split by hyphens to get individual cities
        # But be careful with city names that contain hyphens (e.g., "Winston-Salem")

        # Common patterns for multi-city metros:
        # "City1-City2-City3" → split on '-'
        # But keep "Winston-Salem" as one city

        # Simple approach: Split on ' - ' or '-' with surrounding context
        cities = []
        parts = metro_clean.split('-')

        current_city = []
        for i, part in enumerate(parts):
            part = part.strip()

            # If part starts with lowercase or is very short, it's likely continuation
            # e.g., "Fort Lauderdale" → ["Fort", "Lauderdale"]
            if current_city and (part[0].islower() if part else False or len(part) < 3):
                current_city.append(part)
            else:
                # Save previous city if exists
                if current_city:
                    cities.append(' '.join(current_city))
                # Start new city
                current_city = [part]

        # Don't forget the last city
        if current_city:
            cities.append(' '.join(current_city))

        # Also add the full metro name as a searchable option
        cities.append(metro_clean)

        return cities

    def get_metro_for_city(self, city_name: str) -> List[str]:
        """
        Get metro area(s) for a given city name

        Args:
            city_name: Individual city name (e.g., "Boca Raton", "San Jose")

        Returns:
            List of metro area names (may be multiple if ambiguous)
        """
        # Try exact match first
        if city_name in self.city_to_metro:
            return self.city_to_metro[city_name]

        # Try case-insensitive match
        city_lower = city_name.lower()
        for city, metros in self.city_to_metro.items():
            if city.lower() == city_lower:
                return metros

        # Try partial match
        matches = []
        for city, metros in self.city_to_metro.items():
            if city_lower in city.lower() or city.lower() in city_lower:
                matches.extend(metros)

        return list(set(matches))  # Remove duplicates

    def get_all_searchable_cities(self) -> List[str]:
        """Get all searchable city names (including both individual cities and metro areas)"""
        return sorted(set(self.city_to_metro.keys()))

    def get_city_metro_pairs(self) -> Dict[str, str]:
        """
        Get a flat mapping of city → metro for display
        Returns first metro if multiple matches
        """
        return {city: metros[0] for city, metros in self.city_to_metro.items()}


def create_enhanced_city_list(df: pd.DataFrame) -> tuple:
    """
    Create enhanced city list with individual cities mapped to metros

    Returns:
        Tuple of (city_options, city_to_metro_mapping)
        - city_options: List of all searchable names (cities + metros)
        - city_to_metro_mapping: Dict mapping display name → actual metro name
    """
    mapper = CityMetroMapper(df)

    # Get all metro areas
    metros = list(df['CityName'].unique())

    # Get all individual cities
    individual_cities = mapper.get_all_searchable_cities()

    # Create display options and mapping
    city_options = []
    city_to_metro = {}

    # Add metros first (exact matches)
    for metro in sorted(metros):
        city_options.append(metro)
        city_to_metro[metro] = metro

    # Add individual cities (mapped to metros)
    for city in individual_cities:
        if city not in metros:  # Don't duplicate
            metros_for_city = mapper.get_metro_for_city(city)
            if metros_for_city:
                # Add with indicator
                display_name = f"{city} → {metros_for_city[0]}"
                city_options.append(display_name)
                city_to_metro[display_name] = metros_for_city[0]

    return sorted(city_options), city_to_metro


if __name__ == "__main__":
    # Test the mapper
    import pandas as pd

    df = pd.read_csv('OFLC_Wages_2025-26_Updated/processed_wage_data.csv')
    mapper = CityMetroMapper(df)

    # Test cases
    test_cities = [
        "Miami",
        "Fort Lauderdale",
        "Boca Raton",
        "San Jose",
        "Brooklyn",
        "New York"
    ]

    print("Testing city-to-metro mappings:\n")
    for city in test_cities:
        metros = mapper.get_metro_for_city(city)
        print(f"{city:20} → {metros}")

    print(f"\n\nTotal searchable cities: {len(mapper.get_all_searchable_cities())}")
