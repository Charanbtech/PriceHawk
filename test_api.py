#!/usr/bin/env python3
"""
Simple API test script for PriceHawk backend.
Tests basic functionality like health check, registration, login, and search.
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_registration():
    """Test user registration"""
    print("\n👤 Testing user registration...")
    try:
        data = {
            "email": "test@pricehawk.com",
            "password": "testpass123"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=data)
        if response.status_code in [201, 400]:  # 400 if user already exists
            print("✅ Registration endpoint working")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🔐 Testing user login...")
    try:
        data = {
            "email": "test@pricehawk.com",
            "password": "testpass123"
        }
        response = requests.post(f"{API_BASE}/auth/login", json=data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Login successful")
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_search(token):
    """Test product search"""
    print("\n🔍 Testing product search...")
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        data = {
            "query": "iPhone",
            "max_results": 5
        }
        response = requests.post(f"{API_BASE}/search", json=data, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            print(f"✅ Search successful - found {len(results)} products")
            if results:
                print(f"   Sample product: {results[0].get('title', 'N/A')}")
            return True
        else:
            print(f"❌ Search failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_tracking(token):
    """Test product tracking"""
    if not token:
        print("\n⚠️  Skipping tracking test - no auth token")
        return False
        
    print("\n📊 Testing product tracking...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # First, get tracked products
        response = requests.get(f"{API_BASE}/tracking/products", headers=headers)
        if response.status_code == 200:
            products = response.json().get("products", [])
            print(f"✅ Tracking list retrieved - {len(products)} products tracked")
            return True
        else:
            print(f"❌ Tracking failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Tracking error: {e}")
        return False

def test_notifications(token):
    """Test notifications"""
    if not token:
        print("\n⚠️  Skipping notifications test - no auth token")
        return False
        
    print("\n🔔 Testing notifications...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get notifications
        response = requests.get(f"{API_BASE}/notifications", headers=headers)
        if response.status_code == 200:
            notifications = response.json().get("notifications", [])
            print(f"✅ Notifications retrieved - {len(notifications)} notifications")
            return True
        else:
            print(f"❌ Notifications failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Notifications error: {e}")
        return False

def main():
    print("🦅 PriceHawk API Test Suite")
    print("=" * 40)
    
    # Wait a bit for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    tests_passed = 0
    total_tests = 6
    
    # Run tests
    if test_health():
        tests_passed += 1
    
    if test_registration():
        tests_passed += 1
    
    token = test_login()
    if token:
        tests_passed += 1
    
    if test_search(token):
        tests_passed += 1
    
    if test_tracking(token):
        tests_passed += 1
    
    if test_notifications(token):
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! PriceHawk API is working correctly.")
    elif tests_passed >= total_tests // 2:
        print("⚠️  Some tests failed, but core functionality is working.")
    else:
        print("❌ Many tests failed. Please check your configuration.")
    
    print("\n💡 Tips:")
    print("   - Make sure MongoDB is accessible")
    print("   - Check your .env configuration")
    print("   - Verify Docker containers are running")
    print("   - Check logs with: docker-compose logs")

if __name__ == "__main__":
    main()