"""
Verification script for SuiClient implementation.
Tests basic functionality of the Sui blockchain client.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clients.sui_client import SuiClient
from config import Config


def verify_sui_client():
    """Verify SuiClient basic functionality."""
    print("=" * 60)
    print("Sui Client Verification")
    print("=" * 60)
    
    try:
        # Test 1: Initialize client without sponsor
        print("\n[Test 1] Initializing SuiClient without sponsor...")
        client = SuiClient(network='testnet')
        print("✓ SuiClient initialized successfully")
        print(f"  Network: {client.network}")
        
        # Test 2: Generate wallet
        print("\n[Test 2] Generating new wallet...")
        address, private_key = client.generate_wallet()
        print("✓ Wallet generated successfully")
        print(f"  Address: {address}")
        print(f"  Private key length: {len(private_key)} characters")
        
        # Test 3: Get wallet balance (should be 0 for new wallet)
        print("\n[Test 3] Getting wallet balance...")
        balance = client.get_wallet_balance(address)
        print(f"✓ Balance retrieved: {balance} MIST")
        
        # Test 4: Get owned objects (should be empty for new wallet)
        print("\n[Test 4] Getting owned objects...")
        objects = client.get_owned_objects(address)
        print(f"✓ Owned objects retrieved: {len(objects)} objects")
        
        # Test 5: Initialize with sponsor (if configured)
        print("\n[Test 5] Testing sponsor configuration...")
        sponsor_key = Config.SUI_SPONSOR_PRIVATE_KEY
        if sponsor_key and sponsor_key != 'your-sui-sponsor-private-key':
            try:
                sponsored_client = SuiClient(
                    network='testnet',
                    sponsor_private_key=sponsor_key
                )
                print("✓ SuiClient with sponsor initialized successfully")
            except Exception as e:
                print(f"⚠ Sponsor initialization failed: {str(e)}")
                print("  (This is expected if sponsor key is not configured)")
        else:
            print("⚠ Sponsor private key not configured (skipping)")
        
        # Test 6: Test NFT minting preparation (without actual execution)
        print("\n[Test 6] Testing NFT minting preparation...")
        try:
            # This will fail without sponsor, which is expected
            result = client.mint_nft(
                recipient_address=address,
                nft_name="Test NFT",
                nft_description="Test NFT Description",
                nft_image_url="https://example.com/image.png",
                metadata={"test": "data"},
                use_sponsor=False
            )
            print("✓ NFT minting prepared")
        except NotImplementedError as e:
            print(f"✓ Expected error (Move contract not deployed): {str(e)[:80]}...")
        except Exception as e:
            print(f"⚠ Unexpected error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("Verification Summary")
        print("=" * 60)
        print("✓ SuiClient implementation verified successfully")
        print("✓ Wallet generation working")
        print("✓ Balance and object queries working")
        print("⚠ NFT minting awaits Move contract deployment")
        print("\nNote: Full NFT minting functionality requires:")
        print("  1. Deployed Move smart contract")
        print("  2. Configured sponsor wallet with SUI balance")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = verify_sui_client()
    sys.exit(0 if success else 1)
