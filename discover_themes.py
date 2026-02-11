#!/usr/bin/env python3
"""
Theme Discovery Script
Discovers all available Onemap themes by calling the live API
and documenting what data each theme provides.
"""

import json
import sys
import time
from datetime import datetime
from house_analyzer import OneMapAPI

def discover_all_themes():
    """Discover all available themes from Onemap API"""
    print("="*80)
    print("ONEMAP THEME DISCOVERY")
    print("="*80)
    print()
    
    # Initialize API
    print("🔐 Initializing Onemap API...")
    api = OneMapAPI()
    
    # Get all themes
    print("📋 Fetching all available themes...")
    themes_data = api.get_all_themes_info(more_info=True)
    
    if not themes_data or 'Theme_Names' not in themes_data:
        print("❌ Failed to retrieve themes")
        return
    
    themes = themes_data['Theme_Names']
    print(f"✅ Found {len(themes)} themes!")
    print()
    
    # Sample location (Bishan)
    test_lat = 1.3521
    test_lon = 103.8198
    extents = api.calculate_extents(test_lat, test_lon, radius_km=5.0)
    
    print(f"📍 Testing with location: Bishan ({test_lat}, {test_lon})")
    print(f"   Search area (extents): {extents}")
    print()
    
    # Results storage
    results = {
        'discovery_date': datetime.now().isoformat(),
        'total_themes': len(themes),
        'test_location': {'lat': test_lat, 'lon': test_lon, 'name': 'Bishan'},
        'themes': []
    }
    
    # Test each theme
    print("🔍 Testing each theme...")
    print("-" * 80)
    
    working_themes = 0
    failed_themes = 0
    
    for i, theme in enumerate(themes, 1):
        theme_name = theme.get('THEMENAME', 'Unknown')
        query_name = theme.get('QUERYNAME', '')
        category = theme.get('CATEGORY', 'Uncategorized')
        owner = theme.get('THEME_OWNER', 'Unknown')
        
        print(f"\n[{i}/{len(themes)}] Testing: {theme_name}")
        print(f"    Query: {query_name}")
        print(f"    Category: {category}")
        print(f"    Owner: {owner}")
        
        theme_result = {
            'theme_name': theme_name,
            'query_name': query_name,
            'category': category,
            'owner': owner,
            'icon': theme.get('ICON', ''),
            'expiry_date': theme.get('EXPIRY_DATE', ''),
            'published_date': theme.get('PUBLISHED_DATE', ''),
            'status': 'unknown',
            'data': None,
            'sample_fields': [],
            'feature_count': 0
        }
        
        try:
            # Try to get theme data
            theme_data = api.get_theme_data(query_name, test_lat, test_lon, extents)
            
            if theme_data and len(theme_data) > 0:
                theme_result['status'] = 'working'
                theme_result['feature_count'] = len(theme_data)
                
                # Get sample fields from first result
                if len(theme_data) > 0:
                    first_item = theme_data[0]
                    theme_result['sample_fields'] = list(first_item.keys())
                    # Store first item as sample (limit size)
                    theme_result['data'] = theme_data[0] if len(str(theme_data[0])) < 1000 else {'note': 'Data too large, not stored'}
                
                working_themes += 1
                print(f"    ✅ Working! Found {len(theme_data)} features")
                print(f"       Fields: {', '.join(theme_result['sample_fields'][:10])}")
                if len(theme_result['sample_fields']) > 10:
                    print(f"       ... and {len(theme_result['sample_fields']) - 10} more")
            else:
                theme_result['status'] = 'no_data'
                print(f"    ⚠️  No data found at test location")
        except Exception as e:
            theme_result['status'] = 'error'
            theme_result['error'] = str(e)
            failed_themes += 1
            print(f"    ❌ Error: {str(e)[:100]}")
        
        results['themes'].append(theme_result)
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    print()
    print("="*80)
    print("DISCOVERY SUMMARY")
    print("="*80)
    print(f"Total themes tested: {len(themes)}")
    print(f"Working themes: {working_themes}")
    print(f"No data at location: {len([t for t in results['themes'] if t['status'] == 'no_data'])}")
    print(f"Failed/Error: {failed_themes}")
    print()
    
    # Save results
    output_file = 'discovered_themes.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {output_file}")
    print()
    
    # Print summary by category
    print("THEMES BY CATEGORY:")
    print("-" * 80)
    categories = {}
    for theme in results['themes']:
        cat = theme['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'working': 0}
        categories[cat]['total'] += 1
        if theme['status'] == 'working':
            categories[cat]['working'] += 1
    
    for cat, counts in sorted(categories.items()):
        print(f"{cat:30} - {counts['working']:3}/{counts['total']:3} working")
    
    print()
    print("✅ Discovery complete!")
    
    return results

if __name__ == '__main__':
    try:
        results = discover_all_themes()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Discovery failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
