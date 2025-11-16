#!/usr/bin/env python3
"""
Verify XRPL client configuration and functionality.
Tests wallet generation, balance queries, and sponsor wallet health.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from clients.xrpl_client import XRPLClient
from config import Config
from dotenv import load_dotenv

load_dotenv()


def verify_xrpl_client():
    """Verify XRPL client configuration and functionality."""
    print("=" * 70)
    print("XRPL Client Verification")
    print("=" * 70)
    print()
    
    config = Config()
    
    # Check configuration
    print("Checking configuration...")
    print()
    
    # Check network
    network = config.XRPL_NETWORK
    if not network:
        print("❌ XRPL_NETWORK not configured in .env")
        return False
    print(f"✓ Network: {network}")
    
    # Check sponsor seed
    sponsor_seed = config.XRPL_SPONSOR_SEED
    if not sponsor_seed or sponsor_seed == 'your_xrpl_sponsor_seed':
        print("❌ XRPL_SPONSOR_SEED not configured in .env")
        print("   Run: python scripts/generate_sponsor_wallet.py")
        return False
    print(f"✓ Sponsor seed configured")
    
    print()
    
    try:
        # Initialize XRPL client
        print("Initializing XRPL Client...")
        client = XRPLClient(
            network=network,
            sponsor_seed=sponsor_seed
        )
        print("✓ XRPL client initialized")
        print()
        
        # Check sponsor wallet
        print("Checking sponsor wallet...")
        print()
        
        sponsor_address = client.sponsor_wallet.classic_address
        print(f"  Address: {sponsor_address}")
        
        balance = client.get_wallet_balance(sponsor_address)
        xrp_balance = balance / 1_000_000
        print(f"  Balance: {balance} drops ({xrp_balance:.6f} XRP)")
        
        if balance < 10_000_000:  # Less than 10 XRP
            print()
            print("⚠️  WARNING: Sponsor wallet balance is low!")
            print(f"   Current: {xrp_balance:.6f} XRP")
            print(f"   Recommended: At least 10 XRP")
            print()
            
            if network in ['testnet', 'devnet']:
                print("Get test XRP from faucet:")
                print(f"  https://xrpl.org/xrp-testnet-faucet.html")
                print(f"  Address: {sponsor_address}")
            else:
                print("Transfer XRP to sponsor wallet:")
                print(f"  Address: {sponsor_address}")
        else:
            print("✓ Sponsor wallet has sufficient balance")
        
        print()
        
        # Check sponsor health
        print("Checking sponsor wallet health...")
        print()
        
        health = client.check_sponsor_health()
        
        if health['healthy']:
            print("✓ Sponsor wallet is healthy")
        else:
            print("⚠️  Sponsor wallet health check failed")
            if 'error' in health:
                print(f"   Error: {health['error']}")
        
        if health.get('warnings'):
            print()
            print("Warnings:")
            for warning in health['warnings']:
                print(f"  - {warning}")
        
        if health.get('recommendations'):
            print()
            print("Recommendations:")
            for rec in health['recommendations']:
                print(f"  - {rec}")
        
        print()
        
        # Test wallet generation
        print("Testing wallet generation...")
        test_address, test_seed = client.generate_wallet()
        print(f"✓ Generated test wallet: {test_address}")
        print()
        
        # Summary
        print("=" * 70)
        print("Verification Summary")
        print("=" * 70)
        print()
        print("✓ Configuration valid")
        print("✓ XRPL client initialized")
        print("✓ Sponsor wallet configured")
        print("✓ Wallet generation working")
        print()
        
        if balance >= 10_000_000:
            print("✅ All checks passed! XRPL client is ready for use.")
        else:
            print("⚠️  Please fund the sponsor wallet before minting NFTs.")
        
        print()
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_xrpl_client()
    sys.exit(0 if success else 1)
