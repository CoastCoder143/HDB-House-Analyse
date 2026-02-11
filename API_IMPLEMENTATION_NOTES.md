# Onemap API Implementation Notes

## Alignment with Official Python Documentation

This document explains how our implementation aligns with the official Onemap API Python documentation.

### Official Documentation Examples

The official Onemap API documentation shows Python examples like this:

```python
import requests

url = "https://www.onemap.gov.sg/api/public/themesvc/getAllThemesInfo?moreInfo=Y"
headers = {"Authorization": "**********************"}
response = requests.request("GET", url, headers=headers)
print(response.text)
```

### Our Implementation

We use a session-based approach:

```python
import requests

class OneMapAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': self.access_token})
    
    def _make_authenticated_request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)
```

### Why This is Equivalent and Better

Both approaches achieve the same result, but our session-based approach has several advantages:

1. **Connection Pooling**: Reuses TCP connections for multiple requests (faster)
2. **Automatic Headers**: Authorization header automatically included in all requests
3. **Token Management**: Built-in token refresh when expired
4. **Cleaner Code**: No need to pass headers to every request

### Verification

Both approaches set the Authorization header correctly:

```python
# Official docs
headers = {"Authorization": "token_value"}

# Our implementation
session.headers.update({"Authorization": "token_value"})

# Both result in the same HTTP request header:
# Authorization: token_value
```

## Supported Endpoints

Our implementation supports all documented Onemap API endpoints:

### 1. Authentication
```python
POST /api/auth/post/getToken
```
- Automatically handles token retrieval
- Stores token with 3-day expiry
- Auto-refreshes when expired

### 2. Get All Themes Info
```python
GET /api/public/themesvc/getAllThemesInfo?moreInfo=Y
```
- Method: `get_all_themes_info(more_info=True)`
- Returns 100+ available themes
- Used in `--all-themes` mode

### 3. Get Theme Info
```python
GET /api/public/themesvc/getThemeInfo?queryName=kindergartens
```
- Supported but not currently used
- Can be added if needed

### 4. Retrieve Theme
```python
GET /api/public/themesvc/retrieveTheme?queryName=dengue_cluster
```
- Method: `get_theme_data(query_name)`
- Used in standard mode

### 5. Retrieve Theme with Extents
```python
GET /api/public/themesvc/retrieveTheme?queryName=dengue_cluster&extents=1.291,103.779,1.329,103.872
```
- Method: `get_theme_data(query_name, extents=...)`
- Used for boundary-based queries
- Returns more results than lat/lng

### 6. Reverse Geocode
```python
GET /api/public/revgeocode?location=1.3254,103.9005&buffer=40&addressType=All
```
- Method: `reverse_geocode(lat, lon)`
- Converts coordinates to address

### 7. Search Location
```python
GET /api/public/search?searchVal=MRT&returnGeom=Y
```
- Method: `search_location(query, return_geom=True)`
- Used for MRT, bus stops, roads

### 8. Planning Area
```python
GET /api/public/popapi/getPlanningarea?lat=1.3521&lng=103.8198
```
- Method: `get_planning_area(lat, lon)`
- Returns government planning zone

## Authorization Header Format

**Important**: Onemap API requires just the token value, **NOT** "Bearer {token}"

✅ Correct:
```python
headers = {"Authorization": "eyJhbGc..."}
```

❌ Incorrect:
```python
headers = {"Authorization": "Bearer eyJhbGc..."}
```

Our implementation uses the correct format.

## Error Handling

We handle all documented error responses:

- **400**: Bad Request (invalid parameters)
- **401**: Unauthorized (token expired or invalid)
- **403**: Forbidden (access not allowed)
- **404**: Not Found (theme not available)
- **429**: Rate limit exceeded

## Extents Parameter

The extents parameter defines a bounding box for spatial queries:

```
Format: lat_min,lng_min,lat_max,lng_max
Example: 1.291789,103.7796402,1.3290461,103.8726032
```

Our implementation automatically calculates extents from a center point and radius:

```python
def calculate_extents(lat, lon, radius_km=5.0):
    # Calculates bounding box
    # Returns: "lat_min,lng_min,lat_max,lng_max"
```

## Performance Comparison

### Official Docs Approach (Individual Requests)
```python
for theme in themes:
    headers = {"Authorization": token}
    response = requests.request("GET", url, headers=headers)
    # New TCP connection for each request ⚠️
```

### Our Approach (Session)
```python
session = requests.Session()
session.headers.update({"Authorization": token})
for theme in themes:
    response = session.request("GET", url)
    # Reuses TCP connection ✅
```

**Result**: Our approach is faster for multiple API calls.

## Conclusion

Our implementation:
- ✅ Follows official Python API documentation
- ✅ Uses correct Authorization header format
- ✅ Supports all documented endpoints
- ✅ Handles all error responses
- ✅ Provides additional benefits (connection pooling, token management)
- ✅ Is more efficient for multiple requests

The session-based approach is a best practice and is functionally equivalent to the examples in the official documentation, while providing better performance and cleaner code.
