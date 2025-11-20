#!/usr/bin/env python
"""
Test wallet generation
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from clients.xrpl_client import XRPLClient

def test_wallet_generation():
    """Test XRPL wallet generation"""
    print("Testing XRPL wallet generation...")
    print("-" * 50)
    
    try:
        # Create XRPL client
        client = XRPLClient(network='testnet')
        print("✓ XRPLClient initialized")
        
        # Generate wallet
        address, seed = client.generate_wallet()
        print(f"✓ Wallet generated successfully")
        print(f"  Address: {address}")
        print(f"  Seed: {seed[:15]}...")
        
        # Validate address
        if address.startswith('r') and len(address) >= 25:
            print("✓ Address format is valid")
        else:
            print("✗ Address format is invalid")
            return False
        
        print("-" * 50)
        print("✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_wallet_generation()
    sys.exit(0 if success else 1)
