#!/usr/bin/env python3
"""
Comprehensive diagnostic tool for Onemap API connectivity issues.

Run this to diagnose why bus stops and roads are not appearing.
"""

import socket
import requests
import sys
from datetime import datetime

def print_header(text):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def test_internet_connectivity():
    """Test basic internet connectivity."""
    print_header("1. TESTING BASIC INTERNET CONNECTIVITY")
    
    test_sites = [
        ("Google DNS", "8.8.8.8", 53),
        ("Cloudflare DNS", "1.1.1.1", 53),
        ("Google", "www.google.com", 443),
    ]
    
    for name, host, port in test_sites:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print(f"✅ Can connect to {name} ({host}:{port})")
        except Exception as e:
            print(f"❌ Cannot connect to {name} ({host}:{port})")
            print(f"   Error: {e}")

def test_dns_resolution():
    """Test DNS resolution for onemap.gov.sg."""
    print_header("2. TESTING DNS RESOLUTION FOR ONEMAP")
    
    hosts = [
        "www.onemap.gov.sg",
        "onemap.gov.sg",
        "www.gov.sg",
    ]
    
    for host in hosts:
        try:
            ip_addresses = socket.gethostbyname_ex(host)[2]
            print(f"✅ {host} resolves to: {', '.join(ip_addresses)}")
        except socket.gaierror as e:
            print(f"❌ Cannot resolve {host}")
            print(f"   Error: {e}")
        except Exception as e:
            print(f"❌ Error resolving {host}: {e}")

def test_https_connection():
    """Test HTTPS connection to onemap.gov.sg."""
    print_header("3. TESTING HTTPS CONNECTION TO ONEMAP")
    
    try:
        response = requests.get("https://www.onemap.gov.sg", timeout=10)
        print(f"✅ Can connect to https://www.onemap.gov.sg")
        print(f"   Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Cannot connect to https://www.onemap.gov.sg")
        print(f"   Error: {e}")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout connecting to https://www.onemap.gov.sg")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_onemap_api_endpoints():
    """Test Onemap API endpoints."""
    print_header("4. TESTING ONEMAP API ENDPOINTS")
    
    # Note: These endpoints require authentication, so we expect 400/401 errors
    # We're just testing if we can reach the server
    
    endpoints = [
        "/api/public/nearbysvc/getNearestBusStops?latitude=1.3521&longitude=103.8198&radius_in_meters=1000",
        "/api/public/nearbysvc/getNearestMrtStops?latitude=1.3521&longitude=103.8198&radius_in_meters=5000",
        "/api/auth/post/getToken",
    ]
    
    for endpoint in endpoints:
        url = f"https://www.onemap.gov.sg{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            if status in [400, 401, 403]:
                print(f"✅ Can reach {endpoint}")
                print(f"   Status: {status} (expected - needs authentication)")
            elif status == 200:
                print(f"✅ Can reach {endpoint}")
                print(f"   Status: {status}")
            else:
                print(f"⚠️  Reached {endpoint}")
                print(f"   Unexpected status: {status}")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Cannot reach {endpoint}")
            print(f"   Error: {e}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout reaching {endpoint}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_with_authentication():
    """Test API with authentication if token provided."""
    print_header("5. TESTING WITH AUTHENTICATION")
    
    import os
    token = os.environ.get('ONEMAP_TOKEN')
    
    if not token:
        print("ℹ️  No ONEMAP_TOKEN environment variable set")
        print("   To test with authentication, run:")
        print('   export ONEMAP_TOKEN="your_token_here"')
        print("   python diagnose_connection.py")
        return
    
    print(f"✅ Found ONEMAP_TOKEN environment variable")
    print(f"   Token: {token[:20]}...")
    
    # Test bus stops API
    url = "https://www.onemap.gov.sg/api/public/nearbysvc/getNearestBusStops"
    params = {
        'latitude': 1.3521,
        'longitude': 103.8198,
        'radius_in_meters': 1000
    }
    headers = {
        'Authorization': token
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"\n📍 Testing bus stops at Bishan (1.3521, 103.8198):")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Found {len(data)} bus stops")
            if data:
                print(f"   First stop: {data[0].get('name', 'Unknown')}")
        elif response.status_code == 401:
            print(f"   ❌ Authentication failed - token may be expired")
        elif response.status_code == 403:
            print(f"   ❌ Access forbidden - check token permissions")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection error: {e}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def print_summary():
    """Print diagnostic summary and recommendations."""
    print_header("DIAGNOSTIC SUMMARY & RECOMMENDATIONS")
    
    print("\n📋 If you see ❌ errors above:")
    print("\n1. DNS RESOLUTION FAILURE:")
    print("   - Your system cannot resolve www.onemap.gov.sg")
    print("   - Check /etc/resolv.conf (Linux/Mac)")
    print("   - Try: ping www.onemap.gov.sg")
    print("   - Try: nslookup www.onemap.gov.sg")
    
    print("\n2. CONNECTION REFUSED/TIMEOUT:")
    print("   - Firewall may be blocking HTTPS (port 443)")
    print("   - Corporate network may block external APIs")
    print("   - Check with: curl https://www.onemap.gov.sg")
    
    print("\n3. AUTHENTICATION ERRORS (401/403):")
    print("   - Token may be expired (they expire after 3 days)")
    print("   - Get new token at: https://www.onemap.gov.sg/apidocs/register")
    print("   - Run with: export ONEMAP_TOKEN=\"your_new_token\"")
    
    print("\n4. ALL TESTS PASS BUT STILL NO DATA:")
    print("   - Check coordinates are in Singapore (1.2-1.5, 103.6-104.0)")
    print("   - Some locations may not have bus stops/roads nearby")
    print("   - Try a known location like Bishan: 1.3521, 103.8198")
    
    print("\n💡 QUICK TESTS:")
    print("   1. Can you access: https://www.onemap.gov.sg in a browser?")
    print("   2. Can you ping: ping www.onemap.gov.sg")
    print("   3. Try from different network (mobile hotspot, home WiFi)")
    
    print("\n📞 SUPPORT:")
    print("   If all tests pass but still have issues, please report:")
    print("   - Which tests passed (✅) and which failed (❌)")
    print("   - Your operating system and Python version")
    print("   - Whether you're on corporate network, VPN, Docker, etc.")
    
    print()

def main():
    """Run all diagnostic tests."""
    print("\n🔍 ONEMAP API CONNECTIVITY DIAGNOSTICS")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Python: {sys.version.split()[0]}")
    
    test_internet_connectivity()
    test_dns_resolution()
    test_https_connection()
    test_onemap_api_endpoints()
    test_with_authentication()
    print_summary()

if __name__ == "__main__":
    main()
