"""
Fund sponsor wallet from testnet faucet
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from clients.xrpl_client import XRPLClient

# Load environment variables
load_dotenv()


def fund_from_faucet(address: str, network: str = 'testnet') -> bool:
    """
    Request funds from XRPL testnet faucet
    
    Args:
        address: XRPL address to fund
        network: Network (testnet or devnet)
        
    Returns:
        bool: True if successful
    """
    if network == 'testnet':
        faucet_url = 'https://faucet.altnet.rippletest.net/accounts'
    elif network == 'devnet':
        faucet_url = 'https://faucet.devnet.rippletest.net/accounts'
    else:
        print(f"✗ Invalid network: {network}")
        return False
    
    print(f"\nRequesting funds from {network} faucet...")
    print(f"Address: {address}")
    
    try:
        response = requests.post(
            faucet_url,
            json={'destination': address},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Funds received!")
            print(f"  Amount: {data.get('amount', 'Unknown')} XRP")
            print(f"  Balance: {data.get('balance', 'Unknown')} drops")
            return True
        else:
            print(f"✗ Faucet request failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error requesting funds: {str(e)}")
        return False


def main():
    """Fund sponsor wallet"""
    print("="*60)
    print("XRPL Sponsor Wallet Funding")
    print("="*60)
    
    # Get configuration
    xrpl_network = os.getenv('XRPL_NETWORK', 'testnet')
    xrpl_sponsor_seed = os.getenv('XRPL_SPONSOR_SEED')
    
    if not xrpl_sponsor_seed:
        print("\n✗ XRPL_SPONSOR_SEED not configured in .env")
        return 1
    
    # Initialize XRPL client
    try:
        xrpl_client = XRPLClient(
            network=xrpl_network,
            sponsor_seed=xrpl_sponsor_seed
        )
        
        sponsor_address = xrpl_client.sponsor_wallet.classic_address
        
        print(f"\nNetwork: {xrpl_network}")
        print(f"Sponsor Address: {sponsor_address}")
        
        # Check current balance
        print("\nChecking current balance...")
        balance = xrpl_client.get_sponsor_balance()
        balance_xrp = balance / 1_000_000
        print(f"Current Balance: {balance_xrp} XRP ({balance} drops)")
        
        # Check if funding is needed
        if balance_xrp >= 100:
            print(f"\n✓ Sponsor wallet has sufficient funds ({balance_xrp} XRP)")
            print("  No funding needed.")
            return 0
        
        # Request funds from faucet
        if xrpl_network in ['testnet', 'devnet']:
            print(f"\n⚠ Balance is low ({balance_xrp} XRP)")
            print("  Requesting funds from faucet...")
            
            success = fund_from_faucet(sponsor_address, xrpl_network)
            
            if success:
                # Check new balance
                print("\nChecking new balance...")
                import time
                time.sleep(2)  # Wait for transaction to settle
                
                new_balance = xrpl_client.get_sponsor_balance()
                new_balance_xrp = new_balance / 1_000_000
                print(f"New Balance: {new_balance_xrp} XRP ({new_balance} drops)")
                
                # Check health
                health = xrpl_client.check_sponsor_health()
                print(f"\nSponsor Health: {'✓ Healthy' if health['healthy'] else '✗ Unhealthy'}")
                
                if health.get('warnings'):
                    for warning in health['warnings']:
                        print(f"  {warning}")
                
                if health.get('recommendations'):
                    print("\nRecommendations:")
                    for rec in health['recommendations']:
                        print(f"  • {rec}")
                
                print("\n✓ Sponsor wallet funded successfully!")
                return 0
            else:
                print("\n✗ Failed to fund sponsor wallet")
                print("\nManual funding options:")
                print(f"  1. Visit: https://xrpl.org/xrp-testnet-faucet.html")
                print(f"  2. Enter address: {sponsor_address}")
                print(f"  3. Click 'Get Testnet XRP'")
                return 1
        else:
            print(f"\n⚠ Mainnet detected - cannot use faucet")
            print(f"  Please fund manually: {sponsor_address}")
            return 1
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
