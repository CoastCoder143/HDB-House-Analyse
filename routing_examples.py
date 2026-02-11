#!/usr/bin/env python3
"""
Routing Examples - Onemap API Integration
==========================================

This script demonstrates how to use the enhanced routing capabilities
of the HDB House Analyzer, including public transport routing.

Features:
- Drive, walk, cycle routes
- Public transport routing with date/time
- Multiple PT options (transit, bus, rail)
- Human-readable time and distance formatting
"""

from house_analyzer import OneMapAPI
from datetime import datetime, timedelta


def example_1_drive_route():
    """Example 1: Simple driving route between two locations."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Drive Route from Bishan to Marina Bay")
    print("="*80)
    
    # Initialize API (uses environment variables or prompts)
    api = OneMapAPI()
    
    # Calculate drive route
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,  # Bishan
        end_lat=1.2844, end_lon=103.8607,      # Marina Bay
        route_type='drive'
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
    else:
        # Extract route summary
        summary = route.get('route_summary', {})
        distance = summary.get('total_distance', 0)
        time_sec = summary.get('total_time', 0)
        
        # Format for display
        time_str = OneMapAPI.format_route_time(time_sec)
        dist_str = OneMapAPI.format_route_distance(distance)
        
        print(f"✅ Route found!")
        print(f"   Distance: {dist_str}")
        print(f"   Estimated time: {time_str}")


def example_2_walk_route():
    """Example 2: Walking route to nearby location."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Walking Route to Nearby Park")
    print("="*80)
    
    api = OneMapAPI()
    
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,  # Bishan
        end_lat=1.3550, end_lon=103.8250,       # Bishan Park (approx)
        route_type='walk'
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
    else:
        summary = route.get('route_summary', {})
        distance = summary.get('total_distance', 0)
        time_sec = summary.get('total_time', 0)
        
        time_str = OneMapAPI.format_route_time(time_sec)
        dist_str = OneMapAPI.format_route_distance(distance)
        
        print(f"✅ Walking route found!")
        print(f"   Distance: {dist_str}")
        print(f"   Walking time: {time_str}")


def example_3_pt_morning_commute():
    """Example 3: Public transport route for morning commute."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Morning Commute via Public Transport")
    print("="*80)
    
    api = OneMapAPI()
    
    # Get tomorrow's date for the route
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%m-%d-%Y')
    
    print(f"📅 Planning route for: {date_str} at 08:30:00")
    print(f"🚇 Mode: All public transport (TRANSIT)")
    
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,  # Bishan
        end_lat=1.2844, end_lon=103.8607,      # Marina Bay
        route_type='pt',
        date=date_str,
        time='08:30:00',
        mode='transit',  # All PT (MRT/LRT + buses)
        max_walk_distance=1000,  # Max 1km walking
        num_itineraries=3  # Get 3 route options
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
    else:
        plan = route.get('plan', {})
        itineraries = plan.get('itineraries', [])
        
        print(f"\n✅ Found {len(itineraries)} route option(s):\n")
        
        for i, itinerary in enumerate(itineraries, 1):
            duration = itinerary.get('duration', 0)
            distance = itinerary.get('walkDistance', 0)
            
            time_str = OneMapAPI.format_route_time(duration)
            walk_str = OneMapAPI.format_route_distance(distance)
            
            print(f"   Option {i}:")
            print(f"   ├─ Total journey: {time_str}")
            print(f"   └─ Walking distance: {walk_str}")
            
            # Show legs (segments) of the journey
            legs = itinerary.get('legs', [])
            if legs:
                print(f"      Journey details:")
                for j, leg in enumerate(legs, 1):
                    mode = leg.get('mode', 'WALK')
                    from_name = leg.get('from', {}).get('name', 'Start')
                    to_name = leg.get('to', {}).get('name', 'End')
                    leg_duration = OneMapAPI.format_route_time(leg.get('duration', 0))
                    
                    print(f"      {j}. {mode}: {from_name} → {to_name} ({leg_duration})")
            print()


def example_4_bus_only_route():
    """Example 4: Bus-only public transport route."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Bus-Only Route")
    print("="*80)
    
    api = OneMapAPI()
    
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%m-%d-%Y')
    
    print(f"🚌 Mode: Bus only")
    
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,
        end_lat=1.3300, end_lon=103.8400,
        route_type='pt',
        date=date_str,
        time='14:00:00',
        mode='bus',  # Bus only
        max_walk_distance=500
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
        print(f"   (Bus-only routes may not be available for all locations)")
    else:
        plan = route.get('plan', {})
        itineraries = plan.get('itineraries', [])
        
        if itineraries:
            itinerary = itineraries[0]
            duration = itinerary.get('duration', 0)
            time_str = OneMapAPI.format_route_time(duration)
            print(f"✅ Bus route found! Travel time: {time_str}")
        else:
            print(f"⚠️  No bus-only route available")


def example_5_rail_only_route():
    """Example 5: MRT/LRT only route."""
    print("\n" + "="*80)
    print("EXAMPLE 5: MRT/LRT Only Route")
    print("="*80)
    
    api = OneMapAPI()
    
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%m-%d-%Y')
    
    print(f"🚇 Mode: MRT/LRT only")
    
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,  # Bishan MRT
        end_lat=1.3048, end_lon=103.8318,       # Orchard MRT
        route_type='pt',
        date=date_str,
        time='10:00:00',
        mode='rail',  # MRT/LRT only
        num_itineraries=2
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
    else:
        plan = route.get('plan', {})
        itineraries = plan.get('itineraries', [])
        
        print(f"\n✅ Found {len(itineraries)} MRT route option(s):\n")
        
        for i, itinerary in enumerate(itineraries, 1):
            duration = itinerary.get('duration', 0)
            time_str = OneMapAPI.format_route_time(duration)
            print(f"   Option {i}: {time_str}")


def example_6_cycling_route():
    """Example 6: Cycling route."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Cycling Route")
    print("="*80)
    
    api = OneMapAPI()
    
    route = api.get_route(
        start_lat=1.3521, start_lon=103.8198,
        end_lat=1.3700, end_lon=103.8500,
        route_type='cycle'
    )
    
    if 'error' in route:
        print(f"❌ Error: {route['error']}")
    else:
        summary = route.get('route_summary', {})
        distance = summary.get('total_distance', 0)
        time_sec = summary.get('total_time', 0)
        
        time_str = OneMapAPI.format_route_time(time_sec)
        dist_str = OneMapAPI.format_route_distance(distance)
        
        print(f"✅ Cycling route found!")
        print(f"   Distance: {dist_str}")
        print(f"   Cycling time: {time_str}")


def main():
    """Run all routing examples."""
    print("\n" + "="*80)
    print("ONEMAP ROUTING API - USAGE EXAMPLES")
    print("="*80)
    print("\nDemonstrating all routing capabilities:")
    print("1. Drive route")
    print("2. Walk route")
    print("3. Public transport (morning commute)")
    print("4. Bus-only route")
    print("5. MRT/LRT only route")
    print("6. Cycling route")
    
    try:
        example_1_drive_route()
        example_2_walk_route()
        example_3_pt_morning_commute()
        example_4_bus_only_route()
        example_5_rail_only_route()
        example_6_cycling_route()
        
        print("\n" + "="*80)
        print("✅ All examples completed!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")


if __name__ == '__main__':
    main()
