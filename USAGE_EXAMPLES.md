# Usage Examples

This document provides practical examples of using the HDB House Analyzer.

## Basic Usage

### 1. Standard Mode (11 Curated Categories)

Fast analysis with commonly needed amenities:

```bash
python house_analyzer.py 1.3521 103.8198
```

This will analyze:
- Kindergartens
- Childcare centers
- Parks
- Libraries
- Community clubs
- Eldercare centers
- MRT stations
- Bus stops
- Major roads

**Time**: ~5-10 seconds

### 2. Comprehensive Mode (100+ Theme Categories)

Access all available Onemap themes:

```bash
python house_analyzer.py 1.3521 103.8198 --all-themes
```

This includes everything from standard mode PLUS:
- Dengue clusters
- CET centres
- Sports facilities
- Healthcare facilities
- Educational institutions
- Environmental data
- And 90+ more categories!

**Time**: ~30-60 seconds (many API calls)

### 3. Custom Search Radius

Adjust the search area (default is 5km):

```bash
# Search within 10km radius
python house_analyzer.py 1.3521 103.8198 --radius 10

# Search within 2km radius (faster, fewer results)
python house_analyzer.py 1.3521 103.8198 --radius 2
```

### 4. Limit Results Per Category

Control how many results to show per amenity type:

```bash
# Show top 20 results per category (default is 10)
python house_analyzer.py 1.3521 103.8198 --max-results 20

# Show only top 5 per category (faster)
python house_analyzer.py 1.3521 103.8198 --max-results 5
```

### 5. Combined Options

You can combine multiple options:

```bash
# Comprehensive analysis, 10km radius, top 15 results each
python house_analyzer.py 1.3521 103.8198 --all-themes --radius 10 --max-results 15
```

## Interactive Mode

If you don't provide coordinates as arguments, the script will prompt you:

```bash
python house_analyzer.py
```

Output:
```
================================================================================
HDB HOUSE ANALYZER - Using Onemap API
================================================================================

🔐 Onemap API Authentication Required
--------------------------------------------------------------------------------
The Onemap API requires authentication to access data.
If you don't have an account, register for FREE at:
https://www.onemap.gov.sg/apidocs/register
--------------------------------------------------------------------------------

Enter your Onemap email: your.email@example.com

💡 Note: Your password will be hidden as you type (no characters will appear).
   This is normal for security. Just type your password and press Enter.

Enter your Onemap password: 

✓ Credentials received. Authenticating...

Please enter the house coordinates:
Latitude: 1.3521
Longitude: 103.8198
```

## Sample Coordinates to Try

### Popular HDB Estates

```bash
# Bishan
python house_analyzer.py 1.3521 103.8198

# Tampines
python house_analyzer.py 1.3496 103.9568

# Jurong East
python house_analyzer.py 1.3329 103.7436

# Ang Mo Kio
python house_analyzer.py 1.3691 103.8454

# Punggol
python house_analyzer.py 1.4041 103.9025
```

### City Areas

```bash
# Marina Bay
python house_analyzer.py 1.2844 103.8607

# Orchard
python house_analyzer.py 1.3048 103.8318

# Bugis
python house_analyzer.py 1.2992 103.8554
```

### Nature/Suburban

```bash
# Near Bukit Timah Nature Reserve
python house_analyzer.py 1.3521 103.7760

# Near Sengkang
python house_analyzer.py 1.3916 103.8951
```

## Authentication Methods

### Method 1: Interactive Prompts (Recommended)

Just run the script and it will prompt you:

```bash
python house_analyzer.py 1.3521 103.8198
# Script will ask for email and password
```

### Method 2: Environment Variables

Set credentials before running:

**Linux/Mac:**
```bash
export ONEMAP_EMAIL='your.email@example.com'
export ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3521 103.8198
```

**Windows (Command Prompt):**
```cmd
set ONEMAP_EMAIL=your.email@example.com
set ONEMAP_PASSWORD=your_password
python house_analyzer.py 1.3521 103.8198
```

**Windows (PowerShell):**
```powershell
$env:ONEMAP_EMAIL='your.email@example.com'
$env:ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3521 103.8198
```

### Method 3: .env File

Create a `.env` file in the project directory:

```bash
ONEMAP_EMAIL=your.email@example.com
ONEMAP_PASSWORD=your_password
```

Then run the script normally:

```bash
python house_analyzer.py 1.3521 103.8198
```

**Note**: The `.env` file is automatically ignored by git for security.

## Exporting Results

### Save to JSON

The script will prompt you at the end:

```
Do you want to save the report as JSON? (y/n): y
Enter filename (default: house_analysis_1.3521_103.8198.json): my_analysis.json

✅ Report saved to my_analysis.json
```

Or just press Enter to use the default filename.

### Programmatic Usage

You can also use the analyzer in your Python code:

```python
from house_analyzer import HouseAnalyzer, OneMapAPI

# Initialize with credentials
api = OneMapAPI(email='your@email.com', password='your_password')
analyzer = HouseAnalyzer(api)

# Analyze a location
results = analyzer.analyze_house(
    lat=1.3521,
    lon=103.8198,
    use_all_themes=False,  # or True for comprehensive
    search_radius_km=5.0,
    max_results_per_category=10
)

# Save to JSON
import json
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Or process the data
print(f"Found {results['summary']['total_amenities']} amenities")
for category, items in results['amenities'].items():
    print(f"{category}: {len(items)} found")
```

