# Network Requirements for HDB House Analyzer

## ⚠️ Important: Internet Connection Required

The HDB House Analyzer requires **active internet connection** to function properly. It connects to Singapore's government Onemap API at `www.onemap.gov.sg` to retrieve:

- Address information
- MRT/Bus stop locations
- Amenity data (schools, parks, etc.)
- Road information
- Planning area details

---

## Common Issues & Solutions

### Issue: "Bus stops missing" or "No data found"

**Symptoms**:
```
🚌 Bus Stops:
  No bus stops found within 1 km

🛣️  ROADS & EXPRESSWAYS
  No major roads found within 3 km
```

**Possible Causes**:

#### 1. No Internet Connection
**Check**: Can you access websites?
**Solution**: Connect to internet and try again

#### 2. Firewall Blocking Access
**Check**: Can you access https://www.onemap.gov.sg in your browser?
**Solution**: 
- Allow outbound HTTPS (port 443) to www.onemap.gov.sg
- Whitelist domain in firewall/proxy
- Contact IT support if on corporate network

#### 3. DNS Resolution Failure
**Error**: `Failed to resolve 'www.onemap.gov.sg'`
**Solution**:
- Check DNS settings
- Try using public DNS (8.8.8.8, 1.1.1.1)
- Restart network connection

#### 4. Running in Restricted Environment
**Examples**:
- Docker containers without network access
- CI/CD pipelines without internet
- Air-gapped systems

**Solutions**:
- Enable network access for the environment
- Use mock/cached data for testing (see below)
- Run on a machine with internet access

---

## Network Test

Before running the analyzer, test your connection:

```bash
# Test 1: Can you reach the API?
curl https://www.onemap.gov.sg

# Test 2: Can you resolve DNS?
nslookup www.onemap.gov.sg

# Test 3: Can Python reach it?
python -c "import requests; print(requests.get('https://www.onemap.gov.sg').status_code)"
```

Expected result: Should return 200 or similar successful status.

---

## Improved Error Messages

The analyzer now provides clear error messages when network issues occur:

### Connectivity Check
```
🔍 Checking connectivity to Onemap API...
⚠️  Cannot reach Onemap API server (www.onemap.gov.sg)
   Possible causes:
   1. No internet connection
   2. Firewall blocking access
   3. DNS resolution failure
   
   Please ensure you have internet access and try again.

================================================================================
❌ ANALYSIS CANNOT PROCEED
================================================================================

The analyzer requires internet access to:
  • www.onemap.gov.sg (Singapore Government API)

Please:
  1. Check your internet connection
  2. Ensure firewall allows HTTPS to www.onemap.gov.sg
  3. Try again once connected
```

### Individual API Errors
```
⚠️  Network error - Cannot reach Onemap API server
   Please check your internet connection and try again.
```

---

## Working Environments

✅ **These environments typically work**:
- Personal computers with internet
- Cloud servers (AWS, GCP, Azure)
- Home networks
- Mobile hotspots
- University networks (if not restricted)

❌ **These environments may have issues**:
- Corporate networks with strict firewalls
- Air-gapped systems
- Docker containers without `--network=host`
- Some CI/CD pipelines
- Offline environments

---

## For Developers: Offline Testing

If you need to test without internet access, consider:

### Option 1: Mock Data
Create sample responses and use mock objects:

```python
from unittest.mock import Mock, patch

mock_api = Mock()
mock_api.get_nearest_bus_stops.return_value = [
    {'id': 1, 'name': 'Test Stop', 'lat': 1.3, 'lon': 103.8}
]

analyzer = HouseAnalyzer(api=mock_api)
```

### Option 2: Cached Responses
Save API responses and load them:

```python
import json

# Save responses once (with internet)
results = api.get_nearest_bus_stops(1.3521, 103.8198)
with open('bus_stops_cache.json', 'w') as f:
    json.dump(results, f)

# Use cached data (offline)
with open('bus_stops_cache.json') as f:
    cached_results = json.load(f)
```

### Option 3: Local Mock Server
Run a local server that mimics Onemap API responses.

---

## Required Network Access

The analyzer needs to access these endpoints:

### Authentication:
```
POST https://www.onemap.gov.sg/api/auth/post/getToken
```

### APIs Used:
```
GET https://www.onemap.gov.sg/api/public/revgeocode
GET https://www.onemap.gov.sg/api/public/popapi/getPlanningarea
GET https://www.onemap.gov.sg/api/common/elastic/search
GET https://www.onemap.gov.sg/api/public/nearbysvc/getNearestMrtStops
GET https://www.onemap.gov.sg/api/public/nearbysvc/getNearestBusStops
GET https://www.onemap.gov.sg/api/public/themesvc/getAllThemesInfo
GET https://www.onemap.gov.sg/api/public/themesvc/retrieveTheme
GET https://www.onemap.gov.sg/api/public/routingsvc/route
```

**Port**: 443 (HTTPS)
**Protocol**: TLS 1.2+
**Method**: GET, POST

---

## Firewall Configuration

If configuring firewall rules, allow:

- **Destination**: www.onemap.gov.sg
- **Port**: 443
- **Protocol**: HTTPS
- **Direction**: Outbound
- **Methods**: GET, POST

---

## Troubleshooting Checklist

When you see "No bus stops found" or similar:

- [ ] Can you ping www.onemap.gov.sg?
- [ ] Can you access https://www.onemap.gov.sg in browser?
- [ ] Is your firewall blocking Python/requests?
- [ ] Are you behind a corporate proxy?
- [ ] Do you have valid Onemap credentials?
- [ ] Is your internet connection working for other sites?
- [ ] Are you in a restricted environment (Docker, CI/CD)?

---

## Getting Help

If you've verified network connectivity and still have issues:

1. **Check the error message** - The analyzer now provides specific guidance
2. **Run debug script**: `python debug_bus_stops.py`
3. **Test with curl**: `curl https://www.onemap.gov.sg/api/public/ping`
4. **Check Onemap status**: Visit https://www.onemap.gov.sg
5. **Review authentication**: Ensure credentials are correct

---

## Summary

**The Key Point**: This tool requires internet access to Singapore's government Onemap API. Without it, you'll see "No data found" messages.

**Quick Fix**: Ensure you have internet access and can reach www.onemap.gov.sg before running the analyzer.

**For Testing**: Use mock data or cached responses if internet is unavailable.

---

Last Updated: 2026-02-11
