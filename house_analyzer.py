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

# Import property insights engine
try:
    from property_insights import PropertyInsights
    INSIGHTS_AVAILABLE = True
except ImportError:
    INSIGHTS_AVAILABLE = False
    print("⚠️  Warning: property_insights module not found. Smart insights disabled.")


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
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, 
                 access_token: Optional[str] = None):
        """
        Initialize the Onemap API client.
        
        Args:
            email: Onemap API email (optional, can be set via environment variable ONEMAP_EMAIL)
            password: Onemap API password (optional, can be set via environment variable ONEMAP_PASSWORD)
            access_token: Pre-obtained access token (optional, can be set via environment variable ONEMAP_TOKEN)
                         If provided, skips authentication step
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HDB-House-Analyzer/1.0'
        })
        
        # Get credentials from parameters or environment variables
        self.email = email or os.getenv('ONEMAP_EMAIL')
        self.password = password or os.getenv('ONEMAP_PASSWORD')
        
        # Check for pre-obtained token
        provided_token = access_token or os.getenv('ONEMAP_TOKEN')
        
        self.access_token = None
        self.token_expiry = None
        self.available_themes = None  # Cache for available themes
        
        # If token provided, use it directly (skip authentication)
        if provided_token:
            self.access_token = provided_token
            # Set expiry to 3 days from now (default token validity)
            self.token_expiry = datetime.now() + timedelta(days=3)
            self.session.headers.update({
                'Authorization': self.access_token
            })
        # Otherwise, try to authenticate if credentials are provided
        elif self.email and self.password:
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
                
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️  Network error - Cannot reach Onemap authentication server")
            print(f"   Please check your internet connection.")
            print(f"   Make sure you can access: {self.AUTH_URL}")
            return False
        except requests.exceptions.Timeout:
            print(f"⚠️  Authentication timeout - Server not responding")
            return False
        except Exception as e:
            print(f"Error during authentication: {e}")
            return False
        
        return False
    
    def check_connectivity(self) -> bool:
        """
        Check if we can reach the Onemap API server.
        
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            # Try a simple request to check connectivity
            response = requests.get(f"{self.BASE_URL}/public/ping", timeout=5)
            return True
        except requests.exceptions.ConnectionError:
            print("⚠️  Cannot reach Onemap API server (www.onemap.gov.sg)")
            print("   Possible causes:")
            print("   1. No internet connection")
            print("   2. Firewall blocking access")
            print("   3. DNS resolution failure")
            print("   ")
            print("   Please ensure you have internet access and try again.")
            return False
        except requests.exceptions.Timeout:
            print("⚠️  Onemap API server timeout")
            return False
        except Exception as e:
            print(f"⚠️  Connectivity check failed: {e}")
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
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️  Network error - Cannot reach Onemap API server")
            print(f"   Please check your internet connection and try again.")
            return {}
        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout - Onemap API server not responding")
            return {}
        except Exception as e:
            print(f"Error in location search: {e}")
            return {}
    
    def get_nearest_mrt_stops(self, lat: float, lon: float, radius_m: int = 5000) -> List[Dict]:
        """
        Get nearest MRT/LRT stations within specified radius using Nearby Services API.
        
        Args:
            lat: Latitude (WGS84 format)
            lon: Longitude (WGS84 format)
            radius_m: Search radius in meters (max 5000, default 5000)
            
        Returns:
            List of MRT/LRT stations with id, name, lat, lon, road
        """
        url = f"{self.BASE_URL}/public/nearbysvc/getNearestMrtStops"
        params = {
            'latitude': lat,
            'longitude': lon,
            'radius_in_meters': min(radius_m, 5000)  # Max 5000m per API spec
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()  # Returns list directly
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️  Network error - Cannot reach Onemap API server")
            print(f"   Please check your internet connection and try again.")
            return []
        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout - Onemap API server not responding")
            return []
        except Exception as e:
            print(f"Error getting nearest MRT stops: {e}")
            return []
    
    def get_nearest_bus_stops(self, lat: float, lon: float, radius_m: int = 1000) -> List[Dict]:
        """
        Get nearest bus stops within specified radius using Nearby Services API.
        
        Args:
            lat: Latitude (WGS84 format)
            lon: Longitude (WGS84 format)
            radius_m: Search radius in meters (max 5000, default 1000)
            
        Returns:
            List of bus stops with id, name, lat, lon, road
        """
        url = f"{self.BASE_URL}/public/nearbysvc/getNearestBusStops"
        params = {
            'latitude': lat,
            'longitude': lon,
            'radius_in_meters': min(radius_m, 5000)  # Max 5000m per API spec
        }
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()  # Returns list directly
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️  Network error - Cannot reach Onemap API server")
            print(f"   Please check your internet connection and try again.")
            print(f"   Error: {e}")
            return []
        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout - Onemap API server not responding")
            return []
        except Exception as e:
            print(f"Error getting nearest bus stops: {e}")
            return []
    
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
                  route_type: str = 'drive', date: Optional[str] = None, time: Optional[str] = None,
                  mode: Optional[str] = None, max_walk_distance: Optional[int] = None,
                  num_itineraries: Optional[int] = None) -> Dict:
        """
        Get route information between two points.
        
        Args:
            start_lat: Start latitude (WGS84)
            start_lon: Start longitude (WGS84)
            end_lat: End latitude (WGS84)
            end_lon: End longitude (WGS84)
            route_type: Type of route - 'drive', 'walk', 'cycle', or 'pt' (public transport)
            date: For PT mode - Date in MM-DD-YYYY format (required if route_type='pt')
            time: For PT mode - Time in HH:MM:SS format, 24-hour clock (required if route_type='pt')
            mode: For PT mode - 'transit', 'bus', or 'rail' (required if route_type='pt')
            max_walk_distance: For PT mode - Maximum walking distance in meters (optional)
            num_itineraries: For PT mode - Number of results to return, 1-3 (optional)
            
        Returns:
            Route information including distance and time
            
        Example:
            # Simple drive route
            route = api.get_route(1.3521, 103.8198, 1.2844, 103.8607, route_type='drive')
            
            # Public transport route
            route = api.get_route(
                1.3521, 103.8198, 1.2844, 103.8607, 
                route_type='pt',
                date='02-11-2026',
                time='08:30:00',
                mode='transit',
                max_walk_distance=1000,
                num_itineraries=3
            )
        """
        url = f"{self.BASE_URL}/public/routingsvc/route"
        params = {
            'start': f"{start_lat},{start_lon}",
            'end': f"{end_lat},{end_lon}",
            'routeType': route_type
        }
        
        # Add PT-specific parameters if route_type is 'pt'
        if route_type.lower() == 'pt':
            # PT mode requires date, time, and mode
            if date:
                params['date'] = date
            if time:
                params['time'] = time
            if mode:
                params['mode'] = mode.upper()  # API expects uppercase (TRANSIT, BUS, RAIL)
            
            # Optional PT parameters
            if max_walk_distance is not None:
                params['maxWalkDistance'] = str(max_walk_distance)
            if num_itineraries is not None:
                params['numItineraries'] = str(num_itineraries)
        
        try:
            response = self._make_authenticated_request('GET', url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # No route found
                return {'error': 'No route found between specified locations'}
            else:
                return {'error': f'API error: {str(e)}'}
        except Exception as e:
            # Route API might not always be available
            return {'error': f'Route calculation failed: {str(e)}'}
    
    @staticmethod
    def format_route_time(seconds: int) -> str:
        """
        Format route time from seconds to human-readable format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string (e.g., "15 mins", "1h 30m")
        """
        if seconds < 60:
            return f"{seconds} sec"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} min{'s' if minutes > 1 else ''}"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{hours}h"
    
    @staticmethod
    def format_route_distance(meters: float) -> str:
        """
        Format route distance from meters to human-readable format.
        
        Args:
            meters: Distance in meters
            
        Returns:
            Formatted distance string (e.g., "500m", "2.5km")
        """
        if meters < 1000:
            return f"{int(meters)}m"
        else:
            km = meters / 1000
            return f"{km:.1f}km"


