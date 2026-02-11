# 🏠 Smart Property Agent - HDB House Analyzer 🔍

A **revolutionary** Python tool that transforms you into the smartest property agent in Singapore! Using 100+ Onemap API themes with intelligent analysis, it provides insights that others miss - livability scoring, investment potential, target demographics, and hidden value factors.

## 🌟 What Makes This Smart?

Unlike basic property tools that just list amenities, this analyzer:

- ✅ **Livability Scoring** (0-100 with letter grades A+ to D)
- ✅ **Smart Insights** that identify hidden value & risks
- ✅ **Investment Potential** ratings (High/Medium/Low)
- ✅ **Target Demographics** profiling (who should buy/rent)
- ✅ **Selling Points** generation for property showings
- ✅ **Comparative Intelligence** using 100+ data themes
- ✅ **Singapore-Specific** (hawker centres, MRT proximity, schools)

**See [SMART_AGENT_GUIDE.md](SMART_AGENT_GUIDE.md) for the complete professional guide!**

## ⚠️ Authentication Required

**Important**: The Onemap API requires authentication. You have two options:

1. **Interactive Mode** (Recommended for first-time users):
   - Just run the script - it will ask for your credentials
   - Register at: https://www.onemap.gov.sg/apidocs/register if you don't have an account

2. **Environment Variables** (Optional for convenience):
   ```bash
   export ONEMAP_EMAIL='your_email@example.com'
   export ONEMAP_PASSWORD='your_password'
   ```

See [AUTHENTICATION.md](AUTHENTICATION.md) for more details.

## 🚀 Quick Start - Smart Agent Mode

For the **smartest, most comprehensive analysis** using ALL 100+ themes:

```bash
# Install requirements
pip install -r requirements.txt

# Run with --all-themes for smart agent analysis
python house_analyzer.py 1.3521 103.8198 --all-themes
```

You'll get:
- 🎯 **Livability Score** (0-100 with letter grade)
- 💡 **Smart Insights** (what agents notice)
- 👥 **Ideal Demographics** (who should buy this)
- 🌟 **Key Selling Points** (for showings)
- 💰 **Investment Rating** (potential & rental appeal)
- ⚠️  **Risk Factors** (honest concerns)

Example coordinates to try:
- **Bishan**: `1.3521, 103.8198` (excellent connectivity)
- **Marina Bay**: `1.2844, 103.8607` (CBD location)
- **Punggol**: `1.4041, 103.9025` (new town)

## Features ✨

### 🎯 Smart Property Intelligence

#### Livability Scoring System (0-100 points)
- **Transport** (25 pts): MRT, bus, expressway access
- **Education** (20 pts): Schools, childcare, libraries
- **Healthcare** (15 pts): Hospitals, clinics, pharmacies
- **Shopping** (20 pts): Hawkers, supermarkets, malls
- **Recreation** (10 pts): Parks, community clubs, gyms
- **Safety** (10 pts): Dengue, industrial areas, hazards

#### Smart Insights Generation
- 🌟 Hidden value factors (e.g., "MRT within 500m = PRIME!")
- ⚠️  Risk identification (e.g., dengue clusters, noise)
- ✅ Balanced perspectives (pros AND cons)
- 🎯 Singapore-specific context (hawker centres valued!)

#### Property Profiling
- **Target Demographics**: Who should buy/rent
- **Selling Points**: Ready-made talking points
- **Investment Potential**: High/Medium/Low rating
- **Rental Attractiveness**: Market appeal assessment

### Core Analysis
- **Address Information**: Reverse geocoding to get detailed address from coordinates
- **Planning Area Details**: Get planning area and location information

### Two Modes of Operation

#### 1. Standard Mode (Fast & Focused)
Uses a curated set of 11 amenity categories:
  - Kindergartens and Childcare Centers
  - Parks and National Parks
  - Libraries
  - Community Clubs
  - Eldercare Centers
  - Plus: MRT stations, bus stops, and major expressways

