"""
Sui Blockchain client for wallet generation and NFT minting.
Handles Sui blockchain interactions including wallet creation,
NFT minting transactions, and sponsored transactions.

This client provides the following functionality:
1. Wallet Generation: Create new Sui wallets with address and private key
2. NFT Minting: Mint NFTs on Sui blockchain with sponsored transactions
3. Sponsored Transactions: Allow sponsor wallet to pay gas fees for users
4. NFT Verification: Verify NFT ownership and retrieve metadata
5. Balance Queries: Check wallet balances and owned objects

Requirements:
- 1.3: Automatic Sui wallet creation for new users
- 3.2: NFT minting via Move smart contract
- 3.3: Sponsored transactions (sponsor pays gas fees)

Note: Full NFT minting functionality requires a deployed Move smart contract.
The current implementation provides the infrastructure and will be completed
once the Move contract is deployed to the Sui network.
"""
from typing import Dict, Optional, Tuple
from pysui import SuiConfig, SyncClient
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_crypto import keypair_from_keystring, SuiKeyPair
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_builders.get_builders import GetObjectsOwnedByAddress
import logging
import json


logger = logging.getLogger(__name__)


class SuiClient:
    """
    Client for Sui blockchain operations.
    Handles wallet generation, NFT minting, and sponsored transactions.
    """
    
    def __init__(self, network: str = 'testnet', sponsor_private_key: Optional[str] = None):
        """
        Initialize SuiClient with network configuration.
        
        Args:
            network: Sui network to connect to ('testnet', 'devnet', 'mainnet')
            sponsor_private_key: Private key for sponsoring transactions (gas fee payment)
            
        Requirements: 1.3, 3.2, 3.3
        """
        self.network = network
        self.sponsor_private_key = sponsor_private_key
        
        # Initialize Sui configuration
        if network == 'testnet':
            self.config = SuiConfig.testnet_config()
        elif network == 'devnet':
            self.config = SuiConfig.devnet_config()
        elif network == 'mainnet':
            self.config = SuiConfig.mainnet_config()
        else:
            raise ValueError(f"Invalid network: {network}. Must be 'testnet', 'devnet', or 'mainnet'")
        
        # Initialize sync client
        self.client = SyncClient(self.config)
        
        # Initialize sponsor keypair if provided
        self.sponsor_keypair = None
        if sponsor_private_key:
            try:
                self.sponsor_keypair = keypair_from_keystring(sponsor_private_key)
                logger.info(f"Initialized Sui client on {network} with sponsor wallet")
            except Exception as e:
                logger.error(f"Failed to initialize sponsor keypair: {str(e)}")
                raise ValueError(f"Invalid sponsor private key: {str(e)}")
        else:
            logger.info(f"Initialized Sui client on {network} without sponsor wallet")
    
    def generate_wallet(self) -> Tuple[str, str]:
        """
        Generate a new Sui wallet with address and private key.
        
        Returns:
            Tuple[str, str]: (wallet_address, private_key_string)
            
        Requirements: 1.3 - Automatic Sui wallet creation for new users
        """
        try:
            # Generate new keypair
            keypair = SuiKeyPair.generate()
            
            # Get address and private key
            address = keypair.to_address()
            private_key = keypair.to_keystring()
            
            logger.info(f"Generated new Sui wallet: {address}")
            return (str(address), private_key)
            
        except Exception as e:
            logger.error(f"Failed to generate wallet: {str(e)}")
            raise Exception(f"Wallet generation failed: {str(e)}")
    
    def get_wallet_balance(self, address: str) -> int:
        """
        Get the SUI token balance for a wallet address.
        
        Args:
            address: Sui wallet address
            
        Returns:
            int: Balance in MIST (1 SUI = 1,000,000,000 MIST)
        """
        try:
            sui_address = SuiAddress(address)
            result = self.client.get_gas(sui_address)
            
            if result.is_ok():
                total_balance = sum(coin.balance for coin in result.result_data.data)
                logger.info(f"Retrieved balance for {address}: {total_balance} MIST")
                return total_balance
            else:
                logger.error(f"Failed to get balance: {result.result_string}")
                return 0
                
        except Exception as e:
            logger.error(f"Error getting wallet balance: {str(e)}")
            return 0
    
    def get_owned_objects(self, address: str) -> list:
        """
        Get all objects owned by a wallet address.
        
        Args:
            address: Sui wallet address
            
        Returns:
            list: List of owned objects
        """
        try:
            sui_address = SuiAddress(address)
            builder = GetObjectsOwnedByAddress(owner=sui_address)
            result = self.client.execute(builder)
            
            if result.is_ok():
                objects = result.result_data.data
                logger.info(f"Retrieved {len(objects)} objects for {address}")
                return objects
            else:
                logger.error(f"Failed to get owned objects: {result.result_string}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting owned objects: {str(e)}")
            return []
    
    def mint_nft(
        self,
        recipient_address: str,
        nft_name: str,
        nft_description: str,
        nft_image_url: str,
        metadata: Optional[Dict] = None,
        use_sponsor: bool = True
    ) -> Dict:
        """
        Mint an NFT on the Sui blockchain.
        
        Args:
            recipient_address: Address to receive the NFT
            nft_name: Name of the NFT
            nft_description: Description of the NFT
            nft_image_url: URL of the NFT image
            metadata: Additional metadata for the NFT
            use_sponsor: Whether to use sponsored transaction (sponsor pays gas)
            
        Returns:
            Dict: Transaction result with object_id and transaction_digest
            
        Requirements:
            - 3.2: NFT minting via Move smart contract
            - 3.3: Sponsored transactions (sponsor pays gas fees)
        """
        try:
            # Validate recipient address
            recipient = SuiAddress(recipient_address)
            
            # Prepare NFT metadata
            nft_metadata = {
                'name': nft_name,
                'description': nft_description,
                'image_url': nft_image_url,
                'created_at': None,  # Will be set by blockchain
            }
            
            if metadata:
                nft_metadata.update(metadata)
            
            logger.info(f"Minting NFT for {recipient_address}: {nft_name}")
            
            # Create transaction
            txn = SyncTransaction(client=self.client)
            
            # Note: This is a placeholder for the actual Move contract call
            # In production, you would call your deployed Move module's mint function
            # Example: txn.move_call(
            #     target=f"{package_id}::nft::mint",
            #     arguments=[name, description, image_url],
            #     type_arguments=[]
            # )
            
            # For now, we'll create a basic transfer transaction as a placeholder
            # This should be replaced with actual NFT minting logic once the Move contract is deployed
            
            if use_sponsor and self.sponsor_keypair:
                # Sponsored transaction: sponsor pays gas fees
                logger.info("Using sponsored transaction")
                result = self._execute_sponsored_transaction(txn, recipient, nft_metadata)
            else:
                # Regular transaction: recipient pays gas fees
                logger.warning("Sponsored transaction not available, this would require recipient to pay gas")
                raise NotImplementedError(
                    "Non-sponsored NFT minting requires the Move contract to be deployed. "
                    "Please ensure sponsor wallet is configured."
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to mint NFT: {str(e)}")
            raise Exception(f"NFT minting failed: {str(e)}")
    
    def _execute_sponsored_transaction(
        self,
        transaction: SyncTransaction,
        recipient: SuiAddress,
        nft_metadata: Dict
    ) -> Dict:
        """
        Execute a sponsored transaction where the sponsor pays gas fees.
        
        Args:
            transaction: Transaction to execute
            recipient: Recipient address
            nft_metadata: NFT metadata
            
        Returns:
            Dict: Transaction result
            
        Requirements: 3.3 - Sponsored transactions
        """
        try:
            if not self.sponsor_keypair:
                raise ValueError("Sponsor keypair not configured")
            
            # Note: This is a simplified implementation
            # In production, you would:
            # 1. Build the transaction with the Move contract call
            # 2. Set the sponsor as the gas payer
            # 3. Sign with sponsor's keypair
            # 4. Execute the transaction
            
            # Placeholder for actual implementation
            # The actual implementation depends on the deployed Move contract
            logger.info(f"Executing sponsored transaction for recipient: {recipient}")
            
            # This is where you would execute the actual transaction
            # result = transaction.execute(signer=self.sponsor_keypair)
            
            # For now, return a mock result structure
            # This should be replaced with actual transaction execution
            result = {
                'success': True,
                'nft_object_id': None,  # Will be populated by actual transaction
                'transaction_digest': None,  # Will be populated by actual transaction
                'metadata': nft_metadata,
                'message': 'NFT minting transaction prepared (awaiting Move contract deployment)'
            }
            
            logger.info(f"Sponsored transaction prepared successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute sponsored transaction: {str(e)}")
            raise Exception(f"Sponsored transaction failed: {str(e)}")
    
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
            owned_objects = self.get_owned_objects(wallet_address)
            
            # Check if the NFT object ID is in the owned objects
            for obj in owned_objects:
                if hasattr(obj, 'object_id') and str(obj.object_id) == nft_object_id:
                    logger.info(f"Verified NFT ownership: {wallet_address} owns {nft_object_id}")
                    return True
            
            logger.info(f"NFT ownership verification failed: {wallet_address} does not own {nft_object_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying NFT ownership: {str(e)}")
            return False
    
    def get_nft_metadata(self, nft_object_id: str) -> Optional[Dict]:
        """
        Get metadata for a specific NFT object.
        
        Args:
            nft_object_id: NFT object ID
            
        Returns:
            Optional[Dict]: NFT metadata if found, None otherwise
        """
        try:
            # Get object details from blockchain
            result = self.client.get_object(nft_object_id)
            
            if result.is_ok():
                obj_data = result.result_data
                logger.info(f"Retrieved metadata for NFT: {nft_object_id}")
                
                # Extract metadata from object
                # The structure depends on your Move contract implementation
                metadata = {
                    'object_id': nft_object_id,
                    'owner': str(obj_data.owner) if hasattr(obj_data, 'owner') else None,
                    'type': str(obj_data.object_type) if hasattr(obj_data, 'object_type') else None,
                }
                
                return metadata
            else:
                logger.error(f"Failed to get NFT metadata: {result.result_string}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting NFT metadata: {str(e)}")
            return None
    
    def transfer_nft(
        self,
        sender_private_key: str,
        recipient_address: str,
        nft_object_id: str
    ) -> Dict:
        """
        Transfer an NFT from one address to another.
        
        Args:
            sender_private_key: Private key of the sender
            recipient_address: Address to receive the NFT
            nft_object_id: NFT object ID to transfer
            
        Returns:
            Dict: Transaction result
        """
        try:
            # Create keypair from private key
            sender_keypair = keypair_from_keystring(sender_private_key)
            recipient = SuiAddress(recipient_address)
            
            logger.info(f"Transferring NFT {nft_object_id} to {recipient_address}")
            
            # Create transfer transaction
            txn = SyncTransaction(client=self.client)
            
            # Note: Actual implementation depends on your NFT Move contract
            # This is a placeholder for the transfer logic
            
            result = {
                'success': True,
                'transaction_digest': None,  # Will be populated by actual transaction
                'message': 'NFT transfer prepared (awaiting Move contract deployment)'
            }
            
            logger.info(f"NFT transfer prepared successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to transfer NFT: {str(e)}")
            raise Exception(f"NFT transfer failed: {str(e)}")
