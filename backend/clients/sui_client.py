"""
Sui blockchain client for wallet generation and NFT minting.
Handles Sui blockchain interactions including wallet creation and NFT transactions.

Requirements: 1.3, 3.2, 3.3
"""
from typing import Dict, Optional, Tuple, List
import logging
import os

from pysui import SuiConfig, SyncClient
from pysui.sui.sui_types.scalars import ObjectID, SuiString
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_crypto import keypair_from_keystring, SuiKeyPair, SignatureScheme


logger = logging.getLogger(__name__)


class SuiClient:
    """
    Client for Sui blockchain operations.
    Handles wallet generation, NFT minting, and sponsored transactions.
    
    Uses pysui library for full Sui blockchain integration.
    """
    
    def __init__(self, network: str = 'testnet', sponsor_private_key: Optional[str] = None):
        """
        Initialize SuiClient with network configuration.
        
        Args:
            network: Sui network to connect to ('testnet', 'devnet', 'mainnet')
            sponsor_private_key: Private key for sponsored transactions (keystring format)
        """
        self.network = network
        self.sponsor_private_key = sponsor_private_key
        
        # Initialize Sui configuration based on network
        if network == 'mainnet':
            self.config = SuiConfig.default_config()
        elif network == 'devnet':
            self.config = SuiConfig.devnet_config()
        else:  # testnet (default)
            self.config = SuiConfig.testnet_config()
        
        # Initialize synchronous client
        self.client = SyncClient(self.config)
        
        # Initialize sponsor keypair if provided
        self.sponsor_keypair = None
        if sponsor_private_key:
            try:
                self.sponsor_keypair = keypair_from_keystring(sponsor_private_key)
                logger.info(f"Initialized sponsor keypair: {self.sponsor_keypair.to_address()}")
            except Exception as e:
                logger.error(f"Failed to initialize sponsor keypair: {str(e)}")
                raise ValueError(f"Invalid sponsor private key: {str(e)}")
        
        logger.info(f"Initialized SuiClient for network: {network}")
    
    def generate_wallet(self) -> Tuple[str, str]:
        """
        Generate a new Sui wallet with address and private key.
        
        Returns:
            Tuple[str, str]: (wallet_address, private_key_keystring)
            
        Requirements: 1.3 - Generate Sui wallet for new users
        
        The private key is returned in keystring format (e.g., "suiprivkey1q...")
        which can be used to reconstruct the keypair later.
        """
        try:
            # Generate a new Ed25519 keypair
            keypair = SuiKeyPair.create_new_keypair(SignatureScheme.ED25519)
            
            # Get wallet address
            wallet_address = keypair.to_address()
            
            # Get private key in keystring format
            private_key_keystring = keypair.to_keystring()
            
            logger.info(f"Generated new Sui wallet: {wallet_address}")
            return wallet_address, private_key_keystring
            
        except Exception as e:
            logger.error(f"Failed to generate wallet: {str(e)}")
            raise Exception(f"Wallet generation failed: {str(e)}")
    
    def mint_nft(
        self, 
        recipient_address: str, 
        nft_metadata: Dict,
        package_id: str,
        module_name: str = "nft",
        function_name: str = "mint",
        use_sponsored_transaction: bool = True
    ) -> Dict:
        """
        Mint an NFT on the Sui blockchain by calling a Move smart contract.
        
        Args:
            recipient_address: Wallet address to receive the NFT
            nft_metadata: NFT metadata (name, description, image_url, etc.)
            package_id: Sui package ID containing the NFT minting module
            module_name: Name of the Move module (default: "nft")
            function_name: Name of the minting function (default: "mint")
            use_sponsored_transaction: Whether to use sponsored transaction (gas paid by sponsor)
            
        Returns:
            Dict: Transaction result with nft_object_id and transaction_digest
            
        Requirements: 
            - 3.2 - Call Move smart contract for NFT minting
            - 3.3 - Use sponsor wallet for gas fees
        """
        try:
            # Validate inputs
            if not recipient_address or not recipient_address.startswith('0x'):
                raise ValueError("Invalid recipient address")
            
            if not nft_metadata:
                raise ValueError("NFT metadata is required")
            
            if not package_id:
                raise ValueError("Package ID is required")
            
            # Validate sponsor keypair if sponsored transaction is requested
            if use_sponsored_transaction and not self.sponsor_keypair:
                raise ValueError("Sponsor keypair not configured for sponsored transactions")
            
            # Create transaction
            txn = SyncTransaction(client=self.client, initial_sender=SuiAddress(recipient_address))
            
            # Build Move call arguments
            # Note: Adjust arguments based on your actual Move contract signature
            name = nft_metadata.get('name', 'Airzone NFT')
            description = nft_metadata.get('description', '')
            image_url = nft_metadata.get('image_url', '')
            
            # Call the Move function to mint NFT
            # Example: public entry fun mint(name: String, description: String, url: String, ctx: &mut TxContext)
            txn.move_call(
                target=f"{package_id}::{module_name}::{function_name}",
                arguments=[
                    SuiString(name),
                    SuiString(description),
                    SuiString(image_url)
                ]
            )
            
            # Execute transaction
            if use_sponsored_transaction:
                # Set sponsor for the transaction
                txn.sponsor = self.sponsor_keypair.to_address()
                
                # Build and sign transaction with sponsor
                result = txn.execute(
                    gas_budget="10000000"  # 0.01 SUI
                )
            else:
                # Execute without sponsor (recipient pays gas)
                result = txn.execute(
                    gas_budget="10000000"
                )
            
            # Check if transaction was successful
            if not result.is_ok():
                error_msg = result.result_data.get('error', 'Unknown error')
                raise Exception(f"Transaction failed: {error_msg}")
            
            # Extract transaction details
            tx_digest = result.result_data.get('digest', '')
            
            # Get created objects (NFT object ID)
            created_objects = result.result_data.get('effects', {}).get('created', [])
            nft_object_id = None
            if created_objects:
                nft_object_id = created_objects[0].get('reference', {}).get('objectId', '')
            
            response = {
                'nft_object_id': nft_object_id,
                'transaction_digest': tx_digest,
                'recipient': recipient_address,
                'metadata': nft_metadata,
                'sponsored': use_sponsored_transaction,
                'network': self.network,
                'status': 'success'
            }
            
            logger.info(
                f"Minted NFT for {recipient_address}: "
                f"object_id={nft_object_id}, tx={tx_digest}"
            )
            
            return response
            
        except ValueError as e:
            logger.error(f"Invalid parameters for NFT minting: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to mint NFT: {str(e)}")
            raise Exception(f"NFT minting failed: {str(e)}")
    
    def create_sponsored_transaction(
        self,
        recipient_address: str,
        move_calls: List[Dict],
        gas_budget: str = "10000000"
    ) -> SyncTransaction:
        """
        Create a sponsored transaction where gas fees are paid by the sponsor wallet.
        
        Args:
            recipient_address: Address of the transaction recipient (signer)
            move_calls: List of Move call configurations, each containing:
                - target: "package_id::module::function"
                - arguments: List of arguments for the function
            gas_budget: Gas budget for the transaction (default: 0.01 SUI)
            
        Returns:
            SyncTransaction: Sponsored transaction ready for execution
            
        Requirements: 3.3 - Implement sponsored transactions
        
        Example:
            move_calls = [{
                'target': '0xabc::nft::mint',
                'arguments': [SuiString('NFT Name'), SuiString('Description')]
            }]
        """
        try:
            if not self.sponsor_keypair:
                raise ValueError("Sponsor keypair not configured")
            
            # Create transaction with recipient as initial sender
            txn = SyncTransaction(
                client=self.client,
                initial_sender=SuiAddress(recipient_address)
            )
            
            # Add Move calls to transaction
            for call in move_calls:
                target = call.get('target')
                arguments = call.get('arguments', [])
                
                if not target:
                    raise ValueError("Move call target is required")
                
                txn.move_call(target=target, arguments=arguments)
            
            # Set sponsor for the transaction
            txn.sponsor = self.sponsor_keypair.to_address()
            
            logger.info(
                f"Created sponsored transaction for {recipient_address} "
                f"with sponsor {self.sponsor_keypair.to_address()}"
            )
            
            return txn
            
        except Exception as e:
            logger.error(f"Failed to create sponsored transaction: {str(e)}")
            raise Exception(f"Sponsored transaction creation failed: {str(e)}")
    
    def get_nft_details(self, nft_object_id: str) -> Optional[Dict]:
        """
        Get details of an NFT by its object ID.
        
        Args:
            nft_object_id: NFT object ID on Sui blockchain
            
        Returns:
            Optional[Dict]: NFT details if found, None otherwise
        """
        try:
            logger.info(f"Querying NFT details for: {nft_object_id}")
            
            # Query object from Sui blockchain
            result = self.client.get_object(ObjectID(nft_object_id))
            
            if not result.is_ok():
                logger.warning(f"NFT object not found: {nft_object_id}")
                return None
            
            obj_data = result.result_data
            
            # Extract NFT details
            nft_details = {
                'object_id': nft_object_id,
                'owner': obj_data.get('owner', {}).get('AddressOwner', ''),
                'type': obj_data.get('type', ''),
                'version': obj_data.get('version', ''),
                'digest': obj_data.get('digest', ''),
                'metadata': obj_data.get('content', {}).get('fields', {}),
                'network': self.network
            }
            
            return nft_details
            
        except Exception as e:
            logger.error(f"Failed to get NFT details: {str(e)}")
            return None
    
    def verify_nft_ownership(self, wallet_address: str, nft_object_id: str) -> bool:
        """
        Verify if a wallet owns a specific NFT.
        
        Args:
            wallet_address: Wallet address to check
            nft_object_id: NFT object ID to verify
            
        Returns:
            bool: True if wallet owns the NFT, False otherwise
        """
        try:
            nft_details = self.get_nft_details(nft_object_id)
            
            if not nft_details:
                logger.warning(f"NFT not found: {nft_object_id}")
                return False
            
            owner = nft_details.get('owner', '')
            is_owner = owner == wallet_address
            
            logger.info(
                f"NFT ownership verification: {nft_object_id} "
                f"owned by {owner}, checking against {wallet_address}: {is_owner}"
            )
            
            return is_owner
            
        except Exception as e:
            logger.error(f"Failed to verify NFT ownership: {str(e)}")
            return False
    
    def get_wallet_nfts(self, wallet_address: str, nft_type: Optional[str] = None) -> List[Dict]:
        """
        Get all NFTs owned by a wallet address.
        
        Args:
            wallet_address: Wallet address to query
            nft_type: Optional NFT type filter (e.g., "0xabc::nft::NFT")
            
        Returns:
            List[Dict]: List of NFT details owned by the wallet
        """
        try:
            logger.info(f"Querying NFTs for wallet: {wallet_address}")
            
            # Get all objects owned by the address
            result = self.client.get_objects_owned_by_address(SuiAddress(wallet_address))
            
            if not result.is_ok():
                logger.warning(f"Failed to query objects for wallet: {wallet_address}")
                return []
            
            owned_objects = result.result_data
            nfts = []
            
            # Filter for NFT objects
            for obj in owned_objects:
                obj_type = obj.get('type', '')
                obj_id = obj.get('objectId', '')
                
                # If nft_type filter is provided, check if object matches
                if nft_type and nft_type not in obj_type:
                    continue
                
                # Get detailed NFT information
                nft_details = self.get_nft_details(obj_id)
                if nft_details:
                    nfts.append(nft_details)
            
            logger.info(f"Found {len(nfts)} NFTs for wallet: {wallet_address}")
            return nfts
            
        except Exception as e:
            logger.error(f"Failed to get wallet NFTs: {str(e)}")
            return []
    
    def get_wallet_balance(self, wallet_address: str) -> int:
        """
        Get the SUI balance of a wallet address.
        
        Args:
            wallet_address: Wallet address to query
            
        Returns:
            int: Balance in MIST (1 SUI = 1,000,000,000 MIST)
        """
        try:
            logger.info(f"Querying balance for wallet: {wallet_address}")
            
            result = self.client.get_balance(SuiAddress(wallet_address))
            
            if not result.is_ok():
                logger.warning(f"Failed to query balance for wallet: {wallet_address}")
                return 0
            
            balance = int(result.result_data.get('totalBalance', 0))
            logger.info(f"Wallet {wallet_address} balance: {balance} MIST")
            
            return balance
            
        except Exception as e:
            logger.error(f"Failed to get wallet balance: {str(e)}")
            return 0
