#!/usr/bin/env python3
"""
Debug script to test bus stops and roads APIs
"""

from house_analyzer import OneMapAPI
import json

def test_bus_stops():
    """Test bus stops API"""
    print("=" * 80)
    print("TESTING BUS STOPS API")
    print("=" * 80)
    
    # Initialize API
    api = OneMapAPI()
    
    # Test location: Bishan (known to have bus stops)
    test_lat = 1.3521
    test_lon = 103.8198
    
    print(f"\nTest location: Bishan ({test_lat}, {test_lon})")
    print(f"Authentication status: {api.access_token is not None}")
    
    if api.access_token:
        print(f"Token: {api.access_token[:20]}...")
    else:
        print("⚠️  No token - API calls may fail!")
    
    print("\n" + "-" * 80)
    print("Calling getNearestBusStops API...")
    print("-" * 80)
    
    # Call the API
    bus_results = api.get_nearest_bus_stops(test_lat, test_lon, radius_m=1000)
    
    print(f"\nRaw API response type: {type(bus_results)}")
    print(f"Number of results: {len(bus_results) if isinstance(bus_results, list) else 'N/A'}")
    
    if bus_results:
        print(f"\nFirst result:")
        print(json.dumps(bus_results[0] if isinstance(bus_results, list) else bus_results, indent=2))
        
        if len(bus_results) > 1:
            print(f"\nTotal bus stops found: {len(bus_results)}")
            for i, stop in enumerate(bus_results[:5], 1):
                print(f"  {i}. {stop.get('name', 'N/A')} (ID: {stop.get('id', 'N/A')})")
    else:
        print("\n❌ No results returned!")
        print("This could mean:")
        print("  1. API authentication failed")
        print("  2. No bus stops within radius")
        print("  3. API error (check errors above)")

def test_mrt_stations():
    """Test MRT stations API for comparison"""
    print("\n" + "=" * 80)
    print("TESTING MRT STATIONS API (for comparison)")
    print("=" * 80)
    
    api = OneMapAPI()
    
    test_lat = 1.3521
    test_lon = 103.8198
    
    print(f"\nTest location: Bishan ({test_lat}, {test_lon})")
    
    print("\n" + "-" * 80)
    print("Calling getNearestMrtStops API...")
    print("-" * 80)
    
    mrt_results = api.get_nearest_mrt_stops(test_lat, test_lon, radius_m=5000)
    
    print(f"\nNumber of MRT results: {len(mrt_results) if isinstance(mrt_results, list) else 'N/A'}")
    
    if mrt_results:
        print(f"\nFirst few MRT stations:")
        for i, station in enumerate(mrt_results[:3], 1):
            print(f"  {i}. {station.get('name', 'N/A')} ({station.get('id', 'N/A')})")
    else:
        print("\n❌ No MRT results returned!")

def test_roads():
    """Test roads search"""
    print("\n" + "=" * 80)
    print("TESTING ROADS SEARCH")
    print("=" * 80)
    
    api = OneMapAPI()
    
    print("\n" + "-" * 80)
    print("Searching for PIE (Pan Island Expressway)...")
    print("-" * 80)
    
    pie_results = api.search_location("PIE")
    
    print(f"\nRaw response keys: {pie_results.keys() if isinstance(pie_results, dict) else 'N/A'}")
    
    if pie_results and 'results' in pie_results:
        print(f"Number of PIE results: {len(pie_results['results'])}")
        if pie_results['results']:
            print(f"\nFirst PIE result:")
            print(json.dumps(pie_results['results'][0], indent=2))
    else:
        print("\n❌ No road results!")

if __name__ == '__main__':
    try:
        test_bus_stops()
        test_mrt_stations()
        test_roads()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