#### 2. Smart Agent Mode (--all-themes flag) ⭐
Access to **100+ thematic layers** from Onemap API with intelligent analysis:
  - All standard amenities PLUS
  - Dengue clusters
  - CET centres
  - Healthcare facilities
  - Educational institutions
  - Sports facilities
  - And many more government-provided datasets
  - **PLUS**: Livability scoring, insights, and recommendations!

### Transport & Infrastructure
- **Public Transport Analysis**:
  - Nearby MRT stations (within 5km)
  - Nearby bus stops (within 1km)
  - Distance calculations for each
- **Major Roads & Expressways**:
  - PIE (Pan Island Expressway)
  - CTE (Central Expressway)
  - ECP (East Coast Parkway)
  - AYE (Ayer Rajah Expressway)
  - BKE (Bukit Timah Expressway)
  - KPE (Kallang-Paya Lebar Expressway)
  - SLE (Seletar Expressway)
  - TPE (Tampines Expressway)
  - MCE (Marina Coastal Expressway)
  - KJE (Kranji Expressway)
- **Configurable Search Radius**: Customize the search area (default: 5km)

- **Distance Calculations**: Haversine formula for accurate distance measurements
- **Detailed Reporting**: Comprehensive analysis with sorting by distance
- **JSON Export**: Save full analysis report in JSON format
- **Token-Based Authentication**: Automatic token management and refresh
- **Interactive Credential Prompts**: No need to set environment variables

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/CoastCoder143/HDB-House-Analyse.git
cd HDB-House-Analyse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Register for Onemap API** (one-time, FREE):
   - Visit: https://www.onemap.gov.sg/apidocs/register
   - Fill in your details and verify your email

That's it! The script will prompt you for credentials when you run it.

## Usage 📖

### Method 1: Interactive Mode (Recommended)

Simply run the script - it will ask for everything it needs:

```bash
python house_analyzer.py
```

The script will prompt you for:
1. **Onemap credentials** (if not set as environment variables):
   - Email address
   - Password (hidden input - nothing appears when you type, this is normal!)
2. **House coordinates**:
   - Latitude
   - Longitude

**Important**: When entering your password, you won't see any characters appear on screen. This is intentional for security - just type your password and press Enter.

Example session:
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

Enter your Onemap email: your_email@example.com

💡 Note: Your password will be hidden as you type (no characters will appear).
   This is normal for security. Just type your password and press Enter.

Enter your Onemap password: [nothing shown while typing]

✓ Credentials received. Authenticating...

Please enter the house coordinates:
Latitude: 1.3521
Longitude: 103.8198
```

### Method 2: Command Line Arguments

Provide coordinates directly as command line arguments:

```bash
# Standard mode (fast, curated categories)
python house_analyzer.py 1.3521 103.8198

# Comprehensive mode (100+ theme categories)
python house_analyzer.py 1.3521 103.8198 --all-themes

# Custom search radius (10km instead of default 5km)
python house_analyzer.py 1.3521 103.8198 --radius 10

# More results per category (20 instead of default 10)
python house_analyzer.py 1.3521 103.8198 --max-results 20

# Combine options
python house_analyzer.py 1.3521 103.8198 --all-themes --radius 7.5 --max-results 15
```

### Command Line Options

- `--all-themes`: Use ALL 100+ available themes from Onemap API (comprehensive but slower)
- `--radius KILOMETERS`: Set search radius in kilometers (default: 5.0)
- `--max-results NUMBER`: Maximum results per category (default: 10)
- `-h, --help`: Show help message

**Note**: The `--all-themes` flag will:
- Fetch all available themes dynamically from the Onemap API
- Provide access to 100+ data categories
- Take longer to run (more API calls)
- Give you the most comprehensive analysis possible

Note: You'll still be prompted for credentials if they're not in environment variables.

### Method 3: Pre-set Environment Variables (Optional)

For convenience, you can set credentials once and avoid repeated prompts:

```bash
export ONEMAP_EMAIL='your_email@example.com'
export ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3521 103.8198
```

### Example Coordinates

Here are some example coordinates you can try:

- **Marina Bay**: `1.2844, 103.8607`
- **Orchard Road**: `1.3048, 103.8318`
- **Jurong East**: `1.3329, 103.7436`
- **Punggol**: `1.4041, 103.9025`
- **Tampines**: `1.3496, 103.9568`

## Sample Output 📊

```
================================================================================
HDB HOUSE ANALYSIS REPORT
================================================================================

