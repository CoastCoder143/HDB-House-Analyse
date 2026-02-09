# Onemap API Reference for HDB House Analyzer

This document describes the Onemap API endpoints used by the HDB House Analyzer and the data they provide.

## Overview

The Onemap API is Singapore's official government mapping API provided by the Singapore Land Authority (SLA). It offers various services for geocoding, searching, routing, and thematic data retrieval.

**Base URL**: `https://www.onemap.gov.sg/api`

## Endpoints Used

### 1. Reverse Geocoding API

**Purpose**: Convert latitude/longitude coordinates to a human-readable address.

**Endpoint**: `GET /public/revgeocode`

**Parameters**:
- `location` (required): Latitude and longitude in format "lat,lon"
- `buffer` (optional): Buffer distance in meters (default: 10)
- `addressType` (optional): Type of address to return (All, HDB, etc.)
- `otherFeatures` (optional): Include other features (Y/N)

**Returns**:
- Building name
- Block number
- Road name
- Postal code
- Precise coordinates

**Example**:
```
GET /api/public/revgeocode?location=1.3048,103.8318&buffer=10&addressType=All&otherFeatures=Y
```

---

### 2. Search/Elastic Search API

**Purpose**: Search for locations by name, postal code, or other identifiers.

**Endpoint**: `GET /common/elastic/search`

**Parameters**:
- `searchVal` (required): Search query string
- `returnGeom` (optional): Return geometry (Y/N)
- `getAddrDetails` (optional): Get address details (Y/N)
- `pageNum` (optional): Page number for pagination

**Used For**:
- Finding MRT stations
- Finding bus stops
- Finding expressways and major roads

**Returns**:
- Location name
- Address
- Coordinates (latitude, longitude)
- Additional metadata

**Example**:
```
GET /api/common/elastic/search?searchVal=MRT&returnGeom=Y&getAddrDetails=Y&pageNum=1
```

---

### 3. Thematics API

**Purpose**: Retrieve themed/categorized point-of-interest data near a location.

**Endpoint**: `GET /public/themesvc/retrieveTheme`

**Parameters**:
- `queryName` (required): Theme/category name
- `lat` (required): Latitude
- `lng` (required): Longitude

**Available Themes**:

| Theme Name | Description |
|------------|-------------|
| `kindergartens` | Kindergarten locations |
| `childcare` | Childcare centers |
| `nationalparks` | Parks and national parks |
| `gyms` | Gym and fitness centers |
| `hawkercentres` | Hawker centres |
| `supermarkets` | Supermarket locations |
| `pharmacies` | Pharmacy locations |
| `libraries` | Public libraries |
| `communityclubs` | Community clubs |
| `eldercare` | Eldercare centers |
| `registeredschools` | Registered schools |

**Returns**:
- Name of facility
- Address
- Coordinates
- Additional metadata (varies by theme)

**Example**:
```
GET /api/public/themesvc/retrieveTheme?queryName=kindergartens&lat=1.3048&lng=103.8318
```

---

### 4. Planning Area API

**Purpose**: Get planning area information for a given location.

**Endpoint**: `GET /public/popapi/getPlanningarea`

**Parameters**:
- `lat` (required): Latitude
- `lng` (required): Longitude

**Returns**:
- Planning area name
- Planning area code
- Region information

**Example**:
```
GET /api/public/popapi/getPlanningarea?lat=1.3048&lng=103.8318
```

---

### 5. Routing API (Optional)

**Purpose**: Get route information and accurate travel distances between points.

**Endpoint**: `GET /public/routingsvc/route`

**Parameters**:
- `start` (required): Start coordinates "lat,lon"
- `end` (required): End coordinates "lat,lon"
- `routeType` (required): Type of route (drive, walk, cycle, pt)

**Returns**:
- Route geometry
- Distance
- Estimated time
- Turn-by-turn instructions

**Example**:
```
GET /api/public/routingsvc/route?start=1.3048,103.8318&end=1.2844,103.8607&routeType=drive
```

