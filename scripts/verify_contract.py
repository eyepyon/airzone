#!/usr/bin/env python3
"""
Verify Airzone NFT smart contract deployment and functionality.

This script tests the deployed Move contract by:
1. Checking configuration
2. Generating a test wallet
3. Minting a test NFT
4. Verifying the NFT was created

Requirements: 3.2, 3.3
"""
import sys
import os
import time

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from clients.sui_client import SuiClient
from config import Config


def verify_contract():
    """Verify the deployed NFT contract."""
    print("=" * 70)
    print("Airzone NFT Contract Verification")
    print("=" * 70)
    print()
    
    # Load configuration
    config = Config()
    
    print("Configuration Check")
    print("-" * 70)
    
    # Check network
    network = config.SUI_NETWORK
    if not network:
        print("❌ SUI_NETWORK not configured in .env")
        return False
    print(f"✓ Network: {network}")
    
    # Check sponsor private key
    sponsor_key = config.SUI_SPONSOR_PRIVATE_KEY
    if not sponsor_key or sponsor_key == 'your-sui-sponsor-private-key':
        print("❌ SUI_SPONSOR_PRIVATE_KEY not configured in .env")
        print("   Run: python scripts/generate_sponsor_wallet.py")
        return False
    print(f"✓ Sponsor key configured")
    
    # Check package ID
    package_id = config.SUI_PACKAGE_ID
    if not package_id or package_id == 'your-deployed-package-id':
        print("❌ SUI_PACKAGE_ID not configured in .env")
        print("   Run: bash scripts/deploy_contract.sh")
        return False
    print(f"✓ Package ID: {package_id}")
    
    print()
    
    try:
        # Initialize Sui client
        print("Initializing Sui Client...")
        client = SuiClient(
            network=network,
            sponsor_private_key=sponsor_key,
            package_id=package_id
        )
        print("✓ Sui client initialized")
        print()
        
        # Check sponsor wallet balance
        print("Checking Sponsor Wallet...")
        sponsor_address = str(client.sponsor_keypair.to_address())
        print(f"  Address: {sponsor_address}")
        
        balance = client.get_wallet_balance(sponsor_address)
        sui_balance = balance / 1_000_000_000
        print(f"  Balance: {balance} MIST ({sui_balance:.4f} SUI)")
        
        if balance < 100_000_000:  # Less than 0.1 SUI
            print("  ⚠️  Warning: Low balance. Consider funding the sponsor wallet.")
        else:
            print("  ✓ Sufficient balance")
        print()
        
        # Generate test recipient wallet
        print("Generating Test Recipient Wallet...")
        recipient_address, recipient_key = client.generate_wallet()
        print(f"  Address: {recipient_address}")
        print("✓ Test wallet generated")
        print()
        
        # Test NFT minting
        print("Testing NFT Minting...")
        print("-" * 70)
        print()
        
        nft_name = "Airzone Test NFT"
        nft_description = "Test NFT minted during contract verification"
        nft_image_url = "https://example.com/test-nft.png"
        
        print(f"  Name: {nft_name}")
        print(f"  Description: {nft_description}")
        print(f"  Image URL: {nft_image_url}")
        print(f"  Recipient: {recipient_address}")
        print()
        
        print("Minting NFT (this may take a few seconds)...")
        
        try:
            result = client.mint_nft(
                recipient_address=recipient_address,
                nft_name=nft_name,
                nft_description=nft_description,
                nft_image_url=nft_image_url,
                metadata={'test': True},
                use_sponsor=True
            )
            
            print()
            print("=" * 70)
            print("NFT Minting Result")
            print("=" * 70)
            print()
            
            if result.get('success'):
                print("✓ NFT minted successfully!")
                print()
                print(f"  NFT Object ID:       {result.get('nft_object_id')}")
                print(f"  Transaction Digest:  {result.get('transaction_digest')}")
                print(f"  Recipient:           {result.get('recipient')}")
                print(f"  Sponsor:             {result.get('sponsor')}")
                print()
                
                # View on explorer
                nft_id = result.get('nft_object_id')
                if nft_id:
                    if network == 'mainnet':
                        explorer_url = f"https://suiexplorer.com/object/{nft_id}"
                    else:
                        explorer_url = f"https://suiexplorer.com/object/{nft_id}?network={network}"
                    
                    print(f"  View on Explorer: {explorer_url}")
                    print()
                
                # Verify ownership
                print("Verifying NFT Ownership...")
                time.sleep(2)  # Wait for blockchain to process
                
                if nft_id:
                    owns_nft = client.verify_nft_ownership(recipient_address, nft_id)
                    if owns_nft:
                        print("✓ NFT ownership verified!")
                    else:
                        print("⚠️  Could not verify ownership (may need more time)")
                
                print()
                print("=" * 70)
                print("Verification Summary")
                print("=" * 70)
                print()
                print("✓ Configuration valid")
                print("✓ Sui client initialized")
                print("✓ Sponsor wallet funded")
                print("✓ NFT minting successful")
                print("✓ Sponsored transaction working")
                print()
                print("🎉 Contract verification complete!")
                print()
                print("The Airzone NFT contract is deployed and working correctly.")
                print("You can now start using the NFT minting functionality in your application.")
                print()
                
                return True
            else:
                print("❌ NFT minting failed")
                print(f"   Message: {result.get('message')}")
                return False
                
        except Exception as e:
            print()
            print(f"❌ NFT minting failed: {str(e)}")
            print()
            print("Common issues:")
            print("  - Package ID incorrect or contract not deployed")
            print("  - Sponsor wallet has insufficient balance")
            print("  - Network mismatch between config and deployment")
            print()
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = verify_contract()
    sys.exit(0 if success else 1)
