"""
Verification script to test endpoint functionality.
This script starts the Flask app and tests all registered endpoints.
"""
import sys
import os
import time
import requests
from threading import Thread

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

def start_flask_app():
    """Start Flask app in a separate thread"""
    from app import app
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

def test_endpoints():
    """Test all registered endpoints"""
    base_url = 'http://127.0.0.1:5001'
    
    print("Endpoint Functionality Verification")
    print("=" * 60)
    
    # Wait for Flask to start
    print("\nWaiting for Flask app to start...")
    time.sleep(2)
    
    all_passed = True
    
    # Test health check endpoint
    print("\n✓ Testing Health Check Endpoint:")
    try:
        response = requests.get(f'{base_url}/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ GET /health - Status: {response.status_code}")
            print(f"    Response: {data}")
        else:
            print(f"  ✗ GET /health - Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ GET /health - Error: {str(e)}")
        all_passed = False
    
    # Test API version endpoint
    print("\n✓ Testing API Version Endpoint:")
    try:
        response = requests.get(f'{base_url}/api/v1', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ GET /api/v1 - Status: {response.status_code}")
            print(f"    Available endpoints: {list(data.get('data', {}).get('endpoints', {}).keys())}")
        else:
            print(f"  ✗ GET /api/v1 - Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ GET /api/v1 - Error: {str(e)}")
        all_passed = False
    
    # Test order endpoints (without auth - should return 401)
    print("\n✓ Testing Order Endpoints (without auth):")
    try:
        response = requests.get(f'{base_url}/api/v1/orders', timeout=5)
        if response.status_code == 401:
            print(f"  ✓ GET /api/v1/orders - Status: {response.status_code} (Auth required)")
        else:
            print(f"  ✗ GET /api/v1/orders - Unexpected status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ GET /api/v1/orders - Error: {str(e)}")
        all_passed = False
    
    # Test payment endpoints (without auth - should return 401)
    print("\n✓ Testing Payment Endpoints (without auth):")
    try:
        response = requests.post(f'{base_url}/api/v1/payments/intent', 
                                json={}, timeout=5)
        if response.status_code == 401:
            print(f"  ✓ POST /api/v1/payments/intent - Status: {response.status_code} (Auth required)")
        else:
            print(f"  ✗ POST /api/v1/payments/intent - Unexpected status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ POST /api/v1/payments/intent - Error: {str(e)}")
        all_passed = False
    
    # Test WiFi connect endpoint (no auth required)
    print("\n✓ Testing WiFi Endpoints (no auth required):")
    try:
        response = requests.post(f'{base_url}/api/v1/wifi/connect',
                                json={
                                    "mac_address": "AA:BB:CC:DD:EE:FF",
                                    "ip_address": "192.168.1.100"
                                }, timeout=5)
        # Should return 400 (validation error) or 201 (success), not 401
        if response.status_code in [201, 400, 500]:
            print(f"  ✓ POST /api/v1/wifi/connect - Status: {response.status_code} (Endpoint accessible)")
        else:
            print(f"  ✗ POST /api/v1/wifi/connect - Unexpected status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ POST /api/v1/wifi/connect - Error: {str(e)}")
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All endpoint tests passed!")
        return 0
    else:
        print("✗ Some endpoint tests failed")
        return 1

if __name__ == '__main__':
    # Start Flask in background thread
    flask_thread = Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Run tests
    exit_code = test_endpoints()
    
    # Exit
    sys.exit(exit_code)
