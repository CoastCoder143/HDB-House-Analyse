#!/usr/bin/env python3
"""
Example usage of the HDB House Analyzer

This script demonstrates how to use the house_analyzer module
programmatically in your own Python code.

NOTE: Authentication options:
1. Interactive: Script prompts for credentials when run
2. Environment variables (for automation):
   export ONEMAP_EMAIL='your_email@example.com'
   export ONEMAP_PASSWORD='your_password'
3. Explicit credentials in code (see example_with_explicit_credentials)

See AUTHENTICATION.md for more details.
"""

import os
from house_analyzer import HouseAnalyzer, OneMapAPI

def example_basic_usage():
    """Basic usage example - uses environment variables or prompts."""
    print("Example 1: Basic Analysis")
    print("-" * 50)
    
    # Initialize the analyzer
    # If credentials are in environment variables, uses those
    # Otherwise, would prompt interactively (not suitable for scripts)
    analyzer = HouseAnalyzer()
    
    # Analyze a location (Orchard Road area)
    latitude = 1.3048
    longitude = 103.8318
    
    # Perform the analysis
    results = analyzer.analyze_house(latitude, longitude, max_results=5)
    
    # Access specific results
    print(f"\nAddress: {results['address'].get('road', 'N/A')}")
    print(f"Planning Area: {results['planning_area'].get('pln_area_n', 'N/A')}")
    
    # Show nearest MRT
    if results['transport'].get('mrt_stations'):
        nearest_mrt = results['transport']['mrt_stations'][0]
        print(f"Nearest MRT: {nearest_mrt['name']} ({nearest_mrt['distance_km']} km)")


def example_with_explicit_credentials():
    """Example using explicit credentials instead of environment variables."""
    print("\n\nExample 2: Explicit Credentials")
    print("-" * 50)
    
    # Option 1: Create API client with explicit credentials
    # WARNING: Never hard-code credentials in production!
    # This is just for demonstration.
    email = os.getenv('ONEMAP_EMAIL')  # Still get from env for safety
    password = os.getenv('ONEMAP_PASSWORD')
    
    if email and password:
        # Create authenticated API client
        api = OneMapAPI(email=email, password=password)
        
        # Create analyzer and use custom API client
        analyzer = HouseAnalyzer()
        analyzer.api = api
        
        # Now use the analyzer normally
        results = analyzer.analyze_house(1.3048, 103.8318, max_results=3)
        print(f"Analysis completed with explicit credentials")
        print(f"Found {results['summary']['total_amenities_found']} amenities")
    else:
        print("Credentials not found in environment variables")
        print("Set ONEMAP_EMAIL and ONEMAP_PASSWORD first")


def example_save_to_json():
    """Example of saving results to JSON."""
    print("\n\nExample 3: Save to JSON")
    print("-" * 50)
    
    analyzer = HouseAnalyzer()
    
    # Analyze Marina Bay area
    results = analyzer.analyze_house(1.2844, 103.8607, max_results=10)
    
    # Save to JSON file
    analyzer.save_report_json(results, "marina_bay_analysis.json")
    print("Results saved to marina_bay_analysis.json")


def example_compare_locations():
    """Example comparing multiple locations."""
    print("\n\nExample 4: Compare Multiple Locations")
    print("-" * 50)
    
    analyzer = HouseAnalyzer()
    
    locations = {
        'Orchard': (1.3048, 103.8318),
        'Jurong East': (1.3329, 103.7436),
        'Tampines': (1.3496, 103.9568)
    }
    
    for name, (lat, lon) in locations.items():
        print(f"\n{name}:")
        results = analyzer.analyze_house(lat, lon, max_results=3)
        
        summary = results['summary']
        print(f"  Total Amenities: {summary['total_amenities_found']}")
        
        if summary.get('nearest_mrt'):
            print(f"  Nearest MRT: {summary['nearest_mrt']['name']} "
                  f"({summary['nearest_mrt']['distance_km']:.2f} km)")


def example_custom_analysis():
    """Example of custom analysis focusing on specific amenities."""
    print("\n\nExample 5: Custom Analysis - Schools Only")
    print("-" * 50)
    
    analyzer = HouseAnalyzer()
    
    # Analyze Punggol area
    results = analyzer.analyze_house(1.4041, 103.9025, max_results=10)
    
    # Focus on schools
    schools = results['amenities'].get('registered_schools', [])
    kindergartens = results['amenities'].get('kindergartens', [])
    childcare = results['amenities'].get('childcare', [])
    
    print(f"\nEducational Facilities Analysis:")
    print(f"  Registered Schools: {len(schools)}")
    print(f"  Kindergartens: {len(kindergartens)}")
    print(f"  Childcare Centers: {len(childcare)}")
    
    if schools:
        print(f"\n  Nearest School: {schools[0]['name']}")
        print(f"  Distance: {schools[0]['distance_km']} km")


if __name__ == "__main__":
    print("="*50)
    print("HDB House Analyzer - Example Usage")
    print("="*50)
    print("\nNOTE: Ensure ONEMAP_EMAIL and ONEMAP_PASSWORD are set!")
    print("See AUTHENTICATION.md for setup instructions.\n")
    
    # Run all examples
    example_basic_usage()
    example_with_explicit_credentials()
    example_save_to_json()
    example_compare_locations()
    example_custom_analysis()
    
    print("\n" + "="*50)
    print("All examples completed!")
    print("="*50)
