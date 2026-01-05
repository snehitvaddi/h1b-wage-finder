# Smart Location Search - User Guide

## Overview

The H1B Wage Dashboard now includes a **Smart Location Search** feature that helps you find cities and counties even if you don't know the exact name or location details.

## How It Works

The search engine uses:
1. **Fuzzy Matching**: Finds close matches even with typos or partial names
2. **ZIP Code Lookup**: Converts ZIP codes to city/county names using free geocoding API
3. **Multi-format Input**: Accepts city names, county names, state abbreviations, and combinations

## Supported Search Formats

### 1. City Name Only
```
Austin
San Francisco
New York
Seattle
```

### 2. City + State
```
Austin, TX
San Francisco, CA
New York, NY
Austin Texas
San Francisco California
```

### 3. County Name
```
Travis County
Santa Clara County
Travis
Santa Clara
```

### 4. County + State
```
Travis County, TX
Santa Clara County, CA
Travis Texas
```

### 5. ZIP Code
```
78701
94105
10001
98101
```

### 6. Partial/Fuzzy Matches
```
San Fran        → San Francisco
Austim          → Austin (typo correction)
New Yrok        → New York
```

## Using the Search Feature

### In the Dashboard

1. Go to **City Comparison** view
2. Click on **"Smart Location Search"** expander
3. Enter your search query in the text box
4. Click the **"Search"** button
5. Review the results showing:
   - Full metro area name
   - State
   - Number of counties
   - County names
   - Area code

6. Manually select the city from the dropdown to add it to your comparison

## Search Examples

### Example 1: Search by City Name
**Input**: `Austin`

**Result**:
```
✓ Found 1 matching location(s)!

Austin, TX
- State: Texas
- Counties: 5 (Bastrop County, Caldwell County, Hays County...)
- Area Code: 12420
```

### Example 2: Search by ZIP Code
**Input**: `78701`

**Result**:
```
✓ Found 1 matching location(s)!

Austin, TX
- State: Texas
- Counties: 5 (Bastrop County, Caldwell County, Hays County...)
- Area Code: 12420
```

**How it works**: System looks up ZIP code 78701 → finds Austin, TX → matches to metro area

### Example 3: Search by County
**Input**: `Travis County`

**Result**:
```
✓ Found 1 matching location(s)!

Austin, TX
- State: Texas
- Counties: 5 (Travis County, Williamson County, Hays County...)
- Area Code: 12420
```

### Example 4: Multiple Matches
**Input**: `Springfield`

**Result**:
```
✓ Found 5 matching location(s)!

1. Springfield, MA
   - State: Massachusetts
   - Counties: 3 (Hampden County, Hampshire County...)

2. Springfield, IL
   - State: Illinois
   - Counties: 2 (Sangamon County, Menard County...)

3. Springfield, MO
   - State: Missouri
   - Counties: 4 (Greene County, Christian County...)
```

**Action**: Select the specific Springfield you want from the dropdown

### Example 5: Fuzzy Match with Typo
**Input**: `San Fransico`

**Result**:
```
✓ Found 1 matching location(s)!

San Francisco-Oakland-Berkeley, CA
- State: California
- Counties: 5 (Alameda County, Contra Costa County, Marin County...)
- Area Code: 41860
```

## Understanding Results

### Metro Area Names
Results show the full **Metropolitan Statistical Area (MSA)** name, which may include multiple cities:

```
San Francisco-Oakland-Berkeley, CA
New York-Newark-Jersey City, NY-NJ-PA
Dallas-Fort Worth-Arlington, TX
```

This is because wage data is organized by MSA, which can cover multiple cities and counties.

### Counties
Each metro area includes one or more counties. When you see:

```
Counties: 5 (Travis County, Williamson County, Hays County...)
```

It means:
- The metro area spans 5 counties total
- First 3 are shown in preview
- All counties are included in the wage data

### Area Codes
The area code (e.g., `12420`) is the **OFLC identifier** for that metro area. It's used internally to look up wage data.

## When to Use Location Search

### Scenario 1: Don't Know Exact City Name
**Problem**: "I live in Silicon Valley but don't know if it's San Jose or San Francisco"

**Solution**:
- Search by ZIP code: `95014`
- Or search: `Silicon Valley`
- Or search: `San Jose`