class HouseAnalyzer:
    """Main class for analyzing house locations."""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, 
                 access_token: Optional[str] = None):
        """
        Initialize the house analyzer.
        
        Args:
            email: Onemap API email (optional)
            password: Onemap API password (optional)
            access_token: Pre-obtained access token (optional)
        """
        self.api = OneMapAPI(email=email, password=password, access_token=access_token)
    
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
            'public_transport': {},
            'roads': {},
            'summary': {}
        }
        
        print(f"\n{'='*80}")
        print(f"HDB HOUSE ANALYSIS REPORT")
        print(f"{'='*80}\n")
        
        # Check connectivity first
        print("🔍 Checking connectivity to Onemap API...")
        if not self.api.check_connectivity():
            print("\n" + "="*80)
            print("❌ ANALYSIS CANNOT PROCEED")
            print("="*80)
            print("\nThe analyzer requires internet access to:")
            print("  • www.onemap.gov.sg (Singapore Government API)")
            print("\nPlease:")
            print("  1. Check your internet connection")
            print("  2. Ensure firewall allows HTTPS to www.onemap.gov.sg")
            print("  3. Try again once connected")
            print("\nFor offline testing, consider using mock data or cached results.")
            return results
        print("✅ Connection OK\n")
        
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
        
        # 4. Search for MRT stations using Nearby Services API
        print(f"\n🚇 Searching for nearby MRT stations...")
        mrt_results = self.api.get_nearest_mrt_stops(latitude, longitude, radius_m=5000)
        mrt_locations = []
        
        for station in mrt_results:
            try:
                station_lat = float(station.get('lat', 0))
                station_lon = float(station.get('lon', 0))
                distance = self.calculate_distance(latitude, longitude, station_lat, station_lon)
                
                mrt_locations.append({
                    'name': station.get('name', 'Unknown MRT'),
                    'id': station.get('id', 'N/A'),
                    'road': station.get('road', 'N/A'),
                    'latitude': station_lat,
                    'longitude': station_lon,
                    'distance_km': round(distance, 3),
                    'distance_m': round(distance * 1000, 0)
                })
            except (ValueError, TypeError) as e:
                continue
        
        mrt_locations.sort(key=lambda x: x['distance_km'])
        results['public_transport']['mrt_stations'] = mrt_locations[:max_results]
        
        # 5. Search for bus stops using Nearby Services API
        print(f"🚌 Searching for nearby bus stops...")
        bus_results = self.api.get_nearest_bus_stops(latitude, longitude, radius_m=1000)
        bus_locations = []
        
        for stop in bus_results:
            try:
                stop_lat = float(stop.get('lat', 0))
                stop_lon = float(stop.get('lon', 0))
                distance = self.calculate_distance(latitude, longitude, stop_lat, stop_lon)
                
                bus_locations.append({
                    'name': stop.get('name', 'Unknown Bus Stop'),
                    'id': stop.get('id', 'N/A'),
                    'road': stop.get('road', 'N/A'),
                    'latitude': stop_lat,
                    'longitude': stop_lon,
                    'distance_km': round(distance, 3),
                    'distance_m': round(distance * 1000, 0)
                })
            except (ValueError, TypeError) as e:
                continue
        
        bus_locations.sort(key=lambda x: x['distance_km'])
        results['public_transport']['bus_stops'] = bus_locations[:max_results]
        
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
        results['roads']['expressways'] = road_locations[:10]
        
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
        if results['public_transport'].get('mrt_stations'):
            summary['nearest_mrt'] = results['public_transport']['mrt_stations'][0]
        
        if results['public_transport'].get('bus_stops'):
            summary['nearest_bus_stop'] = results['public_transport']['bus_stops'][0]
        
        if results['roads'].get('expressways'):
            summary['nearest_major_road'] = results['roads']['expressways'][0]
        
        return summary
    
    def print_detailed_report(self, results: Dict):
        """
        Print a detailed analysis report with smart property insights.
        
        Args:
            results: Analysis results dictionary
        """
        print(f"\n{'='*80}")
        print(f"🏠 SMART PROPERTY ANALYSIS REPORT 🔍")
        print(f"{'='*80}\n")
        
        # Generate smart insights if available
        if INSIGHTS_AVAILABLE:
            insights_engine = PropertyInsights()
            scores = insights_engine.calculate_livability_score(results)
            smart_insights = insights_engine.generate_smart_insights(results, scores)
            property_profile = insights_engine.generate_property_profile(results, scores)
            
            # EXECUTIVE SUMMARY (Property Agent Style)
            print("🎯 EXECUTIVE SUMMARY - Property Agent Analysis")
            print("=" * 80)
            overall_score = scores['overall']
            grade = insights_engine.get_grade_from_score(overall_score)
            emoji = insights_engine.get_score_emoji(overall_score)
            
            print(f"\n{emoji} OVERALL LIVABILITY SCORE: {overall_score:.1f}/100 (Grade: {grade})")
            print(f"\nScore Breakdown:")
            print(f"  🚇🚌 Public Transport: {scores['public_transport']:.1f}/20  {insights_engine.get_score_emoji(scores['public_transport']*5)}")
            print(f"  🎓 Education:         {scores['education']:.1f}/20  {insights_engine.get_score_emoji(scores['education']*5)}")
            print(f"  🏥 Healthcare:        {scores['healthcare']:.1f}/15  {insights_engine.get_score_emoji(scores['healthcare']*6.67)}")
            print(f"  🛒 Shopping:          {scores['shopping']:.1f}/20  {insights_engine.get_score_emoji(scores['shopping']*5)}")
            print(f"  🌳 Recreation:        {scores['recreation']:.1f}/10  {insights_engine.get_score_emoji(scores['recreation']*10)}")
            print(f"  🛡️  Safety:            {scores['safety']:.1f}/10  {insights_engine.get_score_emoji(scores['safety']*10)}")
            print(f"  🛣️  Roads & Access:    {scores['roads']:.1f}/5   {insights_engine.get_score_emoji(scores['roads']*20)}")
            
            print(f"\n💡 SMART INSIGHTS - What Smart Agents Notice:")
            print("-" * 80)
            for insight in smart_insights:
                print(f"  {insight}")
            
            print(f"\n👥 IDEAL FOR:")
            print("-" * 80)
            if property_profile['ideal_for']:
                for demographic in property_profile['ideal_for']:
                    print(f"  ✓ {demographic}")
            else:
                print(f"  • General buyers/renters")
            
            print(f"\n🌟 KEY SELLING POINTS:")
            print("-" * 80)
            if property_profile['selling_points']:
                for point in property_profile['selling_points']:
                    print(f"  • {point}")
            else:
                print(f"  • Basic amenities available")
            
            if property_profile['concerns']:
                print(f"\n⚠️  AREAS TO CONSIDER:")
                print("-" * 80)
                for concern in property_profile['concerns']:
                    print(f"  • {concern}")
            
            print(f"\n💰 INVESTMENT INSIGHTS:")
            print("-" * 80)
            print(f"  Investment Potential: {property_profile['investment_potential']}")
            print(f"  Rental Attractiveness: {property_profile['rental_attractiveness']}")
            
            print(f"\n{'='*80}\n")
        
        # Regular Summary
        print("📊 DETAILED BREAKDOWN")
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
        
        # Public Transport details
        print(f"\n🚇🚌 PUBLIC TRANSPORT")
        print("-" * 80)
        print(f"\n🚇 MRT Stations:")
        if results['public_transport'].get('mrt_stations'):
            for i, mrt in enumerate(results['public_transport']['mrt_stations'][:10], 1):
                print(f"  {i}. {mrt['name']}")
                print(f"     Distance: {mrt['distance_km']:.3f} km ({mrt['distance_m']:.0f} m)")
        else:
            print("  No MRT stations found within 5 km")
        
        print(f"\n🚌 Bus Stops:")
        if results['public_transport'].get('bus_stops'):
            for i, bus in enumerate(results['public_transport']['bus_stops'][:10], 1):
                print(f"  {i}. {bus['name']}")
                print(f"     Distance: {bus['distance_km']:.3f} km ({bus['distance_m']:.0f} m)")
        else:
            print("  No bus stops found within 1 km")
        
        # Roads details
        print(f"\n🛣️  ROADS & EXPRESSWAYS")
        print("-" * 80)
        if results['roads'].get('expressways'):
            for i, road in enumerate(results['roads']['expressways'][:10], 1):
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
    
    def save_report_csv(self, results: Dict, filename: str):
        """
        Save analysis results to CSV file.
        
        Args:
            results: Analysis results dictionary
            filename: Output filename
        """
        import csv
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Category', 'Name', 'Distance (km)', 'Distance (m)', 'Details'])
            
            # Write location info
            writer.writerow(['Location', results.get('address', 'Unknown'), '', '', 
                           f"Lat: {results.get('latitude')}, Lon: {results.get('longitude')}"])
            writer.writerow([])  # Empty row
            
            # Write MRT stations
            writer.writerow(['PUBLIC TRANSPORT - MRT STATIONS'])
            for mrt in results['public_transport'].get('mrt_stations', []):
                writer.writerow(['MRT', mrt['name'], f"{mrt['distance_km']:.3f}", 
                               mrt['distance_m'], mrt.get('id', '')])
            writer.writerow([])
            
            # Write bus stops
            writer.writerow(['PUBLIC TRANSPORT - BUS STOPS'])
            for bus in results['public_transport'].get('bus_stops', []):
                writer.writerow(['Bus Stop', bus['name'], f"{bus['distance_km']:.3f}", 
                               bus['distance_m'], bus.get('id', '')])
            writer.writerow([])
            
            # Write roads
            writer.writerow(['ROADS & EXPRESSWAYS'])
            for road in results['roads'].get('expressways', []):
                writer.writerow(['Road', road['name'], f"{road['distance_km']:.3f}", 
                               road['distance_m'], ''])
            writer.writerow([])
            
            # Write amenities
            for amenity_type, locations in results['amenities'].items():
                if locations:
                    writer.writerow([f'AMENITY - {amenity_type.upper().replace("_", " ")}'])
                    for loc in locations:
                        writer.writerow([amenity_type, loc['name'], f"{loc['distance_km']:.3f}", 
                                       loc['distance_m'], loc.get('address', '')])
                    writer.writerow([])
            
        print(f"📊 CSV report saved to: {filename}")
    
    def save_report_markdown(self, results: Dict, filename: str):
        """
        Save analysis results to Markdown file.
        
        Args:
            results: Analysis results dictionary
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            # Title
            f.write("# 🏠 HDB House Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Location
            f.write("## 📍 Location Information\n\n")
            f.write(f"**Address:** {results.get('address', 'Unknown')}\n\n")
            f.write(f"**Coordinates:** {results.get('latitude')}, {results.get('longitude')}\n\n")
            if results.get('planning_area'):
                f.write(f"**Planning Area:** {results['planning_area'].get('pln_area_n', 'Unknown')}\n\n")
            
            # Summary
            if 'summary' in results:
                f.write("## 📊 Summary\n\n")
                summary = results['summary']
                f.write(f"- **Total Amenities Found:** {summary.get('total_amenities_found', 0)}\n")
                if summary.get('nearest_mrt'):
                    mrt = summary['nearest_mrt']
                    f.write(f"- **Nearest MRT:** {mrt['name']} ({mrt['distance_km']:.2f} km)\n")
                if summary.get('nearest_bus_stop'):
                    bus = summary['nearest_bus_stop']
                    f.write(f"- **Nearest Bus Stop:** {bus['name']} ({bus['distance_km']:.2f} km)\n")
                f.write("\n")
            
            # Public Transport
            f.write("## 🚇🚌 Public Transport\n\n")
            f.write("### MRT Stations\n\n")
            f.write("| Name | Distance | ID |\n")
            f.write("|------|----------|----|\n")
            for mrt in results['public_transport'].get('mrt_stations', [])[:10]:
                f.write(f"| {mrt['name']} | {mrt['distance_km']:.2f} km | {mrt.get('id', 'N/A')} |\n")
            f.write("\n")
            
            f.write("### Bus Stops\n\n")
            f.write("| Name | Distance | ID |\n")
            f.write("|------|----------|----|\n")
            for bus in results['public_transport'].get('bus_stops', [])[:10]:
                f.write(f"| {bus['name']} | {bus['distance_km']:.2f} km | {bus.get('id', 'N/A')} |\n")
            f.write("\n")
            
            # Roads
            f.write("## 🛣️ Roads & Expressways\n\n")
            f.write("| Name | Distance |\n")
            f.write("|------|----------|\n")
            for road in results['roads'].get('expressways', [])[:10]:
                f.write(f"| {road['name']} | {road['distance_km']:.2f} km |\n")
            f.write("\n")
            
            # Amenities
            f.write("## 🏢 Nearby Amenities\n\n")
            for amenity_type, locations in results['amenities'].items():
                if locations:
                    f.write(f"### {amenity_type.replace('_', ' ').title()}\n\n")
                    f.write("| Name | Distance | Address |\n")
                    f.write("|------|----------|----------|\n")
                    for loc in locations[:10]:
                        address = loc.get('address', 'N/A')
                        f.write(f"| {loc['name']} | {loc['distance_km']:.2f} km | {address} |\n")
                    f.write("\n")
            
        print(f"📝 Markdown report saved to: {filename}")


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
  python house_analyzer.py 1.3521 103.8198 --token "eyJhbGc..."
  python house_analyzer.py 1.3521 103.8198 --output report.json
  python house_analyzer.py 1.3521 103.8198 --output report.csv --format csv
  python house_analyzer.py 1.3521 103.8198 --output report.md --format markdown
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
    parser.add_argument('--token', type=str, default=None,
                       help='Pre-obtained Onemap API access token (skips authentication)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output file path (auto-generates if not specified)')
    parser.add_argument('--format', '-f', type=str, default='json',
                       choices=['json', 'csv', 'markdown', 'md', 'all'],
                       help='Output format: json, csv, markdown/md, or all (default: json)')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Disable interactive prompts (automatically saves output)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("🏠 SMART PROPERTY AGENT - HDB House Analyzer 🔍")
    print("Using Onemap API with Intelligent Insights & Recommendations")
    print("="*80)
    
    # Check for pre-obtained token first
    token = args.token or os.getenv('ONEMAP_TOKEN')
    
    # Only prompt for credentials if no token provided
    email = os.getenv('ONEMAP_EMAIL')
    password = os.getenv('ONEMAP_PASSWORD')
    
    if not token and (not email or not password):
        print("\n🔐 Onemap API Authentication Required")
        print("-" * 80)
        print("The Onemap API requires authentication to access data.")
        print("If you don't have an account, register for FREE at:")
        print("https://www.onemap.gov.sg/apidocs/register")
        print("-" * 80)
        print("\nYou can authenticate in two ways:")
        print("1. Email & Password (recommended)")
        print("2. Pre-obtained access token (advanced)")
        print("-" * 80)
        
        # Prompt for credentials
        try:
            if not email:
                email = input("\nEnter your Onemap email (or press Enter to use token): ").strip()
            
            # If user chose token option
            if not email:
                token = input("Enter your access token: ").strip()
                if not token:
                    print("\n❌ Error: Either email/password or token is required!")
                    print("Please register at: https://www.onemap.gov.sg/apidocs/register")
                    sys.exit(1)
            else:
                # Get password
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
    elif token:
        print("\n✓ Using pre-obtained access token...")
    else:
        print("\n✓ Credentials found. Authenticating...")
    
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
        print(f"\n🌟 SMART PROPERTY AGENT MODE - Using ALL 100+ Onemap themes")
        print(f"   🔍 Comprehensive analysis with smart insights & recommendations")
        print(f"   ⏱️  This will take longer but provides the best property intelligence")
    else:
        print(f"\n📋 STANDARD MODE - Using curated theme categories (faster)")
        print(f"   💡 TIP: Use --all-themes for smartest property agent analysis!")
        print(f"   🌟 Get livability scores, investment insights & hidden value factors")
    
    print(f"   🎯 Search radius: {args.radius} km")
    print(f"   📊 Max results per category: {args.max_results}")
    print(f"\n{'='*80}")
    
    # Perform analysis with credentials or token
    analyzer = HouseAnalyzer(email=email, password=password, access_token=token)
    results = analyzer.analyze_house(latitude, longitude, 
                                     max_results=args.max_results,
                                     use_all_themes=args.all_themes,
                                     search_radius_km=args.radius)
    
    # Print detailed report
    analyzer.print_detailed_report(results)
    
    # Handle output file generation
    output_file = args.output
    output_format = args.format
    
    # Auto-generate filename if output requested but no filename specified
    if args.no_interactive or output_file:
        if not output_file:
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            lat_str = f"{latitude:.4f}".replace('.', '_')
            lon_str = f"{longitude:.4f}".replace('.', '_')
            base_name = f"house_analysis_{lat_str}_{lon_str}_{timestamp}"
            
            if output_format == 'all':
                output_file = base_name  # Base name for multiple files
            elif output_format in ['markdown', 'md']:
                output_file = f"{base_name}.md"
            elif output_format == 'csv':
                output_file = f"{base_name}.csv"
            else:  # json
                output_file = f"{base_name}.json"
        
        print(f"\n💾 Saving analysis results...")
        print("=" * 80)
        
        # Save in requested format(s)
        if output_format == 'all':
            # Save in all formats
            base = output_file.rsplit('.', 1)[0] if '.' in output_file else output_file
            analyzer.save_report_json(results, f"{base}.json")
            analyzer.save_report_csv(results, f"{base}.csv")
            analyzer.save_report_markdown(results, f"{base}.md")
        elif output_format in ['markdown', 'md']:
            if not output_file.endswith('.md'):
                output_file = output_file.rsplit('.', 1)[0] + '.md'
            analyzer.save_report_markdown(results, output_file)
        elif output_format == 'csv':
            if not output_file.endswith('.csv'):
                output_file = output_file.rsplit('.', 1)[0] + '.csv'
            analyzer.save_report_csv(results, output_file)
        else:  # json (default)
            if not output_file.endswith('.json'):
                output_file = output_file.rsplit('.', 1)[0] + '.json'
            analyzer.save_report_json(results, output_file)
        
        print("=" * 80)
    else:
        # Interactive mode - ask if user wants to save
        save_report = input("\n💾 Do you want to save the report? (y/n): ")
        if save_report.lower() == 'y':
            # Ask for format
            print("\nAvailable formats:")
            print("  1. JSON (complete data structure)")
            print("  2. CSV (tabular format)")
            print("  3. Markdown (formatted report)")
            print("  4. All formats")
            format_choice = input("Choose format (1-4, default=1): ").strip() or '1'
            
            format_map = {
                '1': 'json',
                '2': 'csv',
                '3': 'markdown',
                '4': 'all'
            }
            output_format = format_map.get(format_choice, 'json')
            
            filename = input("Enter filename (or press Enter for auto-generated): ").strip()
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                lat_str = f"{latitude:.4f}".replace('.', '_')
                lon_str = f"{longitude:.4f}".replace('.', '_')
                filename = f"house_analysis_{lat_str}_{lon_str}_{timestamp}"
            
            print(f"\n💾 Saving analysis results...")
            print("=" * 80)
            
            if output_format == 'all':
                base = filename.rsplit('.', 1)[0] if '.' in filename else filename
                analyzer.save_report_json(results, f"{base}.json")
                analyzer.save_report_csv(results, f"{base}.csv")
                analyzer.save_report_markdown(results, f"{base}.md")
            elif output_format == 'markdown':
                if not filename.endswith('.md'):
                    filename += '.md'
                analyzer.save_report_markdown(results, filename)
            elif output_format == 'csv':
                if not filename.endswith('.csv'):
                    filename += '.csv'
                analyzer.save_report_csv(results, filename)
            else:  # json
                if not filename.endswith('.json'):
                    filename += '.json'
                analyzer.save_report_json(results, filename)
            
            print("=" * 80)
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
