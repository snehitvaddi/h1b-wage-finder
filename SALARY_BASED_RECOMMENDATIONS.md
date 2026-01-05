# Salary-Based Recommendations Feature

## Overview

The **Salary-Based Recommendations** feature replaces the "City Comparison" view with a much more practical, personalized tool for **current US employees** seeking H1B sponsorship.

## Problem It Solves

### Before (City Comparison):
- Users had to manually select cities and compare them
- No personalization based on individual circumstances
- Didn't account for user's current salary
- Hard to identify which cities are realistic targets

### After (Salary-Based Recommendations):
- **Personalized recommendations** based on YOUR salary and location
- Automatically finds cities where YOUR salary is ABOVE the prevailing wage
- Ranks cities by lowest wage first (best H1B approval chances)
- Shows exactly how much advantage you have in each city

## How It Works

### User Inputs:

1. **Your Occupation** - Select from 8 supported tech/engineering roles
2. **Your Current Annual Salary** - Enter what you're currently making (e.g., $120,000)
3. **Your Current Location** - Select your city or search by ZIP/county

### Algorithm:

```
1. Filter dataset by selected occupation
2. Calculate average Level 2 wage for all cities
3. Find cities where Level 2 wage < Your current salary
4. Calculate "salary advantage" = Your salary - Prevailing wage
5. Sort by lowest prevailing wage (best H1B chances)
6. Return top 20 cities
```

### Output:

**Top 20 Cities** with:
- **Rank** - Lower rank = better opportunity
- **City Name & State**
- **Prevailing Wage (Level 2)** - The wage threshold for H1B
- **Your Advantage** - How much lower the wage is vs. your salary
- **Advantage %** - Percentage advantage

## Example Scenario

### Input:
- **Occupation**: Data Scientist
- **Current Salary**: $120,000/year
- **Current Location**: San Francisco, CA

### Sample Output:

| Rank | City | State | Prevailing Wage | Your Advantage | Advantage % |
|------|------|-------|-----------------|----------------|-------------|
| 1 | McAllen | TX | $68,640/year | $51,360 lower | 42.8% |
| 2 | Brownsville | TX | $72,280/year | $47,720 lower | 39.8% |
| 3 | El Paso | TX | $78,520/year | $41,480 lower | 34.6% |
| ... | ... | ... | ... | ... | ... |

### Interpretation:

If you move to **McAllen, TX** as a Data Scientist:
- Your $120K salary is **$51,360 ABOVE** the prevailing wage
- This gives you a **42.8% advantage** for H1B approval
- Your employer can easily justify the H1B sponsorship
- Very high approval probability

If you stay in **San Francisco, CA**:
- Prevailing wage might be $180K (hypothetical)
- Your $120K salary is BELOW the prevailing wage
- H1B sponsorship is much harder to justify
- Lower approval probability

## Key Features

### 1. Real-Time Filtering
- Only shows cities where you have an actual advantage
- Eliminates unrealistic options automatically

### 2. Smart Metrics
- **Cities Found**: Total cities where your salary > prevailing wage
- **Lowest Wage Found**: Best city with your highest advantage
- **Avg Potential Savings**: Average advantage across top 20

### 3. Location Search Integration
- Can search current location by:
  - City name (with autocomplete)
  - ZIP code (e.g., 33444)
  - County name (e.g., Palm Beach County)
- Uses the same fuzzy matching as other views

### 4. Current City Highlighting
- If your current city is in the top 20, shows info notification
- Helps you understand if you should stay or relocate

### 5. Download Capability
- Export top 20 cities as CSV
- Filename includes occupation and salary for easy reference
- Contains full metro area names and all wage levels

## Use Cases

### Use Case 1: OPT Worker Planning H1B
**Profile**:
- Currently on OPT in expensive city (NYC, SF, Seattle)
- Making $100K as Software Developer
- H1B lottery coming up

**Action**:
- Use tool to find cheaper cities with lower wages
- Apply to companies in those cities
- Better H1B approval chances when lottery is won

### Use Case 2: H1B Transfer Planning
**Profile**:
- Current H1B holder looking to switch jobs
- Making $130K in current city
- Wants to maximize chances of H1B transfer approval

**Action**:
- Find cities where $130K is well above prevailing wage
- Target companies in those locations
- Smooth H1B transfer process

### Use Case 3: Future Planning
**Profile**:
- International student graduating soon
- Trying to decide which city to target for first job
- Wants to optimize for eventual H1B approval

**Action**:
- Enter expected salary range for occupation
- See which cities offer best H1B prospects
- Make informed decision about where to start career

## Benefits Over City Comparison

| Feature | Old (City Comparison) | New (Salary-Based) |
|---------|----------------------|-------------------|
| Personalization | None | Based on YOUR salary |
| Ease of Use | Manual city selection | Automatic recommendations |
| Relevance | All cities | Only realistic options |
| Actionability | Low | High - clear targets |
| Understanding | Generic data | Personal advantage |
| Ranking | User decides | Auto-ranked by best chance |

## Technical Implementation

### Location: [app.py:460-680](app.py#L460-L680)

**Function**: `display_salary_comparison(df, search_engine)`

**Key Logic**:
```python
# Filter by occupation
occ_df = df[df['SocCode'] == selected_occupation]

# Calculate city averages
city_wages = occ_df.groupby(['CityName', 'AreaName', 'State']).agg({
    'Level2_Annual': 'mean',
    'Level1_Annual': 'mean'
})

# Find better cities
better_cities = city_wages[city_wages['Level2_Annual'] < current_salary]

# Calculate advantage
better_cities['Salary_Difference'] = current_salary - better_cities['Level2_Annual']
better_cities['Savings_Percent'] = (better_cities['Salary_Difference'] / current_salary * 100)

# Sort and get top 20
top_20_cities = better_cities.sort_values('Level2_Annual').head(20)
```

### Navigation Update

**Old Menu**:
- Overall Statistics
- **City Comparison** ← Removed
- Advanced Search
- Occupation Insights

**New Menu**:
- Overall Statistics
- **Salary-Based Recommendations** ← New
- Advanced Search
- Occupation Insights

## User Guidance Section

Built-in instructions explain:

1. **How to interpret results**
   - Lower wage = better H1B chances
   - Salary advantage meaning
   - Ranking significance

2. **Next steps**
   - Research companies in target cities
   - Apply for positions
   - Negotiate salary strategically
   - Understand H1B approval dynamics

## Future Enhancements (Optional)

Potential additions:
1. **Geographic proximity sorting** - Show closest cities first (requires lat/long data)
2. **Cost of living adjustment** - Factor in living costs
3. **Job market size** - Show number of companies in each city
4. **Multiple salary scenarios** - Compare different salary levels side-by-side
5. **Historical trends** - Show if wages are increasing/decreasing

## Summary

The Salary-Based Recommendations feature transforms the dashboard from a **general wage lookup tool** into a **personalized H1B strategy advisor**.

Instead of showing generic wage data, it provides **actionable, individualized recommendations** that help users make informed decisions about where to work to maximize their H1B approval chances.

This is especially valuable for:
- ✅ Current OPT workers planning H1B applications
- ✅ H1B holders considering job changes
- ✅ International students planning post-graduation careers
- ✅ Anyone trying to optimize their H1B sponsorship strategy

---

**The key insight**: Your H1B approval chances improve dramatically when your salary is ABOVE the prevailing wage. This tool finds exactly where that's true for YOU.
