#!/usr/bin/env python3
"""Integration test for database and analytics"""
import requests
import time

BASE_URL = "http://localhost:5000"

def test_analytics():
    """Test analytics endpoint"""
    print("Testing analytics endpoint...")
    response = requests.get(f"{BASE_URL}/api/analytics")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Analytics API working")
        print(f"  Total sent: {data['total_sent']}")
        print(f"  Today sent: {data['today_sent']}")
        print(f"  Week sent: {data['week_sent']}")
        print(f"  Top companies: {data['top_companies']}")
        print(f"  Template usage: {data['template_usage']}")
        print(f"  Daily stats: {data['daily_stats']}")
        return True
    else:
        print(f"✗ Analytics API failed: {response.status_code}")
        return False

def test_dashboard():
    """Test dashboard page"""
    print("\nTesting dashboard page...")
    response = requests.get(f"{BASE_URL}/dashboard")
    
    if response.status_code == 200 and "Analytics Dashboard" in response.text:
        print("✓ Dashboard page loads correctly")
        return True
    else:
        print(f"✗ Dashboard page failed: {response.status_code}")
        return False

def test_homepage():
    """Test homepage"""
    print("\nTesting homepage...")
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("✓ Homepage loads correctly")
        return True
    else:
        print(f"✗ Homepage failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Job Application Email Automation - Integration Tests")
    print("=" * 60)
    
    results = []
    results.append(test_homepage())
    results.append(test_dashboard())
    results.append(test_analytics())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 60)
        exit(0)
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        exit(1)
