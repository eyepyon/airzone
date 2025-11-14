#!/usr/bin/env python3
"""
Generate a Sui sponsor wallet for the Airzone NFT system.

This script generates a new Sui wallet that will be used as the sponsor
wallet to pay gas fees for NFT minting transactions.

Requirements: 3.3 - Sponsored transactions
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from clients.sui_client import SuiClient


def generate_sponsor_wallet():
    """Generate a new sponsor wallet and display instructions."""
    print("=" * 70)
    print("Airzone NFT Sponsor Wallet Generator")
    print("=" * 70)
    print()
    print("This script generates a new Sui wallet to be used as the sponsor")
    print("wallet for NFT minting. The sponsor wallet pays gas fees for users.")
    print()
    
    # Get network choice
    print("Select network:")
    print("  1. Testnet (recommended for development)")
    print("  2. Devnet")
    print("  3. Mainnet (production only)")
    print()
    
    choice = input("Enter choice (1-3) [1]: ").strip() or "1"
    
    network_map = {
        "1": "testnet",
        "2": "devnet",
        "3": "mainnet"
    }
    
    network = network_map.get(choice, "testnet")
    
    print()
    print(f"Generating wallet for {network}...")
    print()
    
    try:
        # Initialize Sui client
        client = SuiClient(network=network)
        
        # Generate wallet
        address, private_key = client.generate_wallet()
        
        print("=" * 70)
        print("Wallet Generated Successfully!")
        print("=" * 70)
        print()
        print(f"Network:      {network}")
        print(f"Address:      {address}")
        print(f"Private Key:  {private_key}")
        print()
        print("⚠️  IMPORTANT: Keep the private key secure and never share it!")
        print()
        
        # Check balance
        balance = client.get_wallet_balance(address)
        sui_balance = balance / 1_000_000_000  # Convert MIST to SUI
        
        print(f"Current Balance: {balance} MIST ({sui_balance:.4f} SUI)")
        print()
        
        if balance == 0:
            print("=" * 70)
            print("Fund Your Sponsor Wallet")
            print("=" * 70)
            print()
            
            if network in ["testnet", "devnet"]:
                print("Get test tokens from the faucet:")
                print()
                print(f"  curl --location --request POST 'https://faucet.{network}.sui.io/gas' \\")
                print(f"    --header 'Content-Type: application/json' \\")
                print(f"    --data-raw '{{\"FixedAmountRequest\":{{\"recipient\":\"{address}\"}}}}'")
                print()
                print("Or use the Sui CLI:")
                print(f"  sui client faucet --address {address}")
                print()
            else:
                print("Transfer SUI tokens to this address to fund the sponsor wallet.")
                print("Recommended: At least 10 SUI for production use.")
                print()
        
        print("=" * 70)
        print("Configuration")
        print("=" * 70)
        print()
        print("Add the following to your backend/.env file:")
        print()
        print(f"SUI_NETWORK={network}")
        print(f"SUI_SPONSOR_PRIVATE_KEY={private_key}")
        print()
        print("=" * 70)
        print("Next Steps")
        print("=" * 70)
        print()
        print("1. Fund the sponsor wallet (see instructions above)")
        print("2. Add the configuration to backend/.env")
        print("3. Deploy the NFT smart contract:")
        print(f"   bash scripts/deploy_contract.sh {network}")
        print("4. Test NFT minting:")
        print("   python backend/verify_sui_client.py")
        print()
        
        # Save to file option
        save = input("Save wallet details to file? (y/N): ").strip().lower()
        if save == 'y':
            filename = f"sponsor_wallet_{network}.txt"
            with open(filename, 'w') as f:
                f.write(f"Airzone NFT Sponsor Wallet\n")
                f.write(f"=" * 70 + "\n")
                f.write(f"\n")
                f.write(f"Network:      {network}\n")
                f.write(f"Address:      {address}\n")
                f.write(f"Private Key:  {private_key}\n")
                f.write(f"\n")
                f.write(f"⚠️  KEEP THIS FILE SECURE AND NEVER COMMIT TO VERSION CONTROL!\n")
                f.write(f"\n")
                f.write(f"Configuration for backend/.env:\n")
                f.write(f"SUI_NETWORK={network}\n")
                f.write(f"SUI_SPONSOR_PRIVATE_KEY={private_key}\n")
            
            print(f"\n✓ Wallet details saved to {filename}")
            print(f"⚠️  Remember to keep this file secure!")
        
        print()
        print("✓ Sponsor wallet generation complete!")
        
    except Exception as e:
        print(f"\n❌ Error generating wallet: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    generate_sponsor_wallet()