### Scenario 2: Know County, Not City
**Problem**: "I'm in Travis County but don't know the metro area"

**Solution**: Search `Travis County` or `Travis County, TX`

### Scenario 3: Multiple Cities with Same Name
**Problem**: "There are multiple Springfields!"

**Solution**:
- Search: `Springfield, IL` (with state)
- Or search by ZIP code
- Results will show all matches - pick the right one

### Scenario 4: Misspelled City
**Problem**: "I typed 'Phoneix' instead of 'Phoenix'"

**Solution**: The fuzzy matcher will still find Phoenix, AZ

### Scenario 5: Suburban Location
**Problem**: "I live in Sunnyvale but want to find the metro area"

**Solution**: Search `Sunnyvale` - it will match to San Jose-Sunnyvale-Santa Clara, CA

## Limitations

### ZIP Code Lookup
- Requires internet connection
- Uses free Zippopotam API
- May have 5-second timeout
- Only works for US ZIP codes

### Coverage
- Only searches within the **top 200 US metro areas**
- Non-metropolitan areas may not appear
- Very small towns might not be included

### Fuzzy Matching
- Requires >70% similarity score
- Very different spellings may not match
- Try multiple variations if needed

## Technical Details

### Matching Algorithm
1. **Exact Match**: Checks for exact city/county name match
2. **Fuzzy Match**: Uses Levenshtein distance algorithm
3. **Score Threshold**: Accepts matches with 70%+ similarity
4. **State Filtering**: Narrows results when state is provided

### ZIP Code Resolution
1. Calls free Zippopotam.us API
2. Extracts city and state from response
3. Searches city+state in database
4. Returns matching metro area(s)

### Search Index
Pre-built search index includes:
- All city names (cleaned)
- All county names
- All state names and abbreviations
- Combined search text for fuzzy matching

## Tips for Best Results

1. **Include State**: `Austin, TX` is better than just `Austin`
2. **Use ZIP Codes**: Most accurate for exact location
3. **Try Variations**: If one search fails, try county name or ZIP
4. **Check Results**: Verify the metro area matches your intended location
5. **Multiple Searches**: Search for 2-3 nearby cities to compare

## Future Enhancements

Planned improvements:
- Auto-add searched cities to comparison
- Show map of metro area
- Display recent searches
- Save favorite locations
- Batch ZIP code lookup (upload file)

## Troubleshooting

### "No locations found"
- Check spelling
- Try adding state abbreviation
- Use ZIP code instead
- Verify location is in top 200 metros

### "ZIP code lookup failed"
- Check internet connection
- Verify 5-digit ZIP code format
- Try searching by city name instead

### Wrong metro area returned
- Add state to narrow results
- Use full county name
- Try ZIP code for precision

## Examples by Use Case

### Tech Worker Moving to Austin
```
Searches:
- "78701" (downtown Austin ZIP)
- "Travis County"
- "Austin, TX"

All return: Austin, TX metro area with 5 counties
```

### Data Scientist in Bay Area
```
Searches:
- "94105" (San Francisco ZIP)
- "San Francisco"
- "Santa Clara County"

Returns multiple metros:
- San Francisco-Oakland-Berkeley
- San Jose-Sunnyvale-Santa Clara
```

### Civil Engineer in Texas
```
Searches:
- "Dallas"
- "Houston"
- "Austin"
- "San Antonio"

Compare all major Texas metros
```

## API Reference

### LocationSearchEngine Class

```python
# Initialize
search_engine = LocationSearchEngine(geography_df)

# Search by city
results = search_engine.search_by_city("Austin", state="TX", limit=10)

# Search by county
results = search_engine.search_by_county("Travis County", state="TX")

# Search by ZIP
results = search_engine.search_by_zip("78701")

# Smart search (auto-detects type)
results = search_engine.smart_search("Austin, TX")

# Get area details
details = search_engine.get_area_details("12420")
```

## Related Documentation

- [README.md](README.md) - General project documentation
- [QUICKSTART.md](QUICKSTART.md) - Installation and setup
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Dashboard usage guide

---

**Need Help?** The Smart Location Search makes finding your city easy - no need to know exact metro area names or county details!