🏠 Retrieving address information...
   Building: RAFFLES PLACE MRT STATION
   Block: N/A
   Road: RAFFLES PLACE
   Postal Code: 048616

📍 Retrieving planning area information...
   Planning Area: DOWNTOWN CORE

🏢 Analyzing nearby amenities...
   Searching for Kindergartens...
   Searching for Childcare...
   Searching for Parks...
   [... more amenities ...]

🚇 Searching for nearby MRT stations...
🚌 Searching for nearby bus stops...
🛣️  Searching for major roads and expressways...

================================================================================
DETAILED ANALYSIS REPORT
================================================================================

📊 SUMMARY
--------------------------------------------------------------------------------
Total Amenities Found: 87
Nearest Amenity: Downtown East Park (Parks) - 0.234 km
Nearest MRT: Raffles Place MRT Station - 0.089 km
Nearest Bus Stop: Bus Stop 01012 - 45 m
Nearest Major Road: Marina Coastal Expressway (MCE) - 1.234 km

🏢 AMENITIES BREAKDOWN
--------------------------------------------------------------------------------

Kindergartens (8 found):
  1. Little Hands Montessori Kindergarten
     Address: 123 Example Street Singapore 123456
     Distance: 0.456 km (456 m)
  [... more results ...]

[... detailed listings for all categories ...]
```

## Output Format 📝

The script provides:

1. **Console Output**: Formatted, human-readable analysis printed to terminal
2. **JSON Export** (optional): Complete data structure saved to file with:
   - Coordinates
   - Address details
   - Planning area information
   - All amenities with distances
   - Transport options
   - Summary statistics

## API Information 🔌

This tool uses the Singapore Government's **Onemap API**, which is free and publicly available. The following endpoints are utilized:

- **Reverse Geocoding API**: Convert coordinates to addresses
- **Search API**: Search for locations, MRT stations, and bus stops
- **Thematics API**: Retrieve themed data (amenities)
- **Planning Area API**: Get planning area information

### Rate Limits

The Onemap API has rate limits. This script includes:
- Timeout handling (10 seconds per request)
- Error handling for failed requests
- Reasonable request limits per category

## Technical Details 🔧

### Distance Calculation

The script uses the **Haversine formula** to calculate accurate distances between coordinates on Earth's surface:

```python
distance_km = haversine(lat1, lon1, lat2, lon2)
```

This provides more accurate results than simple Euclidean distance for geographical coordinates.

### Coordinate Validation

The script validates that coordinates are within Singapore's bounds:
- Latitude: 1.1 to 1.5
- Longitude: 103.6 to 104.1

## Dependencies 📦

- **Python 3.6+**
- **requests**: For HTTP API calls

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available for educational and personal use.

## Acknowledgments 🙏

- **Onemap API** by Singapore Land Authority (SLA) for providing the geographical data
- **Housing & Development Board (HDB)** for Singapore's public housing

## Troubleshooting 🔍

### Common Issues

1. **"Error in reverse geocoding"**: Check your internet connection and ensure coordinates are valid
2. **"No results found"**: Try different coordinates or check if you're within Singapore bounds
3. **API timeouts**: The Onemap API might be experiencing high traffic, try again later

### Getting Help

If you encounter issues:
1. Check that your coordinates are in decimal format (not degrees/minutes/seconds)
2. Ensure you have an active internet connection
3. Verify that the Onemap API is accessible from your location

## Future Enhancements 🚀

Potential improvements:
- Add caching for repeated queries
- Include property price analysis
- Add visualization with maps
- Support for batch analysis of multiple locations
- Integration with property transaction data
- Walking/driving time estimates
- Flood risk and other environmental data

---

**Made with ❤️ for Singapore HDB analysis**