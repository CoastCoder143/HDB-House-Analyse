# Quick Start Guide - HDB House Analyzer

Get started with the HDB House Analyzer in just 3 steps!

## Step 1: Register (One-time, FREE)

Register for a Onemap API account (if you don't have one):
https://www.onemap.gov.sg/apidocs/register

- Fill in your details
- Verify your email
- That's it! You're ready to go.

## Step 2: Install

```bash
# Clone the repository
git clone https://github.com/CoastCoder143/HDB-House-Analyse.git
cd HDB-House-Analyse

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Analyzer

Simply run the script - it will ask for your credentials:

```bash
python house_analyzer.py
```

**What happens:**
1. You'll be prompted for your Onemap email and password
2. You'll be prompted for the house coordinates
3. Analysis runs and displays comprehensive results!

### Example Session

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

Enter your Onemap email: myemail@example.com
Enter your Onemap password: ••••••••

✓ Credentials received. Authenticating...

Please enter the house coordinates:
Latitude: 1.3048
Longitude: 103.8318

[Analysis results displayed...]
```

### Quick Mode with Coordinates

```bash
python house_analyzer.py 1.3048 103.8318
```

Still prompts for credentials, but coordinates are pre-filled.

### Skip Prompts (Optional)

Set environment variables to avoid credential prompts:

```bash
export ONEMAP_EMAIL='your_email@example.com'
export ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3048 103.8318
```

## What You'll See

The analyzer will display:
- ✅ Address information
- ✅ Planning area
- ✅ Nearby amenities (11 categories)
- ✅ Nearest MRT stations
- ✅ Nearest bus stops
- ✅ Major roads & expressways
- ✅ Distances to everything

## Example Locations to Try

### Central Business District
```bash
python house_analyzer.py 1.2844 103.8607
```

### Shopping District (Orchard)
```bash
python house_analyzer.py 1.3048 103.8318
```

### Residential Area (Tampines)
```bash
python house_analyzer.py 1.3496 103.9568
```

### New Town (Punggol)
```bash
python house_analyzer.py 1.4041 103.9025
```

## Understanding the Output

### Summary Section
Shows the most important information at a glance:
- Total amenities found
- Nearest amenity of any type
- Nearest MRT station
- Nearest bus stop
- Nearest major road

### Detailed Sections
Each category shows:
- Name of the facility
- Full address
- Distance in kilometers
- Distance in meters

### Saving Results
When prompted, you can save the full analysis as a JSON file for later use or further processing.

## Tips for Best Results

1. **Use Decimal Coordinates**: Not degrees/minutes/seconds
   - ✅ Correct: `1.3048, 103.8318`
   - ❌ Wrong: `1°18'17.3"N 103°49'54.5"E`

2. **Stay Within Singapore**: The tool validates coordinates
   - Latitude: 1.1 to 1.5
   - Longitude: 103.6 to 104.1

3. **Get Coordinates**: Use Google Maps
   - Right-click on a location
   - Click on the coordinates to copy them
   - Paste into the analyzer

4. **Check Internet**: Onemap API requires internet access

## Common Use Cases

### Buying/Renting a House
Analyze the location to understand:
- Distance to work (via MRT)
- Nearby schools for children
- Shopping and dining (hawker centres, supermarkets)
- Healthcare (pharmacies)
- Recreation (parks, gyms)

### Comparing Multiple Locations
Run the analyzer for each location and compare:
- Which has better MRT access?
- Which is closer to schools?
- Which has more amenities nearby?

### Investment Analysis
Understand the neighborhood:
- Planning area information
- Proximity to expressways (accessibility)
- Available amenities (attractiveness)

## Programmatic Usage

For developers who want to integrate the analyzer into their own code:

```python
from house_analyzer import HouseAnalyzer

# Initialize
analyzer = HouseAnalyzer()

# Analyze a location
results = analyzer.analyze_house(1.3048, 103.8318, max_results=10)

# Access specific data
nearest_mrt = results['transport']['mrt_stations'][0]
print(f"Nearest MRT: {nearest_mrt['name']}")
print(f"Distance: {nearest_mrt['distance_km']} km")

# Save to JSON
analyzer.save_report_json(results, "my_analysis.json")
```

See `example_usage.py` for more examples.

## Troubleshooting

### "Error in reverse geocoding"
- Check your internet connection
- Verify coordinates are valid
- Onemap API might be down (try again later)

### "No results found"
- You might be in a remote area
- Try increasing the search radius in the code
- Some categories might have limited data

### "Invalid coordinates"
- Ensure format is decimal: `1.3048, 103.8318`
- Check you're within Singapore bounds
- Latitude comes before longitude

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [ONEMAP_API_REFERENCE.md](ONEMAP_API_REFERENCE.md) for API details
- Modify `house_analyzer.py` to customize the analysis
- Contribute improvements via pull requests!

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error message carefully
3. Verify your internet connection
4. Check the GitHub issues page
5. Create a new issue with details

---

**Happy Analyzing! 🏠📊**
