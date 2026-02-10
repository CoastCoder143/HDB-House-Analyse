# HDB House Analyzer 🏠

A comprehensive Python tool to analyze HDB (Housing & Development Board) houses in Singapore using the Onemap API. This script provides detailed information about any location including nearby amenities, public transport, major roads, and planning area details.

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

## Features ✨

- **Address Information**: Reverse geocoding to get detailed address from coordinates
- **Planning Area Details**: Get planning area and location information
- **Comprehensive Amenity Search**:
  - Kindergartens and Childcare Centers
  - Parks and National Parks
  - Gyms and Fitness Centers
  - Hawker Centres
  - Supermarkets
  - Pharmacies
  - Libraries
  - Community Clubs
  - Eldercare Centers
  - Registered Schools
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
python house_analyzer.py 1.3521 103.8198
```

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