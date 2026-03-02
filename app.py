"""
H1B Wage Analysis Dashboard
Interactive Streamlit dashboard for analyzing H1B prevailing wages
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
from location_search import LocationSearchEngine, format_search_results
from city_metro_mapper import CityMetroMapper

# Page configuration
st.set_page_config(
    page_title="H1B Wage Finder",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define data paths
DATA_DIR = Path("OFLC_Wages_2025-26_Updated")

# Occupation codes mapping
OCCUPATIONS = {
    '15-1252': 'Software Developers',
    '15-2051': 'Data Scientists',
    '15-2031': 'Operations Research Analysts',
    '15-1243': 'Database Architects',
    '15-1242': 'Database Administrators',
    '15-1244': 'Network/Systems Administrators',
    '15-1211': 'Computer Systems Analysts',
    '15-1212': 'Information Security Analysts',
    '17-2051': 'Civil Engineers',
}

WAGE_LEVELS = {
    'Level1': 'Level 1 (Entry)',
    'Level2': 'Level 2 (Qualified)',
    'Level3': 'Level 3 (Experienced)',
    'Level4': 'Level 4 (Fully Competent)',
}

# US Territories to exclude (when filtering for 50 states + DC only)
US_TERRITORIES = ['Puerto Rico', 'Virgin Islands', 'Guam', 'Northern Mariana Islands', 'American Samoa']


@st.cache_data
def load_data():
    """Load processed wage data"""
    try:
        processed_file = DATA_DIR / 'processed_wage_data.csv'
        top_cities_file = DATA_DIR / 'top_200_cities.csv'
        geo_file = DATA_DIR / 'Geography.csv'

        if not processed_file.exists():
            st.error("Processed data not found. Please run data_processor.py first.")
            return None, None, None

        df = pd.read_csv(processed_file)
        top_cities = pd.read_csv(top_cities_file)
        geo_df = pd.read_csv(geo_file)

        return df, top_cities, geo_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None


@st.cache_resource
def get_search_engine(geo_df):
    """Initialize location search engine (cached)"""
    return LocationSearchEngine(geo_df)


def display_overall_statistics(df, top_cities):
    """Display quick search"""
    st.header("🔍 Quick Search")

    # Occupation filter
    selected_occupation = st.selectbox(
        "Select Occupation",
        options=list(OCCUPATIONS.keys()),
        format_func=lambda x: OCCUPATIONS[x],
        index=0,
        key='overall_occupation'
    )

    # Filter data (default to 50 states only)
    occ_df = df[df['SocCode'] == selected_occupation].copy()
    occ_df = occ_df[~occ_df['State'].isin(US_TERRITORIES)]

    # Display top 20 cities with lowest Level 2 wages
    st.subheader(f"🏆 Top 20 Cities - Lowest Wages")

    # Calculate average Level 2 wage by city for this occupation
    city_avg_wages = occ_df.groupby(['Area', 'CityName', 'AreaName']).agg({
        'Level2_Annual': 'mean',
        'Level1_Annual': 'mean'
    }).reset_index()

    # Get top 20 cities with lowest Level 2 wages
    lowest_wage_cities = city_avg_wages.nsmallest(20, 'Level2_Annual')
    lowest_wage_cities['Avg Level 2 Salary'] = lowest_wage_cities['Level2_Annual'].apply(lambda x: f'${x:,.0f}/year')
    lowest_wage_cities['Avg Level 1 Salary'] = lowest_wage_cities['Level1_Annual'].apply(lambda x: f'${x:,.0f}/year')
    lowest_wage_cities.index = range(1, len(lowest_wage_cities) + 1)

    st.dataframe(
        lowest_wage_cities[['CityName', 'AreaName', 'Avg Level 1 Salary', 'Avg Level 2 Salary']],
        use_container_width=True,
        height=600
    )


def display_city_comparison(df, top_cities, search_engine):
    """Display city comparison section"""
    st.header("🔍 City Comparison Tool")

    st.markdown("""
    Compare H1B prevailing wages across different cities to identify the best locations
    for your H1B application. Lower wages at Level 1 and Level 2 can improve approval chances.
    """)

    # Initialize session state for selected cities if not exists
    if 'comparison_selected_cities' not in st.session_state:
        # Get all unique cities from entire dataset (not just top 200)
        all_city_options = sorted(df['CityName'].unique())
        st.session_state.comparison_selected_cities = list(all_city_options[:3]) if len(all_city_options) >= 3 else []

    # Smart Location Search
    with st.expander("🔎 Smart Location Search - Search by City, County, or ZIP Code", expanded=False):
        st.markdown("""
        **Don't know the exact city name?** Use our smart search!
        - Enter a **city name** (e.g., "Austin", "San Francisco", "Delray Beach")
        - Enter a **county name** (e.g., "Travis County", "Santa Clara", "Palm Beach County")
        - Enter a **ZIP code** (e.g., "78701", "94105", "33444")
        - Enter **city + state** (e.g., "Austin, TX", "San Francisco CA", "Boca Raton FL")

        Found cities will be **automatically added** to your selection below.
        """)

        col_search, col_button = st.columns([3, 1])

        with col_search:
            search_query = st.text_input(
                "Search Location",
                placeholder="Try: Delray Beach, Boca Raton, 33444, Palm Beach County...",
                key="location_search"
            )

        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            search_clicked = st.button("🔍 Search", type="primary")

        if search_clicked and search_query:
            with st.spinner("Searching locations..."):
                results = search_engine.smart_search(search_query, limit=5)

                if not results.empty:
                    st.success(f"✓ Found {len(results)} matching location(s)!")

                    # Auto-populate found cities
                    found_cities = []
                    for idx, row in results.iterrows():
                        area_details = search_engine.get_area_details(row['Area'])
                        if area_details:
                            # Get city name (with fallback to area_name if city_name not available)
                            city_name = area_details.get('city_name', area_details['area_name'].split(',')[0].strip())
                            found_cities.append(city_name)

                            st.info(f"""
                            **{area_details['area_name']}**
                            - State: {area_details['state']}
                            - Counties: {area_details['num_counties']} ({', '.join(area_details['counties'][:3])}{'...' if area_details['num_counties'] > 3 else ''})
                            - Area Code: `{area_details['area_code']}`
                            """)

                    # Add found cities to selection (avoid duplicates)
                    current_selection = st.session_state.comparison_selected_cities
                    for city in found_cities:
                        if city not in current_selection and len(current_selection) < 10:
                            current_selection.append(city)
                    st.session_state.comparison_selected_cities = current_selection

                    st.success(f"✓ Added {len(found_cities)} city/cities to your selection below!")
                else:
                    st.warning(f"No locations found for '{search_query}'. Try a different search term or check spelling.")

    st.divider()

    # Filters
    col1, col2 = st.columns([2, 1])

    with col1:
        # City selection - USE ALL CITIES, not just top 200
        all_city_options = sorted(df['CityName'].unique())

        st.markdown("**💡 Tip:** Start typing to search and filter cities (e.g., type 'Miami' or 'Delray')")

        selected_cities = st.multiselect(
            "Select Cities to Compare (select 2-10 cities)",
            options=all_city_options,
            default=st.session_state.comparison_selected_cities,
            max_selections=10,
            help="Start typing to search! All cities in the dataset are available. Or use Smart Location Search above to search by ZIP/county.",
            key="city_multiselect",
            placeholder="Start typing city name to search..."
        )

        # Update session state
        st.session_state.comparison_selected_cities = selected_cities

    with col2:
        # Occupation selection
        selected_occupation = st.selectbox(
            "Select Occupation",
            options=list(OCCUPATIONS.keys()),
            format_func=lambda x: OCCUPATIONS[x],
            index=0
        )

    if not selected_cities:
        st.warning("Please select at least one city to view comparison.")
        return

    # Filter data
    selected_areas = top_cities[top_cities['CityName'].isin(selected_cities)]['Area'].values
    filtered_df = df[
        (df['Area'].isin(selected_areas)) &
        (df['SocCode'] == selected_occupation)
    ]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # County-level analysis
    st.subheader(f"📍 County-Level Analysis: {OCCUPATIONS[selected_occupation]}")

    # Group by county
    county_wages = filtered_df.groupby([
        'Area', 'CityName', 'State', 'CountyTownName'
    ])[['Level1', 'Level2', 'Level3', 'Level4']].mean().reset_index()

    # Display lowest Level 1 and Level 2 wages
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🟢 Lowest Level 1 Wages (Best for Entry)")
        lowest_l1 = county_wages.nsmallest(15, 'Level1')
        lowest_l1_display = lowest_l1.copy()
        lowest_l1_display['Level1'] = lowest_l1_display['Level1'].apply(lambda x: f'${x:.2f}/hr')
        lowest_l1_display.index = range(1, len(lowest_l1_display) + 1)
        st.dataframe(
            lowest_l1_display[['CityName', 'CountyTownName', 'State', 'Level1']],
            use_container_width=True,
            height=400
        )

    with col2:
        st.markdown("#### 🟡 Lowest Level 2 Wages (Best for Qualified)")
        lowest_l2 = county_wages.nsmallest(15, 'Level2')
        lowest_l2_display = lowest_l2.copy()
        lowest_l2_display['Level2'] = lowest_l2_display['Level2'].apply(lambda x: f'${x:.2f}/hr')
        lowest_l2_display.index = range(1, len(lowest_l2_display) + 1)
        st.dataframe(
            lowest_l2_display[['CityName', 'CountyTownName', 'State', 'Level2']],
            use_container_width=True,
            height=400
        )

    # Visualization: Wage comparison by city
    st.subheader("📊 Wage Level Comparison Across Cities")

    city_avg_wages = filtered_df.groupby('CityName')[
        ['Level1', 'Level2', 'Level3', 'Level4']
    ].mean().reset_index()

    fig = go.Figure()
    for level, label in WAGE_LEVELS.items():
        fig.add_trace(go.Box(
            y=filtered_df[filtered_df['CityName'].isin(selected_cities)][level],
            x=filtered_df[filtered_df['CityName'].isin(selected_cities)]['CityName'],
            name=label,
            boxmean='sd'
        ))

    fig.update_layout(
        title=f'Wage Distribution by City - {OCCUPATIONS[selected_occupation]}',
        xaxis_title='City',
        yaxis_title='Hourly Wage ($)',
        boxmode='group',
        height=500,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed county table
    st.subheader("📋 Detailed County Wage Data")

    # Format wages for display
    display_df = county_wages.copy()
    for col in ['Level1', 'Level2', 'Level3', 'Level4']:
        display_df[col] = display_df[col].apply(lambda x: f'${x:.2f}')

    # Sort by Level 2 (most relevant for H1B)
    display_df_sorted = county_wages.sort_values('Level2').copy()
    for col in ['Level1', 'Level2', 'Level3', 'Level4']:
        display_df_sorted[col] = display_df_sorted[col].apply(lambda x: f'${x:.2f}')

    st.dataframe(
        display_df_sorted[['CityName', 'State', 'CountyTownName', 'Level1', 'Level2', 'Level3', 'Level4']],
        use_container_width=True,
        height=500
    )

    # Download option
    csv = county_wages.to_csv(index=False)
    st.download_button(
        label="📥 Download County Data as CSV",
        data=csv,
        file_name=f"h1b_wages_{selected_occupation}_{'-'.join(selected_cities[:3])}.csv",
        mime="text/csv"
    )


def display_occupation_insights(df, top_cities):
    """Display insights for specific occupations"""
    st.header("🎯 Occupation-Specific Insights")

    selected_occupation = st.selectbox(
        "Select Occupation for Detailed Analysis",
        options=list(OCCUPATIONS.keys()),
        format_func=lambda x: OCCUPATIONS[x],
        key='occupation_insights'
    )

    # Territory filter checkbox
    exclude_territories = st.checkbox(
        "🇺🇸 Show only 50 US States + DC (exclude territories)",
        value=True,
        help="When checked, excludes US territories like Puerto Rico, Guam, Virgin Islands",
        key='insights_exclude_territories'
    )

    occ_data = df[df['SocCode'] == selected_occupation].copy()

    # Apply territory filter if needed
    if exclude_territories:
        occ_data = occ_data[~occ_data['State'].isin(US_TERRITORIES)]

    if occ_data.empty:
        st.warning("No data available for this occupation.")
        return

    # Top cities with lowest Level 1 and Level 2 wages
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 10 Counties: Lowest Level 1 Wages")
        county_l1 = occ_data.groupby(['CityName', 'State', 'CountyTownName'])['Level1_Annual'].mean()
        county_l1 = county_l1.reset_index().nsmallest(10, 'Level1_Annual')
        county_l1['Annual Salary'] = county_l1['Level1_Annual'].apply(lambda x: f'${x:,.0f}/year')
        county_l1.index = range(1, len(county_l1) + 1)
        st.dataframe(county_l1[['CityName', 'State', 'CountyTownName', 'Annual Salary']], use_container_width=True)

    with col2:
        st.subheader("🏆 Top 10 Counties: Lowest Level 2 Wages")
        county_l2 = occ_data.groupby(['CityName', 'State', 'CountyTownName'])['Level2_Annual'].mean()
        county_l2 = county_l2.reset_index().nsmallest(10, 'Level2_Annual')
        county_l2['Annual Salary'] = county_l2['Level2_Annual'].apply(lambda x: f'${x:,.0f}/year')
        county_l2.index = range(1, len(county_l2) + 1)
        st.dataframe(county_l2[['CityName', 'State', 'CountyTownName', 'Annual Salary']], use_container_width=True)

    # Geographic distribution
    st.subheader("🗺️ Geographic Distribution of Wages")

    state_wages = occ_data.groupby('State')[['Level1_Annual', 'Level2_Annual']].mean().reset_index()
    state_wages = state_wages.sort_values('Level2_Annual')
    state_wages.columns = ['State', 'Level 1', 'Level 2']

    fig = px.bar(
        state_wages.head(20),
        x='State',
        y=['Level 1', 'Level 2'],
        title=f'Average Level 1 & Level 2 Annual Salaries by State - {OCCUPATIONS[selected_occupation]}',
        labels={'value': 'Annual Salary ($)', 'variable': 'Wage Level'},
        barmode='group',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


def display_location_role_lookup(df, search_engine):
    """Primary lookup flow: location + role, then wage levels and role comparisons."""
    st.header("📍 Location + Role Lookup")

    # Input controls
    col1, col2 = st.columns([2, 1])
    with col1:
        location_query = st.text_input(
            "Enter PIN code, city, county, or metro area",
            placeholder="e.g., 78701, Austin TX, Palm Beach County",
            key="lookup_location_query"
        )
    with col2:
        selected_occupation = st.selectbox(
            "Select Role",
            options=list(OCCUPATIONS.keys()),
            format_func=lambda x: OCCUPATIONS[x],
            key="lookup_occupation"
        )

    if 'lookup_matches' not in st.session_state:
        st.session_state.lookup_matches = []
    if 'lookup_selected_area' not in st.session_state:
        st.session_state.lookup_selected_area = None

    if st.button("Find wages", type="primary", key="lookup_find_wages"):
        if not location_query.strip():
            st.warning("Please enter a location first.")
        else:
            results = search_engine.smart_search(location_query, limit=8)
            if results.empty:
                st.session_state.lookup_matches = []
                st.session_state.lookup_selected_area = None
                st.warning(f"No locations found for '{location_query}'.")
            else:
                unique_results = results.drop_duplicates(subset=['Area'])[['Area', 'AreaName', 'State']].copy()
                st.session_state.lookup_matches = unique_results.to_dict('records')
                st.session_state.lookup_selected_area = st.session_state.lookup_matches[0]['Area']

    matches = st.session_state.lookup_matches
    if not matches:
        st.info("Search a location to see wage levels for your selected role.")
        return

    area_options = [item['Area'] for item in matches]
    area_labels = {
        item['Area']: f"{item['AreaName']} ({item['State']})" if pd.notna(item.get('State')) else item['AreaName']
        for item in matches
    }

    if st.session_state.lookup_selected_area not in area_options:
        st.session_state.lookup_selected_area = area_options[0]

    selected_area = st.selectbox(
        "Choose matched location",
        options=area_options,
        index=area_options.index(st.session_state.lookup_selected_area),
        format_func=lambda x: area_labels.get(x, x)
    )
    st.session_state.lookup_selected_area = selected_area

    selected_area_name = area_labels[selected_area]

    level_cols_hourly = ['Level1', 'Level2', 'Level3', 'Level4']
    level_cols_annual = ['Level1_Annual', 'Level2_Annual', 'Level3_Annual', 'Level4_Annual']
    level_pairs = list(zip(level_cols_hourly, level_cols_annual))

    # Selected role wage levels in chosen location
    role_df = df[
        (df['Area'] == selected_area) &
        (df['SocCode'] == selected_occupation)
    ].copy()

    if role_df.empty:
        st.warning("No wage records found for this role in the selected location.")
        return

    role_by_county = role_df.groupby(['CountyTownName', 'State'])[level_cols_hourly + level_cols_annual].mean().reset_index()
    role_avg = role_by_county[level_cols_hourly + level_cols_annual].mean()

    st.subheader(f"💼 {OCCUPATIONS[selected_occupation]} in {selected_area_name}")

    level_summary = []
    for idx, (hourly_col, annual_col) in enumerate(level_pairs, start=1):
        level_summary.append({
            'Wage Level': f'Level {idx}',
            'Hourly Wage': f"${role_avg[hourly_col]:.2f}/hr",
            'Annual Wage': f"${role_avg[annual_col]:,.0f}/year"
        })
    st.dataframe(pd.DataFrame(level_summary), use_container_width=True, hide_index=True)

    st.caption("Average shown across counties in the selected OFLC area.")
    with st.expander("County-level wages for this role", expanded=False):
        county_display = role_by_county.copy()
        for idx, (hourly_col, annual_col) in enumerate(level_pairs, start=1):
            county_display[f'Level {idx}'] = county_display.apply(
                lambda row: f"${row[hourly_col]:.2f}/hr | ${row[annual_col]:,.0f}/year",
                axis=1
            )
        county_display = county_display.sort_values('Level2_Annual')
        st.dataframe(
            county_display[['CountyTownName', 'State', 'Level 1', 'Level 2', 'Level 3', 'Level 4']],
            use_container_width=True,
            hide_index=True
        )
    st.divider()

    # Other roles in the same location
    st.subheader("🔁 Other Roles in This Location")
    area_roles = df[df['Area'] == selected_area].copy()
    other_roles = area_roles.groupby('SocCode')[level_cols_hourly + level_cols_annual].mean().reset_index()
    other_roles = other_roles[other_roles['SocCode'].isin(OCCUPATIONS.keys())].copy()
    other_roles['Role'] = other_roles['SocCode'].map(OCCUPATIONS)
    other_roles.loc[other_roles['SocCode'] == selected_occupation, 'Role'] = (
        other_roles.loc[other_roles['SocCode'] == selected_occupation, 'Role'] + " (Selected)"
    )

    for idx, (hourly_col, annual_col) in enumerate(level_pairs, start=1):
        other_roles[f'Level {idx}'] = other_roles.apply(
            lambda row: f"${row[hourly_col]:.2f}/hr | ${row[annual_col]:,.0f}/year",
            axis=1
        )

    other_roles = other_roles.sort_values('Level2_Annual')
    st.dataframe(
        other_roles[['Role', 'Level 1', 'Level 2', 'Level 3', 'Level 4']],
        use_container_width=True,
        hide_index=True,
        height=420
    )


def display_salary_comparison(df, search_engine):
    """Display salary-based city recommendations"""
    st.header("💰 Salary Recommendations")

    # Occupation selection
    selected_occupation = st.selectbox(
        "Select Occupation",
        options=list(OCCUPATIONS.keys()),
        format_func=lambda x: OCCUPATIONS[x],
        index=0,
        key='salary_occupation'
    )

    # Initialize session state for current city selection
    if 'salary_current_city' not in st.session_state:
        all_cities_list = sorted(df['CityName'].unique())
        st.session_state.salary_current_city = all_cities_list[0] if all_cities_list else None

    # Create city mapper for enhanced search
    @st.cache_resource
    def get_city_mapper(_df):
        return CityMetroMapper(_df)

    mapper = get_city_mapper(df)

    # Get enhanced city list with mappings
    all_searchable_cities = sorted(mapper.get_all_searchable_cities())
    metro_areas = sorted(df['CityName'].unique())

    # Combine: Individual cities first, then metros
    combined_options = []
    city_to_metro_map = {}

    # Add individual cities with " → Metro" indicator
    for city in all_searchable_cities:
        metros = mapper.get_metro_for_city(city)
        if metros and city not in metro_areas:  # Only if not already a metro name
            display_name = f"{city} → {metros[0]}"
            combined_options.append(display_name)
            city_to_metro_map[display_name] = metros[0]

    # Add metros as-is
    for metro in metro_areas:
        combined_options.append(metro)
        city_to_metro_map[metro] = metro

    combined_options = sorted(combined_options)

    # Main city selector
    col_select, col_or, col_search = st.columns([5, 1, 5])

    with col_select:
        # Find current selection in combined options
        current_display = st.session_state.salary_current_city
        if current_display not in combined_options:
            # Try to find it in the mapping
            for opt, metro in city_to_metro_map.items():
                if metro == current_display:
                    current_display = opt
                    break

        current_index = combined_options.index(current_display) if current_display in combined_options else 0

        selected_display = st.selectbox(
            "Select Metro Area (not city)",
            options=combined_options,
            index=current_index,
            help="Type your city (e.g., Boca Raton) or metro area name",
            key='current_city_salary_select'
        )

        # Get actual metro area from selection
        current_city = city_to_metro_map.get(selected_display, selected_display)

        # Update session state
        st.session_state.salary_current_city = current_city

    with col_or:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**OR**")

    with col_search:
        search_sub1, search_sub2 = st.columns([3, 1])

        with search_sub1:
            location_query = st.text_input(
                "ZIP or County",
                placeholder="e.g., 33445, Palm Beach County",
                key="salary_location_search",
                label_visibility="collapsed"
            )

        with search_sub2:
            loc_search_clicked = st.button("Find", key="salary_loc_search_btn", type="primary", use_container_width=True)

    # Search results (full width below)
    if loc_search_clicked and location_query:
        results = search_engine.smart_search(location_query, limit=5)
        if not results.empty:
            st.success(f"✓ Found {len(results)} location(s)! Click to select:")

            # Create selectable buttons for each result
            cols = st.columns(min(len(results), 3))
            for idx, row in results.iterrows():
                details = search_engine.get_area_details(row['Area'])
                if details:
                    city_name = details.get('city_name', details['area_name'].split(',')[0].strip())

                    with cols[idx % 3]:
                        if st.button(
                            f"📍 {city_name}",
                            key=f"select_city_{idx}",
                            help=f"Select {details['area_name']}",
                            use_container_width=True
                        ):
                            st.session_state.salary_current_city = city_name
                            st.rerun()
        else:
            st.warning(f"No results for '{location_query}'")

    # Show current selection
    st.info(f"**Currently selected:** {current_city}")

    st.divider()

    # Filter data by occupation
    occ_df = df[df['SocCode'] == selected_occupation].copy()

    if occ_df.empty:
        st.warning(f"No data available for {OCCUPATIONS[selected_occupation]}")
        return

    # Calculate average Level 2 wage by city (most common H1B level)
    city_wages = occ_df.groupby(['CityName', 'AreaName', 'State']).agg({
        'Level2_Annual': 'mean',
        'Level1_Annual': 'mean'
    }).reset_index()

    # Use all cities (not filtered by salary)
    better_cities = city_wages.copy()

    # Get current city's state for proximity calculation
    current_city_state = city_wages[city_wages['CityName'] == current_city]['State'].iloc[0] if len(city_wages[city_wages['CityName'] == current_city]) > 0 else None

    # Add proximity score (0 = same state, 1 = different state)
    if current_city_state:
        better_cities['Proximity_Score'] = better_cities['State'].apply(lambda x: 0 if x == current_city_state else 1)
    else:
        better_cities['Proximity_Score'] = 1

    # Sort by: 1) Same state first, 2) Lowest wage within each group
    better_cities = better_cities.sort_values(
        by=['Proximity_Score', 'Level2_Annual'],
        ascending=[True, True]
    )

    # Get top 20
    top_20_cities = better_cities.head(20).copy()

    # Display results
    st.subheader(f"🏆 Top 20 Cities - Lowest Wages")

    st.info(f"📍 Based on your location: **{current_city}** | Sorted by: **Same state first**, then **lowest wage**")

    col_metric1, col_metric2 = st.columns(2)

    with col_metric1:
        lowest_wage = top_20_cities.iloc[0]['Level2_Annual']
        best_city = top_20_cities.iloc[0]['CityName']
        st.metric(
            "Lowest Wage Found",
            f"${lowest_wage:,.0f}/year",
            help=f"Lowest prevailing wage in {best_city}"
        )

    with col_metric2:
        same_state_count = len(top_20_cities[top_20_cities['Proximity_Score'] == 0])
        st.metric(
            "Same State Options",
            f"{same_state_count} of 20",
            help=f"Cities in {current_city_state}"
        )

    st.divider()

    # Create display dataframe
    display_df = top_20_cities.copy()
    display_df['Rank'] = range(1, len(display_df) + 1)
    display_df['Prevailing Wage (Level 2)'] = display_df['Level2_Annual'].apply(lambda x: f'${x:,.0f}/year')
    display_df['Level 1 Wage'] = display_df['Level1_Annual'].apply(lambda x: f'${x:,.0f}/year')

    # Add proximity indicator
    if current_city_state:
        display_df['Location'] = display_df['State'].apply(
            lambda x: '🏠 Same State' if x == current_city_state else '✈️ Other State'
        )

    # Highlight current city if in list
    if current_city in display_df['CityName'].values:
        st.info(f"ℹ️ Your current city **{current_city}** is in the top 20 list!")

    # Determine columns to display
    columns_to_display = ['Rank', 'CityName', 'State']
    if current_city_state:
        columns_to_display.append('Location')
    columns_to_display.extend(['Level 1 Wage', 'Prevailing Wage (Level 2)'])

    st.dataframe(
        display_df[columns_to_display],
        use_container_width=True,
        height=600,
        hide_index=True
    )

    # Download option
    st.divider()

    download_df = top_20_cities[['CityName', 'AreaName', 'State', 'Level2_Annual', 'Level1_Annual']].copy()
    download_df.columns = ['City', 'Metro Area', 'State', 'Level 2 Annual Wage', 'Level 1 Annual Wage']

    csv = download_df.to_csv(index=False)
    st.download_button(
        label="Download Top 20 Cities as CSV",
        data=csv,
        file_name=f"h1b_cities_{selected_occupation}_{current_city}.csv",
        mime="text/csv"
    )


def display_wage_level_summary(df):
    """Display wage level summary with state/county filters and separate wage level tables"""
    st.header("📊 Wage Level Summary")

    # Apply territory filter (default to 50 states only)
    filtered_df_base = df[~df['State'].isin(US_TERRITORIES)].copy()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        # State filter
        state_options = ['All States'] + sorted(filtered_df_base['State'].unique().tolist())
        selected_state = st.selectbox(
            "Select State",
            options=state_options,
            index=0
        )

    with col2:
        # County filter (filtered by state if selected)
        if selected_state != 'All States':
            county_options = ['All Counties'] + sorted(
                filtered_df_base[filtered_df_base['State'] == selected_state]['CountyTownName'].unique().tolist()
            )
        else:
            county_options = ['All Counties'] + sorted(filtered_df_base['CountyTownName'].unique().tolist())

        selected_county = st.selectbox(
            "Select County",
            options=county_options,
            index=0
        )

    with col3:
        # Occupation selection
        selected_occupation = st.selectbox(
            "Select Occupation",
            options=list(OCCUPATIONS.keys()),
            format_func=lambda x: OCCUPATIONS[x],
            key='advanced_occupation'
        )

    # Filter data
    filtered_df = filtered_df_base[filtered_df_base['SocCode'] == selected_occupation].copy()

    if selected_state != 'All States':
        filtered_df = filtered_df[filtered_df['State'] == selected_state]

    if selected_county != 'All Counties':
        filtered_df = filtered_df[filtered_df['CountyTownName'] == selected_county]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # Group by county and calculate average wages
    county_wages = filtered_df.groupby([
        'State', 'CountyTownName', 'CityName'
    ]).agg({
        'Level1_Annual': 'mean',
        'Level2_Annual': 'mean',
        'Level3_Annual': 'mean',
        'Level4_Annual': 'mean'
    }).reset_index()

    # Summary stats
    st.subheader(f"📊 Results: {OCCUPATIONS[selected_occupation]}")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Counties Found", len(county_wages))
    with col2:
        if selected_state != 'All States':
            st.metric("State", selected_state)
        else:
            st.metric("States", county_wages['State'].nunique())
    with col3:
        if selected_county != 'All Counties':
            st.metric("County", selected_county)

    st.divider()

    # Separate tables for each wage level
    st.subheader("💰 Results by Wage Level")

    # Level 1 Table
    st.markdown("### 🟢 Level 1")
    level1_sorted = county_wages.sort_values('Level1_Annual').copy()
    level1_sorted['Level 1 Annual Salary'] = level1_sorted['Level1_Annual'].apply(lambda x: f'${x:,.0f}')
    level1_sorted.index = range(1, len(level1_sorted) + 1)

    st.dataframe(
        level1_sorted[['State', 'CountyTownName', 'CityName', 'Level 1 Annual Salary']],
        use_container_width=True,
        height=400
    )

    st.divider()

    # Level 2 Table
    st.markdown("### 🟡 Level 2")
    level2_sorted = county_wages.sort_values('Level2_Annual').copy()
    level2_sorted['Level 2 Annual Salary'] = level2_sorted['Level2_Annual'].apply(lambda x: f'${x:,.0f}')
    level2_sorted.index = range(1, len(level2_sorted) + 1)

    st.dataframe(
        level2_sorted[['State', 'CountyTownName', 'CityName', 'Level 2 Annual Salary']],
        use_container_width=True,
        height=400
    )

    st.divider()

    # Level 3 Table
    st.markdown("### 🟠 Level 3")
    level3_sorted = county_wages.sort_values('Level3_Annual').copy()
    level3_sorted['Level 3 Annual Salary'] = level3_sorted['Level3_Annual'].apply(lambda x: f'${x:,.0f}')
    level3_sorted.index = range(1, len(level3_sorted) + 1)

    st.dataframe(
        level3_sorted[['State', 'CountyTownName', 'CityName', 'Level 3 Annual Salary']],
        use_container_width=True,
        height=400
    )

    st.divider()

    # Level 4 Table
    st.markdown("### 🔴 Level 4")
    level4_sorted = county_wages.sort_values('Level4_Annual').copy()
    level4_sorted['Level 4 Annual Salary'] = level4_sorted['Level4_Annual'].apply(lambda x: f'${x:,.0f}')
    level4_sorted.index = range(1, len(level4_sorted) + 1)

    st.dataframe(
        level4_sorted[['State', 'CountyTownName', 'CityName', 'Level 4 Annual Salary']],
        use_container_width=True,
        height=400
    )

    # Download all data
    st.divider()
    st.subheader("📥 Download Data")

    # Prepare download data
    download_df = county_wages.copy()
    download_df.columns = ['State', 'County', 'City', 'Level 1 Annual', 'Level 2 Annual', 'Level 3 Annual', 'Level 4 Annual']
    csv = download_df.to_csv(index=False)

    st.download_button(
        label="Download All Wage Levels as CSV",
        data=csv,
        file_name=f"h1b_wages_{selected_occupation}_{selected_state.replace(' ', '_')}.csv",
        mime="text/csv"
    )


def main():
    """Main application"""

    # Title and description
    st.title("🇺🇸 H1B Wage Finder")
    st.caption("Enter a location and role to instantly see Level 1-4 hourly and annual wages.")

    # Load data
    with st.spinner("Loading wage data..."):
        df, top_cities, geo_df = load_data()

    if df is None or top_cities is None or geo_df is None:
        st.stop()

    # Initialize search engine
    search_engine = get_search_engine(geo_df)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Location + Role Lookup", "Salary Recommendations", "Wage Level Summary", "Quick Search"]
    )

    st.sidebar.divider()
    st.sidebar.caption("OFLC Wage Data 2025-2026")

    # Display selected page
    if page == "Location + Role Lookup":
        display_location_role_lookup(df, search_engine)
    elif page == "Salary Recommendations":
        display_salary_comparison(df, search_engine)
    elif page == "Wage Level Summary":
        display_wage_level_summary(df)
    elif page == "Quick Search":
        display_overall_statistics(df, top_cities)


if __name__ == "__main__":
    main()
