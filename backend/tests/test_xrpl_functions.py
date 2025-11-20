"""
Test XRPL functions without database
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from clients.xrpl_client import XRPLClient
from clients.xaman_client import XamanClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_xrpl_client():
    """Test XRPL client initialization and basic functions"""
    print("\n" + "="*60)
    print("Testing XRPL Client")
    print("="*60)
    
    try:
        # Initialize XRPL client
        xrpl_network = os.getenv('XRPL_NETWORK', 'testnet')
        xrpl_sponsor_seed = os.getenv('XRPL_SPONSOR_SEED')
        
        print(f"Network: {xrpl_network}")
        print(f"Sponsor seed configured: {'Yes' if xrpl_sponsor_seed else 'No'}")
        
        xrpl_client = XRPLClient(
            network=xrpl_network,
            sponsor_seed=xrpl_sponsor_seed
        )
        print("✓ XRPL Client initialized successfully")
        
        # Test wallet generation
        print("\nTesting wallet generation...")
        address, seed = xrpl_client.generate_wallet()
        print(f"✓ Generated wallet:")
        print(f"  Address: {address}")
        print(f"  Seed: {seed[:10]}...")
        
        # Test sponsor balance check
        if xrpl_sponsor_seed:
            print("\nChecking sponsor wallet balance...")
            balance = xrpl_client.get_sponsor_balance()
            balance_xrp = balance / 1_000_000
            print(f"✓ Sponsor balance: {balance_xrp} XRP ({balance} drops)")
            
            # Check sponsor health
            print("\nChecking sponsor health...")
            health = xrpl_client.check_sponsor_health()
            print(f"✓ Sponsor health:")
            print(f"  Healthy: {health['healthy']}")
            print(f"  Balance: {health.get('balance_xrp', 0)} XRP")
            if health.get('warnings'):
                for warning in health['warnings']:
                    print(f"  Warning: {warning}")
        
        print("\n✓ All XRPL client tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ XRPL client test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_xaman_client():
    """Test Xaman client initialization"""
    print("\n" + "="*60)
    print("Testing Xaman Client")
    print("="*60)
    
    try:
        xaman_api_key = os.getenv('XAMAN_API_KEY')
        xaman_api_secret = os.getenv('XAMAN_API_SECRET')
        
        if not xaman_api_key or not xaman_api_secret:
            print("⚠ Xaman API credentials not configured")
            print("  Set XAMAN_API_KEY and XAMAN_API_SECRET in .env to test")
            return True
        
        if xaman_api_key == 'your_xaman_api_key_here':
            print("⚠ Xaman API credentials are placeholder values")
            print("  Get real credentials from https://apps.xaman.app/")
            return True
        
        print(f"API Key configured: Yes")
        print(f"API Secret configured: Yes")
        
        xaman_client = XamanClient(xaman_api_key, xaman_api_secret)
        print("✓ Xaman Client initialized successfully")
        
        print("\n✓ Xaman client tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Xaman client test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("XRPL & Xaman Function Tests")
    print("="*60)
    
    results = []
    
    # Test XRPL client
    results.append(("XRPL Client", test_xrpl_client()))
    
    # Test Xaman client
    results.append(("Xaman Client", test_xaman_client()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
