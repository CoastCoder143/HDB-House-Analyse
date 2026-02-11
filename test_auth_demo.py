#!/usr/bin/env python3
"""
Demonstration that our implementation matches the official Onemap Python API pattern.

Official Pattern (from Onemap docs):
    import requests
    url = "https://www.onemap.gov.sg/api/public/themesvc/retrieveTheme?queryName=dengue_cluster"
    headers = {"Authorization": "**********************"}  # **** is placeholder for actual token
    response = requests.request("GET", url, headers=headers)

Our Implementation:
    session = requests.Session()
    session.headers.update({"Authorization": actual_token})
    response = session.request("GET", url)

Both are functionally equivalent. The session approach is more efficient for multiple requests.
"""

import os
import requests
from house_analyzer import OneMapAPI

def test_direct_approach():
    """
    Test using the exact pattern from official Onemap docs.
    This demonstrates what the official documentation shows.
    """
    print("=" * 80)
    print("OFFICIAL ONEMAP PATTERN (from documentation)")
    print("=" * 80)
    
    # Get credentials
    email = os.getenv('ONEMAP_EMAIL') or input("Enter your Onemap email: ")
    password = os.getenv('ONEMAP_PASSWORD') or input("Enter your Onemap password: ")
    
    # Step 1: Authenticate to get token (official pattern)
    auth_url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    payload = {"email": email, "password": password}
    
    auth_response = requests.post(auth_url, json=payload, timeout=10)
    
    if auth_response.status_code == 200:
        token = auth_response.json().get('access_token')
        print(f"✓ Authentication successful")
        print(f"✓ Token obtained: {token[:20]}..." if token else "✗ No token received")
        
        # Step 2: Use token exactly as shown in official docs
        url = "https://www.onemap.gov.sg/api/public/themesvc/getAllThemesInfo?moreInfo=N"
        headers = {"Authorization": token}  # This is the official pattern
        
        print(f"\nMaking request with pattern:")
        print(f'  headers = {{"Authorization": token}}')
        print(f'  response = requests.request("GET", url, headers=headers)')
        
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            theme_count = len(data.get('Theme_Names', []))
            print(f"✓ Request successful!")
            print(f"✓ Retrieved {theme_count} themes")
            print(f"\nFirst 3 themes:")
            for theme in data.get('Theme_Names', [])[:3]:
                print(f"  - {theme.get('THEMENAME')} ({theme.get('QUERYNAME')})")
        else:
            print(f"✗ Request failed: {response.status_code}")
    else:
        print(f"✗ Authentication failed: {auth_response.status_code}")


def test_our_implementation():
    """
    Test using our Session-based approach.
    This demonstrates that our implementation works the same way.
    """
    print("\n" + "=" * 80)
    print("OUR SESSION-BASED IMPLEMENTATION")
    print("=" * 80)
    
    # Get credentials
    email = os.getenv('ONEMAP_EMAIL') or input("Enter your Onemap email: ")
    password = os.getenv('ONEMAP_PASSWORD') or input("Enter your Onemap password: ")
    
    # Use our OneMapAPI class
    api = OneMapAPI(email=email, password=password)
    
    # The class automatically authenticates and sets up the session
    print("✓ OneMapAPI initialized")
    print(f"✓ Session headers include Authorization: {bool(api.session.headers.get('Authorization'))}")
    
    # Get all themes using our implementation
    themes = api.get_all_themes_info(more_info=False)
    
    if themes:
        theme_count = len(themes)
        print(f"✓ Request successful!")
        print(f"✓ Retrieved {theme_count} themes")
        print(f"\nFirst 3 themes:")
        for theme in themes[:3]:
            print(f"  - {theme.get('THEMENAME')} ({theme.get('QUERYNAME')})")
    else:
        print("✗ No themes retrieved")


def compare_approaches():
    """
    Compare both approaches to show they're equivalent.
    """
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    
    print("""
Our implementation uses the same Authorization header format as the official docs:

OFFICIAL PATTERN:
    headers = {"Authorization": "token_value"}
    response = requests.request("GET", url, headers=headers)

OUR PATTERN:
    session.headers.update({"Authorization": "token_value"})
    response = session.request("GET", url)

KEY POINTS:
✓ Both use: headers = {"Authorization": "token"}
✓ Both use: requests.request() method
✓ NO "Bearer" prefix (as per Onemap API specification)
✓ Session approach reuses connections (more efficient)
✓ Session automatically includes headers in all requests

CONCLUSION:
Our implementation is functionally equivalent to the official pattern,
but more efficient for making multiple API calls.
""")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ONEMAP API AUTHORIZATION DEMONSTRATION")
    print("=" * 80)
    print("\nThis script demonstrates that our implementation follows the")
    print("official Onemap Python API documentation exactly.\n")
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--official":
        # Test official pattern only
        test_direct_approach()
    elif len(sys.argv) > 1 and sys.argv[1] == "--ours":
        # Test our implementation only
        test_our_implementation()
    elif len(sys.argv) > 1 and sys.argv[1] == "--compare":
        # Just show comparison
        compare_approaches()
    else:
        # Run both tests
        test_direct_approach()
        test_our_implementation()
        compare_approaches()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
