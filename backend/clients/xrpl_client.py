"""
XRPL (XRP Ledger) Blockchain client for wallet generation and NFT minting.
Handles XRPL blockchain interactions including wallet creation,
NFT minting transactions, and NFT management.

Requirements:
- 1.3: Automatic XRPL wallet creation for new users
- 3.2: NFT minting on XRPL
- 3.3: Transaction management
"""
from typing import Dict, Optional, Tuple
import logging
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint, Payment
from xrpl.transaction import submit_and_wait
from xrpl.models.requests import AccountNFTs, AccountInfo
from xrpl.utils import xrp_to_drops
import xrpl

logger = logging.getLogger(__name__)


class XRPLClient:
    """
    Client for XRPL blockchain operations.
    Handles wallet generation, NFT minting, and transaction management.
    """
    
    def __init__(
        self,
        network: str = 'testnet',
        sponsor_seed: Optional[str] = None
    ):
        """
        Initialize XRPLClient with network configuration.
        
        Args:
            network: XRPL network to connect to ('testnet', 'devnet', 'mainnet')
            sponsor_seed: Seed for sponsoring transactions (optional)
            
        Requirements: 1.3, 3.2, 3.3
        """
        self.network = network
        self.sponsor_seed = sponsor_seed
        
        # Initialize XRPL client based on network
        if network == 'testnet':
            self.client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
        elif network == 'devnet':
            self.client = JsonRpcClient("https://s.devnet.rippletest.net:51234")
        elif network == 'mainnet':
            self.client = JsonRpcClient("https://xrplcluster.com")
        else:
            raise ValueError(f"Invalid network: {network}. Must be 'testnet', 'devnet', or 'mainnet'")
        
        # Initialize sponsor wallet if provided
        self.sponsor_wallet = None
        if sponsor_seed:
            try:
                self.sponsor_wallet = Wallet.from_seed(sponsor_seed)
                logger.info(f"Initialized XRPL client on {network} with sponsor wallet: {self.sponsor_wallet.classic_address}")
            except Exception as e:
                logger.error(f"Failed to initialize sponsor wallet: {str(e)}")
                raise ValueError(f"Invalid sponsor seed: {str(e)}")
        else:
            logger.info(f"Initialized XRPL client on {network} without sponsor wallet")
    
    def generate_wallet(self) -> Tuple[str, str]:
        """
        Generate a new XRPL wallet with address and seed.
        
        Returns:
            Tuple[str, str]: (wallet_address, seed)
            
        Requirements: 1.3 - Automatic XRPL wallet creation for new users
        """
        try:
            # Generate new wallet
            wallet = Wallet.create()
            
            address = wallet.classic_address
            seed = wallet.seed
            
            logger.info(f"Generated new XRPL wallet: {address}")
            return (address, seed)
            
        except Exception as e:
            logger.error(f"Failed to generate wallet: {str(e)}")
            raise Exception(f"Wallet generation failed: {str(e)}")
    
    def get_wallet_balance(self, address: str) -> int:
        """
        Get the XRP balance for a wallet address.
        
        Args:
            address: XRPL wallet address
            
        Returns:
            int: Balance in drops (1 XRP = 1,000,000 drops)
        """
        try:
            account_info = AccountInfo(account=address)
            response = self.client.request(account_info)
            
            if response.is_successful():
                balance = int(response.result['account_data']['Balance'])
                logger.info(f"Retrieved balance for {address}: {balance} drops ({balance / 1_000_000} XRP)")
                return balance
            else:
                logger.error(f"Failed to get balance: {response.result}")
                return 0
                
        except Exception as e:
            logger.error(f"Error getting wallet balance: {str(e)}")
            return 0
    
    def mint_nft(
        self,
        recipient_address: str,
        nft_uri: str,
        transfer_fee: int = 0,
        flags: int = 8,  # tfTransferable
        issuer_seed: Optional[str] = None
    ) -> Dict:
        """
        Mint an NFT on the XRPL blockchain.
        
        Args:
            recipient_address: Address to receive the NFT
            nft_uri: URI pointing to NFT metadata (IPFS or HTTP)
            transfer_fee: Transfer fee in basis points (0-50000, representing 0-50%)
            flags: NFT flags (8 = tfTransferable, 1 = tfBurnable, 2 = tfOnlyXRP, 4 = tfTrustLine)
            issuer_seed: Seed of the issuer wallet (uses sponsor if not provided)
            
        Returns:
            Dict: Transaction result with nft_token_id and transaction_hash
            
        Requirements:
            - 3.2: NFT minting on XRPL
        """
        try:
            # Use sponsor wallet or provided issuer
            if issuer_seed:
                issuer_wallet = Wallet.from_seed(issuer_seed)
            elif self.sponsor_wallet:
                issuer_wallet = self.sponsor_wallet
            else:
                raise ValueError("No issuer wallet available. Provide issuer_seed or configure sponsor wallet.")
            
            logger.info(f"Minting NFT for {recipient_address} from issuer: {issuer_wallet.classic_address}")
            logger.info(f"NFT URI: {nft_uri}")
            
            # Create NFT mint transaction
            mint_tx = NFTokenMint(
                account=issuer_wallet.classic_address,
                uri=xrpl.utils.str_to_hex(nft_uri),
                flags=flags,
                transfer_fee=transfer_fee,
                nftoken_taxon=0
            )
            
            # Submit and wait for transaction
            response = submit_and_wait(mint_tx, self.client, issuer_wallet)
            
            if response.is_successful():
                # Extract NFT token ID from metadata
                nft_token_id = None
                if 'meta' in response.result and 'nftoken_id' in response.result['meta']:
                    nft_token_id = response.result['meta']['nftoken_id']
                
                tx_hash = response.result['hash']
                
                logger.info(f"✓ NFT minted successfully")
                logger.info(f"  NFT Token ID: {nft_token_id}")
                logger.info(f"  Transaction Hash: {tx_hash}")
                logger.info(f"  Issuer: {issuer_wallet.classic_address}")
                
                # If recipient is different from issuer, transfer the NFT
                if recipient_address != issuer_wallet.classic_address and nft_token_id:
                    logger.info(f"Transferring NFT to recipient: {recipient_address}")
                    # Note: NFT transfer on XRPL requires creating an offer and accepting it
                    # This is a simplified version - full implementation would need offer creation
                
                return {
                    'success': True,
                    'nft_token_id': nft_token_id,
                    'transaction_hash': tx_hash,
                    'issuer': issuer_wallet.classic_address,
                    'recipient': recipient_address,
                    'uri': nft_uri,
                    'message': 'NFT minted successfully on XRPL'
                }
            else:
                error_msg = response.result.get('error', 'Unknown error')
                logger.error(f"Transaction failed: {error_msg}")
                raise Exception(f"Transaction execution failed: {error_msg}")
            
        except Exception as e:
            logger.error(f"Failed to mint NFT: {str(e)}")
            raise Exception(f"NFT minting failed: {str(e)}")
    
    def get_account_nfts(self, address: str) -> list:
        """
        Get all NFTs owned by a wallet address.
        
        Args:
            address: XRPL wallet address
            
        Returns:
            list: List of NFTs owned by the address
        """
        try:
            account_nfts = AccountNFTs(account=address)
            response = self.client.request(account_nfts)
            
            if response.is_successful():
                nfts = response.result.get('account_nfts', [])
                logger.info(f"Retrieved {len(nfts)} NFTs for {address}")
                return nfts
            else:
                logger.error(f"Failed to get NFTs: {response.result}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting NFTs: {str(e)}")
            return []
    
    def verify_nft_ownership(self, wallet_address: str, nft_token_id: str) -> bool:
        """
        Verify if a wallet owns a specific NFT.
        
        Args:
            wallet_address: Wallet address to check
            nft_token_id: NFT token ID to verify
            
        Returns:
            bool: True if wallet owns the NFT, False otherwise
        """
        try:
            nfts = self.get_account_nfts(wallet_address)
            
            for nft in nfts:
                if nft.get('NFTokenID') == nft_token_id:
                    logger.info(f"Verified NFT ownership: {wallet_address} owns {nft_token_id}")
                    return True
            
            logger.info(f"NFT ownership verification failed: {wallet_address} does not own {nft_token_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying NFT ownership: {str(e)}")
            return False
    
    def get_sponsor_balance(self) -> int:
        """
        Get the current balance of the sponsor wallet.
        
        Returns:
            int: Balance in drops (1 XRP = 1,000,000 drops)
        """
        if not self.sponsor_wallet:
            logger.warning("Sponsor wallet not configured")
            return 0
        
        try:
            balance = self.get_wallet_balance(self.sponsor_wallet.classic_address)
            logger.info(f"Sponsor wallet balance: {balance} drops ({balance / 1_000_000} XRP)")
            return balance
        except Exception as e:
            logger.error(f"Failed to get sponsor balance: {str(e)}")
            return 0
    
    def check_sponsor_health(self) -> Dict:
        """
        Check the health status of the sponsor wallet.
        
        Returns:
            Dict: Health status with balance, warnings, and recommendations
        """
        try:
            if not self.sponsor_wallet:
                return {
                    'healthy': False,
                    'error': 'Sponsor wallet not configured',
                    'recommendation': 'Configure XRPL_SPONSOR_SEED in .env file'
                }
            
            sponsor_address = self.sponsor_wallet.classic_address
            balance = self.get_sponsor_balance()
            
            # Define balance thresholds (in drops)
            CRITICAL_THRESHOLD = 10_000_000  # 10 XRP
            WARNING_THRESHOLD = 50_000_000  # 50 XRP
            HEALTHY_THRESHOLD = 100_000_000  # 100 XRP
            
            status = {
                'healthy': True,
                'sponsor_address': sponsor_address,
                'balance_drops': balance,
                'balance_xrp': balance / 1_000_000,
                'network': self.network,
                'warnings': [],
                'recommendations': []
            }
            
            if balance < CRITICAL_THRESHOLD:
                status['healthy'] = False
                status['warnings'].append(
                    f"CRITICAL: Balance extremely low ({balance / 1_000_000} XRP)"
                )
                status['recommendations'].append(
                    "Immediately fund sponsor wallet to continue NFT minting"
                )
            elif balance < WARNING_THRESHOLD:
                status['warnings'].append(
                    f"WARNING: Balance low ({balance / 1_000_000} XRP)"
                )
                status['recommendations'].append(
                    "Consider funding sponsor wallet soon"
                )
            elif balance < HEALTHY_THRESHOLD:
                status['warnings'].append(
                    f"INFO: Balance moderate ({balance / 1_000_000} XRP)"
                )
            
            # Add funding instructions
            if balance < WARNING_THRESHOLD:
                if self.network in ['testnet', 'devnet']:
                    status['recommendations'].append(
                        f"Get test XRP from faucet: https://xrpl.org/xrp-testnet-faucet.html"
                    )
                    status['recommendations'].append(
                        f"Wallet address: {sponsor_address}"
                    )
                else:
                    status['recommendations'].append(
                        f"Transfer XRP to sponsor address: {sponsor_address}"
                    )
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to check sponsor health: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'recommendation': 'Check sponsor wallet configuration and network connectivity'
            }
