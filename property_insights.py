#!/usr/bin/env python3
"""
Property Insights Engine
========================

Provides intelligent analysis and recommendations for property evaluation.
Acts as a smart property agent to identify hidden value and insights.
"""

from typing import Dict, List, Tuple
import math


class PropertyInsights:
    """
    Smart property analysis engine that provides insights like a top property agent.
    """
    
    # Amenity importance weights (0-10 scale)
    AMENITY_WEIGHTS = {
        # Education (High importance for families)
        'kindergartens': 8,
        'childcare': 8,
        'registered_schools': 9,
        'schools': 9,
        'junior_colleges': 7,
        'primary_schools': 9,
        'secondary_schools': 9,
        
        # Healthcare (Critical for all)
        'hospitals': 10,
        'clinics': 7,
        'pharmacies': 6,
        'eldercare': 5,
        'nursing_homes': 5,
        
        # Transport (Very high importance)
        'mrt_stations': 10,
        'lrt_stations': 8,
        'bus_stops': 7,
        'taxi_stands': 5,
        
        # Shopping & Daily needs (High importance)
        'shopping_malls': 7,
        'supermarkets': 8,
        'hawker_centres': 9,  # Singapore essential!
        'markets': 7,
        'convenience_stores': 6,
        
        # Recreation & Lifestyle (Medium-High importance)
        'parks': 7,
        'community_clubs': 6,
        'libraries': 6,
        'gyms': 5,
        'sports_facilities': 5,
        'swimming_pools': 5,
        
        # Safety & Security (High importance)
        'police_stations': 7,
        'fire_stations': 6,
        'civil_defence': 5,
        
        # Negative factors (detractors)
        'dengue_cluster': -8,
        'industrial': -5,
        'construction': -3,
        'pollution': -7,
        
        # Other useful amenities
        'banks': 5,
        'post_offices': 4,
        'places_of_worship': 3,
        'cemeteries': -4,
        
        # Default for unknown categories
        'default': 3
    }
    
    # Distance thresholds for different amenity types (in km)
    DISTANCE_THRESHOLDS = {
        'walking': 0.5,      # 5-10 min walk
        'short_walk': 1.0,   # 10-15 min walk
        'cycling': 3.0,      # Cycling distance
        'short_drive': 5.0,  # Short drive/bus
        'acceptable': 10.0   # Still acceptable
    }
    
    def __init__(self):
        """Initialize the property insights engine."""
        pass
    
    def calculate_livability_score(self, results: Dict) -> Dict:
        """
        Calculate comprehensive livability score (0-100).
        
        Args:
            results: Analysis results from house analyzer
            
        Returns:
            Dictionary with overall score and breakdown
        """
        scores = {
            'overall': 0,
            'transport': 0,
            'education': 0,
            'healthcare': 0,
            'shopping': 0,
            'recreation': 0,
            'safety': 0,
            'breakdown': {}
        }
        
        # Transport score (25 points max)
        scores['transport'] = self._calculate_transport_score(results)
        
        # Education score (20 points max)
        scores['education'] = self._calculate_education_score(results)
        
        # Healthcare score (15 points max)
        scores['healthcare'] = self._calculate_healthcare_score(results)
        
        # Shopping & daily needs (20 points max)
        scores['shopping'] = self._calculate_shopping_score(results)
        
        # Recreation score (10 points max)
        scores['recreation'] = self._calculate_recreation_score(results)
        
        # Safety score (10 points max)
        scores['safety'] = self._calculate_safety_score(results)
        
        # Calculate overall (sum of categories)
        scores['overall'] = min(100, sum([
            scores['transport'],
            scores['education'],
            scores['healthcare'],
            scores['shopping'],
            scores['recreation'],
            scores['safety']
        ]))
        
        return scores
    
    def _calculate_transport_score(self, results: Dict) -> float:
        """Calculate transport accessibility score (0-25)."""
        score = 0
        
        # MRT within walking distance (15 points)
        mrt_stations = results.get('transport', {}).get('mrt_stations', [])
        if mrt_stations:
            nearest_mrt = mrt_stations[0]['distance_km']
            if nearest_mrt <= 0.5:
                score += 15
            elif nearest_mrt <= 1.0:
                score += 12
            elif nearest_mrt <= 2.0:
                score += 8
            elif nearest_mrt <= 3.0:
                score += 5
        
        # Bus stops (7 points)
        bus_stops = results.get('transport', {}).get('bus_stops', [])
        if bus_stops:
            nearest_bus = bus_stops[0]['distance_km']
            if nearest_bus <= 0.3:
                score += 7
            elif nearest_bus <= 0.5:
                score += 5
            elif nearest_bus <= 1.0:
                score += 3
        
        # Not too close to expressway (noise) (3 points)
        roads = results.get('transport', {}).get('major_roads', [])
        if roads:
            nearest_road = roads[0]['distance_km']
            if nearest_road >= 0.5:  # Good distance
                score += 3
            elif nearest_road >= 0.3:
                score += 2
        else:
            score += 3  # No major roads nearby is good
        
        return score
    
    def _calculate_education_score(self, results: Dict) -> float:
        """Calculate education facilities score (0-20)."""
        score = 0
        amenities = results.get('amenities', {})
        
        # Schools nearby (12 points)
        for school_type in ['registered_schools', 'primary_schools', 'secondary_schools', 'schools']:
            schools = amenities.get(school_type, [])
            if schools:
                nearest = schools[0]['distance_km']
                if nearest <= 1.0:
                    score += 6
                elif nearest <= 2.0:
                    score += 4
                elif nearest <= 3.0:
                    score += 2
                break
        
        # Childcare/kindergarten (5 points)
        for care_type in ['kindergartens', 'childcare']:
            care = amenities.get(care_type, [])
            if care:
                nearest = care[0]['distance_km']
                if nearest <= 0.5:
                    score += 3
                elif nearest <= 1.0:
                    score += 2
                elif nearest <= 2.0:
                    score += 1
                break
        
        # Libraries (3 points)
        libraries = amenities.get('libraries', [])
        if libraries:
            nearest = libraries[0]['distance_km']
            if nearest <= 2.0:
                score += 3
            elif nearest <= 5.0:
                score += 2
        
        return min(20, score)
    
    def _calculate_healthcare_score(self, results: Dict) -> float:
        """Calculate healthcare facilities score (0-15)."""
        score = 0
        amenities = results.get('amenities', {})
        
        # Hospitals/clinics (10 points)
        for health_type in ['hospitals', 'clinics']:
            facilities = amenities.get(health_type, [])
            if facilities:
                nearest = facilities[0]['distance_km']
                if nearest <= 1.0:
                    score += 5
                elif nearest <= 3.0:
                    score += 3
                elif nearest <= 5.0:
                    score += 2
                break
        
        # Pharmacies (3 points)
        pharmacies = amenities.get('pharmacies', [])
        if pharmacies:
            nearest = pharmacies[0]['distance_km']
            if nearest <= 0.5:
                score += 3
            elif nearest <= 1.0:
                score += 2
        
        # Eldercare (2 points)
        eldercare = amenities.get('eldercare', [])
        if eldercare and eldercare[0]['distance_km'] <= 2.0:
            score += 2
        
        return min(15, score)
    
    def _calculate_shopping_score(self, results: Dict) -> float:
        """Calculate shopping & daily needs score (0-20)."""
        score = 0
        amenities = results.get('amenities', {})
        
        # Hawker centres (essential in Singapore!) (8 points)
        hawkers = amenities.get('hawker_centres', [])
        if hawkers:
            nearest = hawkers[0]['distance_km']
            if nearest <= 0.5:
                score += 8
            elif nearest <= 1.0:
                score += 6
            elif nearest <= 2.0:
                score += 4
        
        # Supermarkets (7 points)
        supermarkets = amenities.get('supermarkets', [])
        if supermarkets:
            nearest = supermarkets[0]['distance_km']
            if nearest <= 0.5:
                score += 7
            elif nearest <= 1.0:
                score += 5
            elif nearest <= 2.0:
                score += 3
        
        # Shopping malls (5 points)
        malls = amenities.get('shopping_malls', [])
        if malls:
            nearest = malls[0]['distance_km']
            if nearest <= 1.0:
                score += 5
            elif nearest <= 3.0:
                score += 3
        
        return min(20, score)
    
    def _calculate_recreation_score(self, results: Dict) -> float:
        """Calculate recreation facilities score (0-10)."""
        score = 0
        amenities = results.get('amenities', {})
        
        # Parks (5 points)
        parks = amenities.get('parks', []) or amenities.get('nationalparks', [])
        if parks:
            nearest = parks[0]['distance_km']
            if nearest <= 0.5:
                score += 5
            elif nearest <= 1.0:
                score += 4
            elif nearest <= 2.0:
                score += 3
        
        # Community clubs (3 points)
        cc = amenities.get('community_clubs', [])
        if cc and cc[0]['distance_km'] <= 2.0:
            score += 3
        
        # Gyms/sports (2 points)
        for rec_type in ['gyms', 'sports_facilities', 'swimming_pools']:
            facilities = amenities.get(rec_type, [])
            if facilities and facilities[0]['distance_km'] <= 2.0:
                score += 2
                break
        
        return min(10, score)
    
    def _calculate_safety_score(self, results: Dict) -> float:
        """Calculate safety & security score (0-10)."""
        score = 10  # Start with full score
        amenities = results.get('amenities', {})
        
        # Dengue clusters nearby (deduct points)
        dengue = amenities.get('dengue_cluster', [])
        if dengue:
            nearest = dengue[0]['distance_km']
            if nearest <= 0.5:
                score -= 5
            elif nearest <= 1.0:
                score -= 3
            elif nearest <= 2.0:
                score -= 1
        
        # Industrial areas nearby (deduct points)
        industrial = amenities.get('industrial', [])
        if industrial:
            nearest = industrial[0]['distance_km']
            if nearest <= 0.5:
                score -= 3
            elif nearest <= 1.0:
                score -= 2
        
        return max(0, score)
    
    def generate_smart_insights(self, results: Dict, scores: Dict) -> List[str]:
        """
        Generate smart property insights that agents would notice.
        
        Args:
            results: Analysis results
            scores: Livability scores
            
        Returns:
            List of insights
        """
        insights = []
        amenities = results.get('amenities', {})
        transport = results.get('transport', {})
        
        # Transport insights
        mrt_stations = transport.get('mrt_stations', [])
        if mrt_stations:
            nearest_mrt = mrt_stations[0]
            if nearest_mrt['distance_km'] <= 0.5:
                insights.append(f"🌟 **PRIME LOCATION**: MRT station ({nearest_mrt['name']}) within 500m walking distance - highly desirable!")
            elif nearest_mrt['distance_km'] <= 1.0:
                insights.append(f"✅ **EXCELLENT**: MRT station ({nearest_mrt['name']}) within 1km - good connectivity")
        
        # Multiple MRT lines
        if len(mrt_stations) >= 2:
            insights.append(f"🎯 **CONNECTIVITY BONUS**: Access to {len(mrt_stations)} MRT stations - exceptional transport options")
        
        # Education insights
        schools_found = False
        for school_type in ['registered_schools', 'primary_schools', 'secondary_schools', 'schools']:
            schools = amenities.get(school_type, [])
            if schools and schools[0]['distance_km'] <= 1.0:
                insights.append(f"👨‍👩‍👧 **FAMILY-FRIENDLY**: Primary school within 1km - ideal for families with children")
                schools_found = True
                break
        
        # Hawker centre (Singapore essential!)
        hawkers = amenities.get('hawker_centres', [])
        if hawkers and hawkers[0]['distance_km'] <= 0.5:
            insights.append(f"🍜 **LOCAL LIVING**: Hawker centre within 500m - authentic Singapore lifestyle & affordable dining")
        
        # Parks for recreation
        parks = amenities.get('parks', []) or amenities.get('nationalparks', [])
        if parks and parks[0]['distance_km'] <= 0.5:
            insights.append(f"🌳 **WELLNESS BONUS**: Park within 500m - great for exercise, relaxation & air quality")
        
        # Shopping convenience
        supermarkets = amenities.get('supermarkets', [])
        if supermarkets and supermarkets[0]['distance_km'] <= 0.5:
            insights.append(f"🛒 **CONVENIENCE**: Supermarket within 500m - daily essentials within walking distance")
        
        # Warning signs
        dengue = amenities.get('dengue_cluster', [])
        if dengue and dengue[0]['distance_km'] <= 1.0:
            insights.append(f"⚠️  **ALERT**: Dengue cluster within 1km - consider mosquito prevention measures")
        
        # Major roads proximity
        roads = transport.get('major_roads', [])
        if roads:
            nearest_road = roads[0]
            if nearest_road['distance_km'] <= 0.2:
                insights.append(f"🔊 **NOISE CONCERN**: Expressway within 200m - potential noise pollution issue")
            elif nearest_road['distance_km'] >= 0.5 and nearest_road['distance_km'] <= 1.5:
                insights.append(f"✅ **BALANCED**: Good distance from expressway - accessible but quiet")
        
        # Overall livability
        overall_score = scores['overall']
        if overall_score >= 85:
            insights.append(f"⭐ **EXCEPTIONAL LOCATION**: Livability score {overall_score}/100 - top-tier property location!")
        elif overall_score >= 70:
            insights.append(f"✅ **GREAT LOCATION**: Livability score {overall_score}/100 - solid choice for living")
        elif overall_score >= 50:
            insights.append(f"🔵 **DECENT LOCATION**: Livability score {overall_score}/100 - reasonable for budget-conscious buyers")
        else:
            insights.append(f"⚠️  **LIMITED AMENITIES**: Livability score {overall_score}/100 - consider if you need more facilities")
        
        return insights
    
    def generate_property_profile(self, results: Dict, scores: Dict) -> Dict:
        """
        Generate a property profile with target demographics and selling points.
        
        Args:
            results: Analysis results
            scores: Livability scores
            
        Returns:
            Property profile dictionary
        """
        profile = {
            'ideal_for': [],
            'selling_points': [],
            'concerns': [],
            'investment_potential': 'Medium',
            'rental_attractiveness': 'Medium'
        }
        
        amenities = results.get('amenities', {})
        transport = results.get('transport', {})
        
        # Determine ideal demographics
        if scores['education'] >= 15:
            profile['ideal_for'].append('Families with school-age children')
        if scores['transport'] >= 20:
            profile['ideal_for'].append('Working professionals (easy commute)')
        if scores['recreation'] >= 7:
            profile['ideal_for'].append('Active lifestyle seekers')
        if amenities.get('eldercare'):
            profile['ideal_for'].append('Multi-generational families')
        if scores['overall'] >= 75:
            profile['ideal_for'].append('Premium property investors')
        
        # Selling points
        mrt_stations = transport.get('mrt_stations', [])
        if mrt_stations and mrt_stations[0]['distance_km'] <= 0.5:
            profile['selling_points'].append('MRT within 500m - premium transport connectivity')
        if scores['education'] >= 15:
            profile['selling_points'].append('Excellent school access - sought after by families')
        if scores['shopping'] >= 15:
            profile['selling_points'].append('Complete daily amenities - high convenience')
        if scores['recreation'] >= 7:
            profile['selling_points'].append('Good recreation facilities - quality lifestyle')
        
        # Concerns
        if scores['transport'] < 10:
            profile['concerns'].append('Limited public transport - car dependency')
        if scores['education'] < 10:
            profile['concerns'].append('Few schools nearby - may not suit families')
        if scores['shopping'] < 10:
            profile['concerns'].append('Limited shopping options - less convenient')
        
        # Investment potential
        if scores['overall'] >= 80 and scores['transport'] >= 20:
            profile['investment_potential'] = 'High'
            profile['rental_attractiveness'] = 'High'
        elif scores['overall'] >= 60:
            profile['investment_potential'] = 'Medium-High'
            profile['rental_attractiveness'] = 'Medium-High'
        elif scores['overall'] < 40:
            profile['investment_potential'] = 'Low-Medium'
            profile['rental_attractiveness'] = 'Low-Medium'
        
        return profile
    
    def get_grade_from_score(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        else:
            return 'D'
    
    def get_score_emoji(self, score: float) -> str:
        """Get emoji indicator for score."""
        if score >= 85:
            return '🟢'  # Excellent
        elif score >= 70:
            return '🟡'  # Good
        elif score >= 50:
            return '🟠'  # Average
        else:
            return '🔴'  # Below average
