# Theme Discovery Guide 🔍

## Overview

This guide explains how to use the theme discovery system to explore all available Onemap themes and integrate them into the property analyzer.

---

## Quick Start

### 1. Run Discovery

```bash
python discover_themes.py
```

This will:
- Authenticate with Onemap API
- Fetch all 100+ themes
- Test each theme at a sample location
- Save results to `discovered_themes.json`

### 2. View Results

```bash
# View all working themes
cat discovered_themes.json | jq '.themes[] | select(.status=="working") | {name: .theme_name, category: .category}'

# Count by category
cat discovered_themes.json | jq '.themes | group_by(.category) | map({category: .[0].category, count: length})'

# See sample data for a theme
cat discovered_themes.json | jq '.themes[] | select(.query_name=="dengue_cluster")'
```

---

## Understanding the Results

### Result Structure

```json
{
  "discovery_date": "2026-02-11T07:24:00.000Z",
  "total_themes": 120,
  "test_location": {
    "lat": 1.3521,
    "lon": 103.8198,
    "name": "Bishan"
  },
  "themes": [...]
}
```

### Theme Entry

```json
{
  "theme_name": "Kindergartens",
  "query_name": "kindergartens",
  "category": "Education",
  "owner": "EARLY CHILDHOOD DEVELOPMENT AGENCY",
  "icon": "school.gif",
  "expiry_date": "31/12/2026",
  "published_date": "01/01/2012",
  "status": "working",  // or "no_data" or "error"
  "data": {...},        // Sample data
  "sample_fields": ["NAME", "ADDRESS", ...],
  "feature_count": 10
}
```

---

## Analyzing Discovery Results

### 1. Categorize Themes

Group themes by what they measure:

**Safety & Security**:
- dengue_cluster
- crime_hotspots (if available)
- fire_stations
- police_stations

**Education**:
- kindergartens
- childcare
- primary_schools
- secondary_schools
- junior_colleges

**Healthcare**:
- hospitals
- clinics
- polyclinics
- eldercare

**Transport**:
- mrt_stations
- lrt_stations
- bus_stops
- taxi_stands

**Community & Lifestyle**:
- community_clubs
- libraries
- parks
- sports_facilities
- hawker_centres

**Environment**:
- park_connectors
- nature_reserves
- cycling_paths
- green_spaces

### 2. Identify Useful Fields

For each working theme, check `sample_fields`:

```bash
# See what data kindergartens provide
jq '.themes[] | select(.query_name=="kindergartens") | .sample_fields' discovered_themes.json
```

Common useful fields:
- `NAME` - Facility name
- `ADDRESS` / `POSTAL_CODE` - Location
- `LATITUDE` / `LONGITUDE` - Coordinates
- `DESCRIPTION` - Details
- `HYPERLINK` - More info
- Custom fields (e.g., `CASE_SIZE` for dengue)

---

## Integrating Discovered Themes

### Step 1: Update Theme Categories

Based on discovery results, update the curated theme list in `house_analyzer.py`:

```python
CURATED_THEMES = {
    'Education': [
        'kindergartens',
        'childcare',
        'primary_schools',  # If discovered
        'secondary_schools',  # If discovered
    ],
    'Health': [
        'hospitals',
        'clinics',
        'eldercare',
        'dengue_cluster',  # Safety factor
    ],
    'Community': [
        'community_clubs',
        'libraries',
        'hawker_centres',
    ],
    # Add newly discovered categories
    'Safety': [
        'dengue_cluster',
        'fire_stations',  # If discovered
    ],
}
```

### Step 2: Handle New Data Structures

For each new theme, handle its specific fields:

```python
def parse_dengue_data(results):
    """Parse dengue cluster data"""
    for item in results:
        cluster = {
            'name': item.get('NAME', ''),
            'description': item.get('DESCRIPTION', ''),
            'case_size': item.get('CASE_SIZE', 0),
            'link': item.get('HYPERLINK', ''),
            # Add coordinates if available
            'latitude': item.get('LATITUDE'),
            'longitude': item.get('LONGITUDE'),
        }
        # Calculate distance if coordinates available
        if cluster['latitude'] and cluster['longitude']:
            cluster['distance'] = calculate_distance(...)
        yield cluster
```

### Step 3: Update Scoring System

Add new factors to PropertyInsights:

```python
def _calculate_safety_score(self, results):
    """Calculate safety score including dengue"""
    score = 10  # Start with perfect score
    
    # Dengue clusters (negative factor)
    dengue_data = results.get('dengue_clusters', [])
    for cluster in dengue_data:
        distance = cluster.get('distance_km', float('inf'))
        if distance < 0.5:  # Within 500m
            score -= 3  # Major concern
        elif distance < 1.0:  # Within 1km
            score -= 2  # Moderate concern
    
    return max(0, score)
```

### Step 4: Add Smart Insights

Generate insights from new data:

```python
def generate_dengue_insights(self, results):
    """Generate dengue-related insights"""
    dengue_data = results.get('dengue_clusters', [])
    
    if dengue_data:
        closest = min(dengue_data, key=lambda x: x.get('distance_km', float('inf')))
        if closest.get('distance_km', float('inf')) < 1.0:
            return {
                'type': 'warning',
                'icon': '⚠️',
                'message': f"Dengue cluster within {closest['distance_km']:.1f}km",
                'details': closest.get('description', ''),
                'link': closest.get('link', '')
            }
    return None
```

---

## Examples of Useful Discoveries

### Example 1: Dengue Clusters

