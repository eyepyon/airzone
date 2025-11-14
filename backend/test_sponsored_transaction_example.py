#!/usr/bin/env python3
"""
Example integration test for sponsored transactions.
Demonstrates how to use the sponsored transaction feature in the Airzone system.

This is an example/template file - not meant to be run directly without proper setup.

Requirements: 3.3 - Sponsored transactions
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clients.sui_client import SuiClient
from config import Config


def example_sponsored_transaction_flow():
    """
    Example flow demonstrating sponsored transaction usage.
    
    This shows the complete flow from initialization to NFT minting
    with sponsor wallet management.
    """
    print("=" * 70)
    print("Sponsored Transaction Example Flow")
    print("=" * 70)
    
    # Step 1: Initialize SuiClient with sponsor configuration
    print("\n[Step 1] Initialize SuiClient with sponsor wallet")
    print("-" * 70)
    
    try:
        client = SuiClient(
            network=Config.SUI_NETWORK,
            sponsor_private_key=Config.SUI_SPONSOR_PRIVATE_KEY,
            package_id=Config.SUI_PACKAGE_ID
        )
        print(f"✓ Client initialized")
        print(f"  Network: {client.network}")
        print(f"  Sponsor configured: {client.sponsor_keypair is not None}")
        print(f"  Package ID: {client.package_id or 'Not configured'}")
    except Exception as e:
        print(f"✗ Failed to initialize client: {str(e)}")
        return False
    
    # Step 2: Check sponsor wallet health
    print("\n[Step 2] Check sponsor wallet health")
    print("-" * 70)
    
    try:
        health = client.check_sponsor_health()
        
        print(f"Health Status: {'✓ Healthy' if health['healthy'] else '✗ Unhealthy'}")
        print(f"Sponsor Address: {health.get('sponsor_address', 'N/A')}")
        print(f"Balance: {health.get('balance_sui', 0):.6f} SUI")
        print(f"Network: {health.get('network', 'N/A')}")
        print(f"Estimated Remaining Transactions: {health.get('estimated_remaining_transactions', 0)}")
        
        if health.get('warnings'):
            print("\nWarnings:")
            for warning in health['warnings']:
                print(f"  ⚠️  {warning}")
        
        if health.get('recommendations'):
            print("\nRecommendations:")
            for rec in health['recommendations']:
                print(f"  • {rec}")
        
        if not health['healthy']:
            print("\n✗ Sponsor wallet is not healthy. Please address issues before minting.")
            return False
            
    except Exception as e:
        print(f"✗ Failed to check health: {str(e)}")
        return False
    
    # Step 3: Validate sponsor balance
    print("\n[Step 3] Validate sponsor balance")
    print("-" * 70)
    
    try:
        is_valid = client.validate_sponsor_balance()
        
        if is_valid:
            print("✓ Sponsor wallet has sufficient balance")
            balance = client.get_sponsor_balance()
            print(f"  Current balance: {balance / 1_000_000_000:.6f} SUI")
            
            gas_cost = client.estimate_gas_cost()
            print(f"  Estimated gas per TX: {gas_cost / 1_000_000_000:.6f} SUI")
            
            remaining_txs = balance // gas_cost
            print(f"  Estimated remaining TXs: {remaining_txs}")
        else:
            print("✗ Sponsor wallet balance is insufficient")
            return False
            
    except Exception as e:
        print(f"✗ Failed to validate balance: {str(e)}")
        return False
    
    # Step 4: Generate test recipient wallet
    print("\n[Step 4] Generate test recipient wallet")
    print("-" * 70)
    
    try:
        recipient_address, recipient_key = client.generate_wallet()
        print(f"✓ Test recipient wallet generated")
        print(f"  Address: {recipient_address}")
        print(f"  (This wallet will receive the NFT without paying gas)")
    except Exception as e:
        print(f"✗ Failed to generate recipient wallet: {str(e)}")
        return False
    
    # Step 5: Prepare NFT metadata
    print("\n[Step 5] Prepare NFT metadata")
    print("-" * 70)
    
    nft_data = {
        'name': 'Airzone Welcome NFT',
        'description': 'Thank you for connecting to Airzone WiFi',
        'image_url': 'https://example.com/airzone-nft.png',
        'metadata': {
            'location': 'Test Location',
            'connected_at': '2024-01-01T00:00:00Z',
            'network': 'Airzone-Guest'
        }
    }
    
    print(f"✓ NFT metadata prepared")
    print(f"  Name: {nft_data['name']}")
    print(f"  Description: {nft_data['description']}")
    print(f"  Image URL: {nft_data['image_url']}")
    
    # Step 6: Mint NFT with sponsored transaction
    print("\n[Step 6] Mint NFT with sponsored transaction")
    print("-" * 70)
    
    try:
        print("Initiating sponsored transaction...")
        print("(Sponsor wallet will pay gas fees)")
        
        result = client.mint_nft(
            recipient_address=recipient_address,
            nft_name=nft_data['name'],
            nft_description=nft_data['description'],
            nft_image_url=nft_data['image_url'],
            metadata=nft_data['metadata'],
            use_sponsor=True  # This is the key - sponsor pays gas
        )
        
        print("\n✓ NFT minted successfully with sponsored transaction!")
        print(f"\nTransaction Details:")
        print(f"  NFT Object ID: {result['nft_object_id']}")
        print(f"  Transaction Digest: {result['transaction_digest']}")
        print(f"  Recipient: {result['recipient']}")
        print(f"  Sponsor: {result['sponsor']}")
        print(f"  Gas Used: {result['gas_used'] / 1_000_000_000:.6f} SUI")
        print(f"  Sponsor Balance After: {result['sponsor_balance_after'] / 1_000_000_000:.6f} SUI")
        
        print(f"\n✓ Recipient received NFT without paying any gas fees!")
        
    except ValueError as e:
        if "Package ID not configured" in str(e):
            print("⊘ Skipped: Move contract not deployed yet")
            print("  Deploy contract: bash scripts/deploy_contract.sh testnet")
            return True  # Not a failure, just not ready yet
        else:
            print(f"✗ Failed to mint NFT: {str(e)}")
            return False
    except Exception as e:
        print(f"✗ Failed to mint NFT: {str(e)}")
        return False
    
    # Step 7: Verify post-transaction sponsor health
    print("\n[Step 7] Verify post-transaction sponsor health")
    print("-" * 70)
    
    try:
        health = client.check_sponsor_health()
        
        print(f"Post-Transaction Status: {'✓ Healthy' if health['healthy'] else '⚠️  Needs Attention'}")
        print(f"Balance: {health.get('balance_sui', 0):.6f} SUI")
        print(f"Estimated Remaining Transactions: {health.get('estimated_remaining_transactions', 0)}")
        
        if health.get('warnings'):
            print("\nWarnings:")
            for warning in health['warnings']:
                print(f"  ⚠️  {warning}")
                
    except Exception as e:
        print(f"⚠️  Failed to check post-transaction health: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("\n✓ Sponsored transaction flow completed successfully!")
    print("\nKey Points:")
    print("  • Sponsor wallet paid all gas fees")
    print("  • Recipient received NFT without needing SUI tokens")
    print("  • Transaction was transparent to the end user")
    print("  • Sponsor balance was validated before transaction")
    print("  • Health monitoring provided warnings and recommendations")
    
    print("\nThis demonstrates the core value proposition:")
    print("  Users can receive NFTs without:")
    print("    - Having a wallet beforehand")
    print("    - Owning any cryptocurrency")
    print("    - Understanding blockchain technology")
    print("    - Paying any fees")
    
    print("\n" + "=" * 70)
    
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("Airzone Sponsored Transaction Example")
    print("=" * 70)
    print("\nThis example demonstrates the sponsored transaction feature")
    print("where the system pays gas fees for users to receive NFTs.")
    print("\nRequirements:")
    print("  • SUI_SPONSOR_PRIVATE_KEY configured in .env")
    print("  • Sponsor wallet funded with SUI tokens")
    print("  • SUI_PACKAGE_ID configured (after contract deployment)")
    print("=" * 70)
    
    try:
        success = example_sponsored_transaction_flow()
        
        if success:
            print("\n✓ Example completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ Example failed. Please check configuration.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
