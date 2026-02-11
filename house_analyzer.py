#!/usr/bin/env python3
"""
HDB House Analyzer using Onemap API
====================================

This script analyzes a house location using Singapore's Onemap API.
It provides comprehensive information about:
- Address and location details
- Nearby amenities (schools, parks, community centers, etc.)
- Public transport (MRT stations, bus stops)
- Major roads and expressways
- Planning area information
- Distance calculations to all nearby features

Author: HDB House Analyzer
"""

import requests
import json
import math
import os
import getpass
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import sys


@dataclass
class Location:
    """Represents a geographical location."""
    latitude: float
    longitude: float
    name: str = ""
    address: str = ""
    category: str = ""
    distance: float = 0.0


class OneMapAPI:
    """Wrapper for Onemap API endpoints."""
    
    BASE_URL = "https://www.onemap.gov.sg/api"
    AUTH_URL = "https://www.onemap.gov.sg/api/auth/post/getToken"
    
    # Theme codes for different amenities
    THEMES = {
        'kindergartens': 'kindergartens',
        'childcare': 'childcare',
        'parks': 'nationalparks',
        'gyms': 'gyms',
        'hawker_centres': 'hawkercentres',
        'supermarkets': 'supermarkets',
        'pharmacies': 'pharmacies',
        'libraries': 'libraries',
        'community_clubs': 'communityclubs',
        'eldercare': 'eldercare',
        'registered_schools': 'registeredschools'
    }
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the Onemap API client.
        
        Args:
            email: Onemap API email (optional, can be set via environment variable ONEMAP_EMAIL)
            password: Onemap API password (optional, can be set via environment variable ONEMAP_PASSWORD)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HDB-House-Analyzer/1.0'
        })
        
        # Get credentials from parameters or environment variables
        self.email = email or os.getenv('ONEMAP_EMAIL')
        self.password = password or os.getenv('ONEMAP_PASSWORD')
        
        self.access_token = None
        self.token_expiry = None
        self.available_themes = None  # Cache for available themes
        
        # Try to authenticate if credentials are provided
        if self.email and self.password:
            self._authenticate()
    
    def _authenticate(self) -> bool:
        """
        Authenticate with Onemap API and get access token.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            payload = {
                'email': self.email,
                'password': self.password
            }
            
            response = requests.post(
                self.AUTH_URL,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                
                # Tokens typically expire in 3 days, set expiry time
                # Convert to int in case API returns string
                expires_in_raw = data.get('expiry_timestamp', 259200)
                try:
                    expires_in = int(expires_in_raw)
                except (ValueError, TypeError):
                    expires_in = 259200  # default 3 days in seconds
                
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                
                # Update session headers with token
                if self.access_token:
                    self.session.headers.update({
                        'Authorization': self.access_token
                    })
                    return True
            else:
                print(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error during authentication: {e}")
            return False
        
        return False
    
    def _ensure_authenticated(self) -> bool:
        """
        Ensure we have a valid authentication token.
        
        Returns:
            True if authenticated, False otherwise
        """
        # Check if token exists and is not expired
        if self.access_token and self.token_expiry:
            if datetime.now() < self.token_expiry:
                return True
        
        # Try to re-authenticate
        if self.email and self.password:
            return self._authenticate()
        
        return False
    
    def _make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an authenticated request to the API.
        
        Args:
            method: HTTP method (get, post, etc.)
            url: URL to request
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response object
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            # If no credentials, try without auth (some endpoints might be public)
            pass
        
        # Make the request
        response = self.session.request(method, url, **kwargs)
        return response
    
    def reverse_geocode(self, lat: float, lon: float) -> Dict:
        """
        Get address from coordinates using reverse geocoding.
        
        Args:
            lat: Latitude (WGS84 format)
            lon: Longitude (WGS84 format)
            
        Returns:
            Dictionary with geocoding results
        """
        url = f"{self.BASE_URL}/public/revgeocode"
        params = {
            'location': f"{lat},{lon}",
            'buffer': 10,
            'addressType': 'All'
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error in reverse geocoding: {e}")
            return {}
    
    def search_location(self, search_val: str, return_geom: str = 'Y', get_addr_details: str = 'Y') -> Dict:
        """
        Search for a location by name or postal code.
        
        Args:
            search_val: Search query
            return_geom: Return geometry (Y/N)
            get_addr_details: Get address details (Y/N)
            
        Returns:
            Dictionary with search results
        """
        url = f"{self.BASE_URL}/common/elastic/search"
        params = {
            'searchVal': search_val,
            'returnGeom': return_geom,
            'getAddrDetails': get_addr_details,
            'pageNum': 1
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error in location search: {e}")
            return {}
    
    def get_all_themes_info(self, more_info: bool = True) -> List[Dict]:
        """
        Get all available themes from Onemap API.
        
        Args:
            more_info: If True, returns detailed info about each theme
            
        Returns:
            List of theme information dictionaries
        """
        url = f"{self.BASE_URL}/public/themesvc/getAllThemesInfo"
        params = {'moreInfo': 'Y' if more_info else 'N'}
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Theme_Names' in data:
                self.available_themes = data['Theme_Names']
                return data['Theme_Names']
            return []
        except Exception as e:
            print(f"Error getting themes info: {e}")
            return []
    
    def calculate_extents(self, lat: float, lon: float, radius_km: float = 5.0) -> str:
        """
        Calculate extents (bounding box) around a point.
        
        Args:
            lat: Center latitude
            lon: Center longitude
            radius_km: Radius in kilometers for the bounding box
            
        Returns:
            Extents string in format: "lat_min,lng_min,lat_max,lng_max"
        """
        # Approximate degrees per km (works for Singapore's latitude)
        # 1 degree latitude ≈ 111 km
        # 1 degree longitude ≈ 111 km * cos(latitude)
        import math
        
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
        
        lat_min = lat - lat_delta
        lat_max = lat + lat_delta
        lon_min = lon - lon_delta
        lon_max = lon + lon_delta
        
        return f"{lat_min},{lon_min},{lat_max},{lon_max}"
    
    def get_theme_data(self, query_name: str, lat: float = None, lon: float = None, 
                       extents: str = None, radius_km: float = 5.0) -> List[Dict]:
        """
        Get themed data (amenities) near a location.
        
        Args:
            query_name: Theme name (e.g., 'kindergartens', 'parks')
            lat: Latitude (optional if extents provided)
            lon: Longitude (optional if extents provided)
            extents: Boundary box as "lat_min,lng_min,lat_max,lng_max" (optional)
            radius_km: Radius for calculating extents if lat/lon provided (default 5km)
            
        Returns:
            List of amenities
        """
        url = f"{self.BASE_URL}/public/themesvc/retrieveTheme"
        params = {'queryName': query_name}
        
        # Use extents if provided, otherwise calculate from lat/lon
        if extents:
            params['extents'] = extents
        elif lat is not None and lon is not None:
            params['extents'] = self.calculate_extents(lat, lon, radius_km)
        else:
            raise ValueError("Either extents or lat/lon must be provided")
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'SrchResults' in data and data['SrchResults']:
                return data['SrchResults'][1:] if len(data['SrchResults']) > 1 else []
            return []
        except requests.exceptions.HTTPError as e:
            # Silently skip 404 errors (theme not available in API)
            if e.response.status_code == 404:
                return []
            # Show other HTTP errors
            print(f"Error getting theme data for {query_name}: {e}")
            return []
        except Exception as e:
            print(f"Error getting theme data for {query_name}: {e}")
            return []
    
    def get_planning_area(self, lat: float, lon: float) -> Dict:
        """
        Get planning area information for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Planning area information
        """
        url = f"{self.BASE_URL}/public/popapi/getPlanningarea"
        params = {
            'lat': lat,
            'lng': lon
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Silently skip 400/404 errors (location not in planning area database)
            if e.response.status_code in [400, 404]:
                return {}
            # Show other HTTP errors
            print(f"Error getting planning area: {e}")
            return {}
        except Exception as e:
            print(f"Error getting planning area: {e}")
            return {}
    
    def get_route(self, start_lat: float, start_lon: float, end_lat: float, end_lon: float, 
                  route_type: str = 'drive') -> Dict:
        """
        Get route information between two points.
        
        Args:
            start_lat: Start latitude
            start_lon: Start longitude
            end_lat: End latitude
            end_lon: End longitude
            route_type: Type of route (drive, walk, cycle, pt)
            
        Returns:
            Route information including distance
        """
        url = f"{self.BASE_URL}/public/routingsvc/route"
        params = {
            'start': f"{start_lat},{start_lon}",
            'end': f"{end_lat},{end_lon}",
            'routeType': route_type
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # Route API might not always be available, use straight-line distance
            return {}


class HouseAnalyzer:
    """Main class for analyzing house locations."""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the house analyzer.
        
        Args:
            email: Onemap API email (optional)
            password: Onemap API password (optional)
        """
        self.api = OneMapAPI(email=email, password=password)
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula.
        
        Args:
            lat1: First point latitude
            lon1: First point longitude
            lat2: Second point latitude
            lon2: Second point longitude
            
        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def analyze_house(self, latitude: float, longitude: float, max_results: int = 10, 
                      use_all_themes: bool = False, search_radius_km: float = 5.0) -> Dict:
        """
        Perform comprehensive analysis of a house location.
        
        Args:
            latitude: House latitude
            longitude: House longitude
            max_results: Maximum number of results per category
            use_all_themes: If True, fetch and use all available themes from API (100+)
            search_radius_km: Search radius in kilometers for extents calculation
            
        Returns:
            Dictionary containing all analysis results
        """
        results = {
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'address': {},
            'planning_area': {},
            'amenities': {},
            'transport': {},
            'summary': {}
        }
        
        print(f"\n{'='*80}")
        print(f"HDB HOUSE ANALYSIS REPORT")
        print(f"{'='*80}\n")
        
        # 1. Get address information
        print("🏠 Retrieving address information...")
        geocode_data = self.api.reverse_geocode(latitude, longitude)
        if geocode_data and 'GeocodeInfo' in geocode_data:
            geo_info = geocode_data['GeocodeInfo'][0] if geocode_data['GeocodeInfo'] else {}
            results['address'] = {
                'building': geo_info.get('BUILDINGNAME', 'N/A'),
                'block': geo_info.get('BLOCK', 'N/A'),
                'road': geo_info.get('ROAD', 'N/A'),
                'postal': geo_info.get('POSTALCODE', 'N/A'),
                'latitude': geo_info.get('LATITUDE', latitude),
                'longitude': geo_info.get('LONGITUDE', longitude)
            }
            
            print(f"   Building: {results['address']['building']}")
            print(f"   Block: {results['address']['block']}")
            print(f"   Road: {results['address']['road']}")
            print(f"   Postal Code: {results['address']['postal']}")
        
        # 2. Get planning area information
        print(f"\n📍 Retrieving planning area information...")
        planning_data = self.api.get_planning_area(latitude, longitude)
        if planning_data:
            results['planning_area'] = planning_data
            print(f"   Planning Area: {planning_data.get('pln_area_n', 'N/A')}")
        
        # 3. Search for amenities using themes
        print(f"\n🏢 Analyzing nearby amenities...")
        amenities_data = {}
        
        # Determine which themes to use
        if use_all_themes:
            print("   Fetching all available themes from Onemap API...")
            all_themes = self.api.get_all_themes_info(more_info=True)
            if all_themes:
                print(f"   Found {len(all_themes)} available themes!")
                themes_to_search = {theme['QUERYNAME']: theme['QUERYNAME'] for theme in all_themes}
            else:
                print("   Could not fetch themes, using default set")
                themes_to_search = self.api.THEMES
        else:
            themes_to_search = self.api.THEMES
        
        for amenity_name, theme_code in themes_to_search.items():
            print(f"   Searching for {amenity_name.replace('_', ' ').title()}...")
            theme_results = self.api.get_theme_data(theme_code, lat=latitude, lon=longitude, 
                                                    radius_km=search_radius_km)
            
            locations = []
            for item in theme_results[:max_results]:
                try:
                    item_lat = float(item.get('Lat') or item.get('LATITUDE') or item.get('LatLng', '').split(',')[0])
                    item_lon = float(item.get('Lng') or item.get('LONGITUDE') or item.get('LatLng', '').split(',')[1])
                    
                    distance = self.calculate_distance(latitude, longitude, item_lat, item_lon)
                    
                    location = {
                        'name': item.get('NAME') or item.get('name') or item.get('DESCRIPTION', 'Unknown'),
                        'address': item.get('ADDRESSPOSTALCODE') or item.get('ADDRESS', 'N/A'),
                        'latitude': item_lat,
                        'longitude': item_lon,
                        'distance_km': round(distance, 3),
                        'distance_m': round(distance * 1000, 0)
                    }
                    locations.append(location)
                except (ValueError, TypeError, IndexError, KeyError) as e:
                    continue
            
            # Sort by distance
            locations.sort(key=lambda x: x['distance_km'])
            if locations:  # Only add if we found results
                amenities_data[amenity_name] = locations
        
        results['amenities'] = amenities_data
        
        # 4. Search for MRT stations
        print(f"\n🚇 Searching for nearby MRT stations...")
        mrt_results = self.api.search_location("MRT")
        mrt_locations = []
        
        if mrt_results and 'results' in mrt_results:
            for station in mrt_results['results'][:50]:  # Check more MRT stations
                try:
                    station_lat = float(station.get('LATITUDE', 0))
                    station_lon = float(station.get('LONGITUDE', 0))
                    distance = self.calculate_distance(latitude, longitude, station_lat, station_lon)
                    
                    # Only include MRT stations within 5km
                    if distance <= 5.0:
                        mrt_locations.append({
                            'name': station.get('SEARCHVAL', 'Unknown MRT'),
                            'address': station.get('ADDRESS', 'N/A'),
                            'latitude': station_lat,
                            'longitude': station_lon,
                            'distance_km': round(distance, 3),
                            'distance_m': round(distance * 1000, 0)
                        })
                except (ValueError, TypeError) as e:
                    continue
        
        mrt_locations.sort(key=lambda x: x['distance_km'])
        results['transport']['mrt_stations'] = mrt_locations[:max_results]
        
        # 5. Search for bus stops
        print(f"🚌 Searching for nearby bus stops...")
        bus_results = self.api.search_location("Bus Stop")
        bus_locations = []
        
        if bus_results and 'results' in bus_results:
            for stop in bus_results['results'][:100]:  # Check many bus stops
                try:
                    stop_lat = float(stop.get('LATITUDE', 0))
                    stop_lon = float(stop.get('LONGITUDE', 0))
                    distance = self.calculate_distance(latitude, longitude, stop_lat, stop_lon)
                    
                    # Only include bus stops within 1km
                    if distance <= 1.0:
                        bus_locations.append({
                            'name': stop.get('SEARCHVAL', 'Unknown Bus Stop'),
                            'address': stop.get('ADDRESS', 'N/A'),
                            'latitude': stop_lat,
                            'longitude': stop_lon,
                            'distance_km': round(distance, 3),
                            'distance_m': round(distance * 1000, 0)
                        })
                except (ValueError, TypeError) as e:
                    continue
        
        bus_locations.sort(key=lambda x: x['distance_km'])
        results['transport']['bus_stops'] = bus_locations[:max_results]
        
        # 6. Search for major roads and expressways
        print(f"🛣️  Searching for major roads and expressways...")
        expressways = ['PIE', 'CTE', 'ECP', 'AYE', 'BKE', 'KPE', 'SLE', 'TPE', 'MCE', 'KJE']
        road_locations = []
        
        for expressway in expressways:
            eway_results = self.api.search_location(expressway)
            if eway_results and 'results' in eway_results:
                for road in eway_results['results'][:5]:
                    try:
                        road_lat = float(road.get('LATITUDE', 0))
                        road_lon = float(road.get('LONGITUDE', 0))
                        distance = self.calculate_distance(latitude, longitude, road_lat, road_lon)
                        
                        if distance <= 3.0:  # Within 3km
                            road_locations.append({
                                'name': road.get('SEARCHVAL', expressway),
                                'type': 'Expressway',
                                'latitude': road_lat,
                                'longitude': road_lon,
                                'distance_km': round(distance, 3),
                                'distance_m': round(distance * 1000, 0)
                            })
                    except (ValueError, TypeError) as e:
                        continue
        
        road_locations.sort(key=lambda x: x['distance_km'])
        results['transport']['major_roads'] = road_locations[:10]
        
        # Generate summary statistics
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict) -> Dict:
        """
        Generate summary statistics from analysis results.
        
        Args:
            results: Analysis results dictionary
            
        Returns:
            Summary statistics
        """
        summary = {
            'total_amenities_found': 0,
            'nearest_amenity': None,
            'nearest_mrt': None,
            'nearest_bus_stop': None,
            'nearest_major_road': None,
            'amenity_counts': {}
        }
        
        # Count amenities
        for amenity_type, locations in results['amenities'].items():
            count = len(locations)
            summary['total_amenities_found'] += count
            summary['amenity_counts'][amenity_type] = count
            
            if locations and (not summary['nearest_amenity'] or 
                            locations[0]['distance_km'] < summary['nearest_amenity']['distance_km']):
                summary['nearest_amenity'] = {
                    'type': amenity_type,
                    'name': locations[0]['name'],
                    'distance_km': locations[0]['distance_km']
                }
        
        # Nearest transport
        if results['transport'].get('mrt_stations'):
            summary['nearest_mrt'] = results['transport']['mrt_stations'][0]
        
        if results['transport'].get('bus_stops'):
            summary['nearest_bus_stop'] = results['transport']['bus_stops'][0]
        
        if results['transport'].get('major_roads'):
            summary['nearest_major_road'] = results['transport']['major_roads'][0]
        
        return summary
    
    def print_detailed_report(self, results: Dict):
        """
        Print a detailed analysis report.
        
        Args:
            results: Analysis results dictionary
        """
        print(f"\n{'='*80}")
        print(f"DETAILED ANALYSIS REPORT")
        print(f"{'='*80}\n")
        
        # Summary
        print("📊 SUMMARY")
        print("-" * 80)
        summary = results['summary']
        print(f"Total Amenities Found: {summary['total_amenities_found']}")
        
        if summary['nearest_amenity']:
            print(f"Nearest Amenity: {summary['nearest_amenity']['name']} "
                  f"({summary['nearest_amenity']['type'].replace('_', ' ').title()}) - "
                  f"{summary['nearest_amenity']['distance_km']:.3f} km")
        
        if summary['nearest_mrt']:
            print(f"Nearest MRT: {summary['nearest_mrt']['name']} - "
                  f"{summary['nearest_mrt']['distance_km']:.3f} km")
        
        if summary['nearest_bus_stop']:
            print(f"Nearest Bus Stop: {summary['nearest_bus_stop']['name']} - "
                  f"{summary['nearest_bus_stop']['distance_m']:.0f} m")
        
        if summary['nearest_major_road']:
            print(f"Nearest Major Road: {summary['nearest_major_road']['name']} - "
                  f"{summary['nearest_major_road']['distance_km']:.3f} km")
        
        # Amenities breakdown
        print(f"\n🏢 AMENITIES BREAKDOWN")
        print("-" * 80)
        for amenity_type, locations in results['amenities'].items():
            if locations:
                print(f"\n{amenity_type.replace('_', ' ').title()} ({len(locations)} found):")
                for i, loc in enumerate(locations[:5], 1):  # Show top 5
                    print(f"  {i}. {loc['name']}")
                    print(f"     Address: {loc['address']}")
                    print(f"     Distance: {loc['distance_km']:.3f} km ({loc['distance_m']:.0f} m)")
        
        # Transport details
        print(f"\n🚇 MRT STATIONS")
        print("-" * 80)
        if results['transport'].get('mrt_stations'):
            for i, mrt in enumerate(results['transport']['mrt_stations'][:10], 1):
                print(f"  {i}. {mrt['name']}")
                print(f"     Distance: {mrt['distance_km']:.3f} km ({mrt['distance_m']:.0f} m)")
        else:
            print("  No MRT stations found within 5 km")
        
        print(f"\n🚌 BUS STOPS")
        print("-" * 80)
        if results['transport'].get('bus_stops'):
            for i, bus in enumerate(results['transport']['bus_stops'][:10], 1):
                print(f"  {i}. {bus['name']}")
                print(f"     Distance: {bus['distance_km']:.3f} km ({bus['distance_m']:.0f} m)")
        else:
            print("  No bus stops found within 1 km")
        
        print(f"\n🛣️  MAJOR ROADS & EXPRESSWAYS")
        print("-" * 80)
        if results['transport'].get('major_roads'):
            for i, road in enumerate(results['transport']['major_roads'][:10], 1):
                print(f"  {i}. {road['name']} ({road['type']})")
                print(f"     Distance: {road['distance_km']:.3f} km ({road['distance_m']:.0f} m)")
        else:
            print("  No major roads found within 3 km")
        
        print(f"\n{'='*80}\n")
    
    def save_report_json(self, results: Dict, filename: str):
        """
        Save analysis results to JSON file.
        
        Args:
            results: Analysis results dictionary
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Report saved to: {filename}")


def main():
    """Main function to run the house analyzer."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='HDB House Analyzer using Onemap API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python house_analyzer.py 1.3521 103.8198
  python house_analyzer.py 1.3521 103.8198 --all-themes
  python house_analyzer.py 1.3521 103.8198 --radius 10
        """
    )
    parser.add_argument('latitude', type=float, nargs='?', help='Latitude of the house')
    parser.add_argument('longitude', type=float, nargs='?', help='Longitude of the house')
    parser.add_argument('--all-themes', action='store_true', 
                       help='Use all 100+ available themes from Onemap API (slower but more comprehensive)')
    parser.add_argument('--radius', type=float, default=5.0, 
                       help='Search radius in kilometers (default: 5.0)')
    parser.add_argument('--max-results', type=int, default=10,
                       help='Maximum results per category (default: 10)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("HDB HOUSE ANALYZER - Using Onemap API")
    print("="*80)
    
    # Check for API credentials
    email = os.getenv('ONEMAP_EMAIL')
    password = os.getenv('ONEMAP_PASSWORD')
    
    if not email or not password:
        print("\n🔐 Onemap API Authentication Required")
        print("-" * 80)
        print("The Onemap API requires authentication to access data.")
        print("If you don't have an account, register for FREE at:")
        print("https://www.onemap.gov.sg/apidocs/register")
        print("-" * 80)
        
        # Prompt for credentials
        try:
            if not email:
                email = input("\nEnter your Onemap email: ").strip()
            if not password:
                print("\n💡 Note: Your password will be hidden as you type (no characters will appear).")
                print("   This is normal for security. Just type your password and press Enter.")
                password = getpass.getpass("\nEnter your Onemap password: ").strip()
            
            if not email or not password:
                print("\n❌ Error: Email and password are required!")
                print("Please register at: https://www.onemap.gov.sg/apidocs/register")
                sys.exit(1)
                
            print("\n✓ Credentials received. Authenticating...")
        except KeyboardInterrupt:
            print("\n\n❌ Authentication cancelled by user.")
            sys.exit(1)
    
    # Get user input
    if args.latitude is not None and args.longitude is not None:
        latitude = args.latitude
        longitude = args.longitude
    else:
        print("\nPlease enter the house coordinates:")
        try:
            latitude = float(input("Latitude: "))
            longitude = float(input("Longitude: "))
        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")
            sys.exit(1)
    
    # Validate coordinates (Singapore bounds)
    if not (1.1 <= latitude <= 1.5 and 103.6 <= longitude <= 104.1):
        print(f"Warning: Coordinates ({latitude}, {longitude}) may be outside Singapore!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Show analysis mode
    if args.all_themes:
        print(f"\n🌟 Using ALL available themes from Onemap API (100+ categories)")
        print(f"   This will take longer but provide more comprehensive data.")
    else:
        print(f"\n📋 Using curated theme categories (faster, focused results)")
        print(f"   Use --all-themes flag to access 100+ theme categories")
    
    print(f"   Search radius: {args.radius} km")
    print(f"   Max results per category: {args.max_results}")
    
    # Perform analysis with credentials
    analyzer = HouseAnalyzer(email=email, password=password)
    results = analyzer.analyze_house(latitude, longitude, 
                                     max_results=args.max_results,
                                     use_all_themes=args.all_themes,
                                     search_radius_km=args.radius)
    
    # Print detailed report
    analyzer.print_detailed_report(results)
    
    # Ask if user wants to save the report
    save_report = input("\nDo you want to save the report as JSON? (y/n): ")
    if save_report.lower() == 'y':
        filename = input("Enter filename (default: house_analysis_report.json): ").strip()
        if not filename:
            filename = "house_analysis_report.json"
        if not filename.endswith('.json'):
            filename += '.json'
        analyzer.save_report_json(results, filename)
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