**Note**: The current implementation uses Haversine formula for distance calculation as a fallback, which provides accurate straight-line distances. The routing API can be used for actual road/walking distances.

---

## Data Processing

### Distance Calculation

The analyzer uses the **Haversine formula** to calculate great-circle distances between two points on Earth:

```python
R = 6371  # Earth's radius in kilometers

lat1_rad = radians(lat1)
lat2_rad = radians(lat2)
delta_lat = radians(lat2 - lat1)
delta_lon = radians(lon2 - lon1)

a = sin(delta_lat/2)² + cos(lat1) * cos(lat2) * sin(delta_lon/2)²
c = 2 * asin(sqrt(a))

distance = R * c
```

This provides accurate distances for:
- Short distances (< 100km) with < 0.5% error
- Great circle paths (shortest distance on Earth's surface)

### Filtering and Sorting

Results are:
1. **Filtered** by maximum distance:
   - MRT stations: 5 km radius
   - Bus stops: 1 km radius
   - Major roads: 3 km radius
   - Amenities: No limit (API returns nearest)

2. **Sorted** by distance (nearest first)

3. **Limited** to top results (default: 10 per category)

---

## Rate Limits and Best Practices

### Rate Limits
- Onemap API has rate limits (exact limits not publicly specified)
- The analyzer includes 10-second timeouts per request
- Implements error handling for failed requests

### Best Practices
1. **Cache results** if querying the same location multiple times
2. **Batch queries** when analyzing multiple locations
3. **Handle errors gracefully** (network issues, API downtime)
4. **Validate coordinates** before making API calls
5. **Respect rate limits** by adding delays if needed

---

## Error Handling

The analyzer handles various error scenarios:

| Error Type | Handling |
|------------|----------|
| Network errors | Caught and logged, continues with other queries |
| Invalid coordinates | Validation with warning prompt |
| API timeouts | 10-second timeout, graceful failure |
| Empty results | Displays "No results found" messages |
| Malformed responses | Try-catch blocks with fallback to empty data |

---

## Data Accuracy

### Coordinate Precision
- API accepts coordinates with up to 6 decimal places
- 6 decimal places ≈ 11cm precision
- Typical GPS accuracy: 5-10 meters

### Distance Accuracy
- Haversine formula: ±0.5% for distances < 100km
- Actual walking/driving distance may differ due to:
  - Road layout
  - Terrain
  - Building locations
  
### Data Freshness
- Onemap data is regularly updated by government agencies
- Some categories update more frequently than others
- Check the API for the most current data

---

## Singapore Coordinate Bounds

Valid coordinates for Singapore:
- **Latitude**: 1.1° to 1.5° N
- **Longitude**: 103.6° to 104.1° E

Common areas:
- Marina Bay: 1.2844, 103.8607
- Orchard Road: 1.3048, 103.8318
- Jurong East: 1.3329, 103.7436
- Punggol: 1.4041, 103.9025
- Tampines: 1.3496, 103.9568
- Woodlands: 1.4382, 103.7891
- Changi: 1.3644, 103.9915

---

## Future Enhancements

Potential additional APIs that could be integrated:

1. **Population Query API**: Get demographic data for planning areas
2. **URA Space API**: Get land use and property information
3. **HDB Property Information**: Get HDB-specific data
4. **Traffic API**: Real-time traffic conditions
5. **Weather API**: Climate and weather data
6. **School Information API**: Detailed school data
7. **Property Transaction API**: Historical transaction prices

---

## Resources

- **Onemap API Documentation**: https://www.onemap.gov.sg/docs/
- **OneMap Portal**: https://www.onemap.gov.sg/
- **Data.gov.sg**: https://data.gov.sg/ (Additional Singapore datasets)
- **Singapore Land Authority**: https://www.sla.gov.sg/

---

## License and Attribution

- Onemap API is provided by Singapore Land Authority (SLA)
- Data is from various Singapore government agencies
- Free for use with proper attribution
- Check official documentation for terms of service

---

**Last Updated**: 2026-02-09