## Understanding the Output

### Summary Section

```
📊 SUMMARY
--------------------------------------------------------------------------------
Total Amenities Found: 60
Nearest Amenity: Ang Mo Kio CC (Community Clubs) - 2.840 km
Nearest MRT: UPPER THOMSON MRT STATION (TE8) - 1.479 km
```

This gives you a quick overview of what was found.

### Amenities Breakdown

```
Kindergartens (10 found):
  1. PCF Sparkletots Preschool @ Cheng San-Seletar Blk 435 (KN)
     Address: 560435
     Distance: 4.201 km (4201 m)
```

Each amenity shows:
- Name
- Address or postal code
- Distance in both kilometers and meters

### Distance Calculation

Distances are calculated using the Haversine formula, which accounts for the Earth's curvature. This gives accurate "as the crow flies" distances.

## Tips

### 1. Start with Standard Mode

For most users, the standard mode (11 categories) is sufficient:

```bash
python house_analyzer.py 1.3521 103.8198
```

### 2. Use Comprehensive Mode for Detailed Analysis

If you need exhaustive information (e.g., for research or decision-making):

```bash
python house_analyzer.py 1.3521 103.8198 --all-themes
```

### 3. Adjust Radius Based on Location

- **City areas**: Use smaller radius (2-3km)
- **Suburban areas**: Use medium radius (5km, default)
- **Rural areas**: Use larger radius (7-10km)

### 4. Export to JSON for Further Analysis

Save results to JSON and analyze with Excel, Python pandas, or other tools:

```python
import json
import pandas as pd

# Load JSON
with open('house_analysis.json', 'r') as f:
    data = json.load(f)

# Convert amenities to DataFrame
all_amenities = []
for category, items in data['amenities'].items():
    for item in items:
        item['category'] = category
        all_amenities.append(item)

df = pd.DataFrame(all_amenities)
print(df.head())

# Find nearest kindergarten
kindergartens = df[df['category'] == 'kindergartens']
nearest = kindergartens.loc[kindergartens['distance'].idxmin()]
print(f"Nearest kindergarten: {nearest['name']} at {nearest['distance']:.2f} km")
```

## Troubleshooting

### Issue: 401 Unauthorized

**Problem**: Invalid or expired credentials

**Solution**: 
1. Verify your email and password are correct
2. Register at https://www.onemap.gov.sg/apidocs/register if you don't have an account
3. Re-run the script and enter credentials when prompted

### Issue: 404 Not Found for Some Themes

**Problem**: Some theme categories are not available in the Onemap API

**Solution**: 
This is normal. The script silently skips unavailable themes and continues with available ones.

### Issue: Slow Performance

**Problem**: Comprehensive mode with --all-themes is slow

**Solution**:
1. Use standard mode for faster results
2. Reduce search radius: `--radius 3`
3. Reduce max results: `--max-results 5`

### Issue: No Bus Stops Found

**Problem**: Search radius for bus stops is only 1km

**Solution**:
Bus stop search uses a 1km radius (hardcoded). This is intentional as you typically walk to nearby bus stops. MRT stations use a 5km radius.

## Getting Help

For more information, see:
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `ONEMAP_API_REFERENCE.md` - API details
- `API_IMPLEMENTATION_NOTES.md` - Technical implementation details
- `AUTHENTICATION.md` - Authentication guide

## Example Session

Here's what a complete session looks like:

```bash
$ python house_analyzer.py 1.3521 103.8198

================================================================================
HDB HOUSE ANALYZER - Using Onemap API
================================================================================

🔐 Onemap API Authentication Required
--------------------------------------------------------------------------------
Enter your Onemap email: user@example.com
Enter your Onemap password: [hidden]

✓ Credentials received. Authenticating...

================================================================================
HDB HOUSE ANALYSIS REPORT
================================================================================

🏠 Retrieving address information...
   Building: CENTRAL CATCHMENT NATURE RESERVE
   Road: NIL
   Postal Code: NIL

📍 Retrieving planning area information...

🏢 Analyzing nearby amenities...
   Searching for Kindergartens...
   Searching for Childcare...
   [... more categories ...]

🚇 Searching for nearby MRT stations...
🚌 Searching for nearby bus stops...
🛣️  Searching for major roads and expressways...

================================================================================
DETAILED ANALYSIS REPORT
================================================================================

📊 SUMMARY
--------------------------------------------------------------------------------
Total Amenities Found: 60
Nearest Amenity: Ang Mo Kio CC (Community Clubs) - 2.840 km
Nearest MRT: UPPER THOMSON MRT STATION (TE8) - 1.479 km

[... detailed results ...]

================================================================================

Do you want to save the report as JSON? (y/n): y
Enter filename (default: house_analysis_1.3521_103.8198.json): bishan_analysis.json

✅ Report saved to bishan_analysis.json
✅ Analysis complete!
```