```json
{
  "theme_name": "Dengue Clusters",
  "query_name": "dengue_cluster",
  "category": "Health",
  "sample_fields": [
    "NAME",
    "DESCRIPTION",
    "CASE_SIZE",
    "HOMES",
    "PUBLIC_PLACES",
    "HYPERLINK"
  ]
}
```

**Use in analyzer**:
- Safety scoring (negative factor)
- Health risk assessment
- Smart insight warnings
- Link to official NEA data

### Example 2: Park Connectors

```json
{
  "theme_name": "Park Connectors",
  "query_name": "park_connectors",
  "category": "Environment",
  "sample_fields": [
    "NAME",
    "LENGTH",
    "DESCRIPTION"
  ]
}
```

**Use in analyzer**:
- Recreation scoring (positive factor)
- Lifestyle assessment
- Cycling/walking opportunities
- Green space connectivity

### Example 3: Construction Sites

```json
{
  "theme_name": "Construction Sites",
  "query_name": "construction",
  "category": "Development",
  "sample_fields": [
    "PROJECT_NAME",
    "STATUS",
    "COMPLETION_DATE"
  ]
}
```

**Use in analyzer**:
- Future development insights
- Potential noise/dust concerns
- Property value trends
- Neighborhood changes

---

## Best Practices

### 1. Test Location Selection

Choose diverse test locations to discover more themes:

```python
test_locations = [
    {'name': 'Bishan', 'lat': 1.3521, 'lon': 103.8198},      # Residential
    {'name': 'CBD', 'lat': 1.2844, 'lon': 103.8607},         # Commercial
    {'name': 'Punggol', 'lat': 1.4041, 'lon': 103.9025},     # New town
    {'name': 'Sentosa', 'lat': 1.2494, 'lon': 103.8303},     # Tourist
]
```

### 2. Handle Missing Data

Not all themes return data at all locations:

```python
theme_data = api.get_theme_data(query_name, lat, lon, extents)
if theme_data and len(theme_data) > 0:
    # Process data
    pass
else:
    # Theme exists but no data at this location
    pass
```

### 3. Rate Limiting

Respect API limits:

```python
import time

for theme in themes:
    data = api.get_theme_data(...)
    time.sleep(0.1)  # 100ms delay between requests
```

### 4. Error Handling

Some themes may fail:

```python
try:
    data = api.get_theme_data(query_name, lat, lon, extents)
except Exception as e:
    print(f"Theme {query_name} failed: {e}")
    continue  # Skip to next theme
```

---

## Integration Workflow

### 1. Discover

```bash
python discover_themes.py
```

### 2. Analyze

```bash
# Find high-value themes
jq '.themes[] | select(.status=="working") | select(.category | test("Health|Safety|Education"))' discovered_themes.json
```

### 3. Test

```bash
# Test integration with one theme
python -c "
from house_analyzer import OneMapAPI
api = OneMapAPI()
data = api.get_theme_data('dengue_cluster', 1.3521, 103.8198)
print(f'Found {len(data)} dengue clusters')
"
```

### 4. Integrate

Update `house_analyzer.py` with new themes.

### 5. Verify

```bash
python house_analyzer.py 1.3521 103.8198 --all-themes
```

---

## Troubleshooting

### No themes found

**Problem**: `discovered_themes.json` shows all themes with `status: "error"`

**Solution**:
- Check authentication (email/password or token)
- Verify network connectivity
- Check API rate limits

### Some themes return no data

**Problem**: Theme status is `"no_data"`

**Solution**:
- Normal! Not all themes have data at all locations
- Try different test locations
- Theme may be location-specific (e.g., industrial zones)

### Discovery takes too long

**Problem**: Script runs for >5 minutes

**Solution**:
- Increase delay between requests: `time.sleep(0.2)`
- Test subset first: `themes[:10]`
- Run during off-peak hours

---

## Advanced Usage

### Discover by Category

```python
# In discover_themes.py
target_categories = ['Education', 'Health', 'Safety']
filtered_themes = [t for t in themes if t.get('CATEGORY') in target_categories]
```

### Multiple Test Locations

```python
test_locations = [...]
for location in test_locations:
    extents = api.calculate_extents(location['lat'], location['lon'])
    # Test each theme at this location
```

### Compare Theme Availability

```python
# See which areas have more amenities
location_scores = {}
for location in test_locations:
    working_count = sum(1 for theme in themes if theme_works_at(location))
    location_scores[location['name']] = working_count
```

---

## Next Steps

1. **Run Discovery**: `python discover_themes.py`
2. **Review Results**: Check `discovered_themes.json`
3. **Identify Valuable Themes**: Focus on safety, health, education
4. **Update Analyzer**: Integrate new themes
5. **Test**: Verify with real locations
6. **Document**: Update theme descriptions
7. **Deploy**: Use in production analysis

---

## Useful Commands

```bash
# Count working themes by category
jq '.themes | group_by(.category) | map({category: .[0].category, working: map(select(.status=="working")) | length})' discovered_themes.json

# List all education themes
jq '.themes[] | select(.category=="Education") | {name: .theme_name, status: .status}' discovered_themes.json

# Find themes with most data
jq '.themes | sort_by(.feature_count) | reverse | .[0:10] | .[] | {name: .theme_name, count: .feature_count}' discovered_themes.json

# Export working themes to CSV
jq -r '.themes[] | select(.status=="working") | [.theme_name, .query_name, .category, .feature_count] | @csv' discovered_themes.json > working_themes.csv
```

---

**Ready to discover all available Onemap themes!** 🚀

Run `python discover_themes.py` and explore the full potential of Singapore's open data!
