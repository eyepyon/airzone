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
    
    def __init__(
        self,
        network: str = 'testnet',
        sponsor_private_key: Optional[str] = None,
        package_id: Optional[str] = None
    ):
        """
        Initialize SuiClient with network configuration.
        
        Args:
            network: Sui network to connect to ('testnet', 'devnet', 'mainnet')
            sponsor_private_key: Private key for sponsoring transactions (gas fee payment)
            package_id: Deployed Move package ID for NFT contract
            
        Requirements: 1.3, 3.2, 3.3
        """
        self.network = network
        self.sponsor_private_key = sponsor_private_key
        self.package_id = package_id
        
        # Initialize Sui configuration
        # Use the default configuration for the specified network
        if network == 'testnet':
            self.config = SuiConfig.default_config()
            self.config.rpc_url = "https://fullnode.testnet.sui.io:443"
        elif network == 'devnet':
            self.config = SuiConfig.default_config()
            self.config.rpc_url = "https://fullnode.devnet.sui.io:443"
        elif network == 'mainnet':
            self.config = SuiConfig.default_config()
            self.config.rpc_url = "https://fullnode.mainnet.sui.io:443"
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
        
        # Validate package ID if provided
        if package_id:
            logger.info(f"Using NFT package ID: {package_id}")
        else:
            logger.warning("No package ID provided. NFT minting will not be available until contract is deployed.")
    
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
        Mint an NFT on the Sui blockchain using the deployed Move contract.
        
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
            # Validate package ID is configured
            if not self.package_id:
                raise ValueError(
                    "Package ID not configured. Please deploy the Move contract and set SUI_PACKAGE_ID in .env"
                )
            
            # Validate sponsor is configured for sponsored transactions
            if use_sponsor and not self.sponsor_keypair:
                raise ValueError(
                    "Sponsor keypair not configured. Please set SUI_SPONSOR_PRIVATE_KEY in .env"
                )
            
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
            
            # Call the Move contract's mint function
            # Target format: {package_id}::{module}::{function}
            target = f"{self.package_id}::nft::mint"
            
            # Prepare arguments for the mint function
            # Arguments: name, description, image_url, recipient
            arguments = [
                nft_name.encode('utf-8'),
                nft_description.encode('utf-8'),
                nft_image_url.encode('utf-8'),
                str(recipient)
            ]
            
            logger.info(f"Calling Move function: {target}")
            
            if use_sponsor and self.sponsor_keypair:
                # Sponsored transaction: sponsor pays gas fees
                logger.info("Using sponsored transaction")
                result = self._execute_sponsored_transaction(
                    txn,
                    target,
                    arguments,
                    recipient_address,
                    nft_metadata
                )
            else:
                # Regular transaction: recipient pays gas fees
                logger.warning("Non-sponsored transaction not recommended for this use case")
                raise NotImplementedError(
                    "Non-sponsored NFT minting is not supported. "
                    "Please ensure sponsor wallet is configured."
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to mint NFT: {str(e)}")
            raise Exception(f"NFT minting failed: {str(e)}")
    
    def get_sponsor_balance(self) -> int:
        """
        Get the current balance of the sponsor wallet.
        
        Returns:
            int: Balance in MIST (1 SUI = 1,000,000,000 MIST)
            
        Requirements: 3.3 - Sponsor wallet management
        """
        if not self.sponsor_keypair:
            logger.warning("Sponsor keypair not configured")
            return 0
        
        try:
            sponsor_address = str(self.sponsor_keypair.to_address())
            balance = self.get_wallet_balance(sponsor_address)
            logger.info(f"Sponsor wallet balance: {balance} MIST ({balance / 1_000_000_000:.4f} SUI)")
            return balance
        except Exception as e:
            logger.error(f"Failed to get sponsor balance: {str(e)}")
            return 0
    
    def validate_sponsor_balance(self, required_balance: int = 100_000_000) -> bool:
        """
        Validate that the sponsor wallet has sufficient balance for transactions.
        
        Args:
            required_balance: Minimum required balance in MIST (default: 0.1 SUI)
            
        Returns:
            bool: True if balance is sufficient, False otherwise
            
        Requirements: 3.3 - Sponsor wallet management
        """
        if not self.sponsor_keypair:
            logger.error("Sponsor keypair not configured")
            return False
        
        try:
            current_balance = self.get_sponsor_balance()
            
            if current_balance < required_balance:
                logger.warning(
                    f"Sponsor wallet balance too low: {current_balance} MIST "
                    f"(required: {required_balance} MIST)"
                )
                return False
            
            logger.info(f"Sponsor wallet balance sufficient: {current_balance} MIST")
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate sponsor balance: {str(e)}")
            return False
    
    def estimate_gas_cost(self) -> int:
        """
        Estimate the gas cost for an NFT minting transaction.
        
        Returns:
            int: Estimated gas cost in MIST
            
        Note: This is a conservative estimate. Actual costs may vary.
        """
        # Conservative estimate for NFT minting on Sui
        # Typical NFT mint costs ~0.01-0.05 SUI
        # We use 0.1 SUI as a safe buffer
        return 100_000_000  # 0.1 SUI in MIST
    
    def _execute_sponsored_transaction(
        self,
        transaction: SyncTransaction,
        target: str,
        arguments: list,
        recipient_address: str,
        nft_metadata: Dict
    ) -> Dict:
        """
        Execute a sponsored transaction where the sponsor pays gas fees.
        
        This implements the sponsored transaction pattern where:
        1. The sponsor wallet pays for gas fees
        2. The NFT is minted and transferred to the recipient
        3. The recipient doesn't need any SUI tokens
        4. Sponsor balance is validated before execution
        5. Transaction status is tracked and logged
        
        Args:
            transaction: Transaction to execute
            target: Move function target (package::module::function)
            arguments: Function arguments
            recipient_address: Recipient address
            nft_metadata: NFT metadata
            
        Returns:
            Dict: Transaction result with nft_object_id and transaction_digest
            
        Requirements: 3.3 - Sponsored transactions
        """
        try:
            if not self.sponsor_keypair:
                raise ValueError("Sponsor keypair not configured")
            
            sponsor_address = str(self.sponsor_keypair.to_address())
            
            logger.info(f"Executing sponsored transaction for recipient: {recipient_address}")
            logger.info(f"Sponsor address: {sponsor_address}")
            logger.info(f"Move call target: {target}")
            
            # Validate sponsor balance before executing transaction
            gas_budget = self.estimate_gas_cost()
            
            if not self.validate_sponsor_balance(required_balance=gas_budget):
                raise ValueError(
                    f"Insufficient sponsor wallet balance. "
                    f"Required: {gas_budget} MIST ({gas_budget / 1_000_000_000:.4f} SUI). "
                    f"Please fund the sponsor wallet."
                )
            
            # Build the transaction with the Move contract call
            # The sponsor will pay for gas fees
            logger.info(f"Building Move call transaction...")
            transaction.move_call(
                target=target,
                arguments=arguments,
                type_arguments=[]
            )
            
            # Execute the transaction with sponsor as signer
            # The sponsor pays gas fees, but NFT goes to recipient
            logger.info(f"Executing transaction with gas budget: {gas_budget} MIST ({gas_budget / 1_000_000_000:.4f} SUI)")
            
            result = transaction.execute(
                gas_budget=gas_budget,
                signer=self.sponsor_keypair
            )
            
            # Check if transaction was successful
            if result.is_ok():
                tx_result = result.result_data
                transaction_digest = tx_result.digest if hasattr(tx_result, 'digest') else None
                
                # Extract created objects (the minted NFT)
                created_objects = []
                if hasattr(tx_result, 'effects') and hasattr(tx_result.effects, 'created'):
                    created_objects = tx_result.effects.created
                
                # Get the NFT object ID (first created object)
                nft_object_id = None
                if created_objects and len(created_objects) > 0:
                    nft_object_id = str(created_objects[0].reference.object_id)
                
                # Calculate gas used
                gas_used = 0
                if hasattr(tx_result, 'effects') and hasattr(tx_result.effects, 'gas_used'):
                    gas_used = tx_result.effects.gas_used.computation_cost + \
                              tx_result.effects.gas_used.storage_cost
                
                logger.info(f"✓ NFT minted successfully")
                logger.info(f"  NFT Object ID: {nft_object_id}")
                logger.info(f"  Transaction Digest: {transaction_digest}")
                logger.info(f"  Gas Used: {gas_used} MIST ({gas_used / 1_000_000_000:.6f} SUI)")
                logger.info(f"  Recipient: {recipient_address}")
                logger.info(f"  Sponsor: {sponsor_address}")
                
                # Get updated sponsor balance
                remaining_balance = self.get_sponsor_balance()
                logger.info(f"  Sponsor Balance After: {remaining_balance} MIST ({remaining_balance / 1_000_000_000:.4f} SUI)")
                
                return {
                    'success': True,
                    'nft_object_id': nft_object_id,
                    'transaction_digest': transaction_digest,
                    'gas_used': gas_used,
                    'metadata': nft_metadata,
                    'recipient': recipient_address,
                    'sponsor': sponsor_address,
                    'sponsor_balance_after': remaining_balance,
                    'message': 'NFT minted successfully with sponsored transaction'
                }
            else:
                error_msg = result.result_string if hasattr(result, 'result_string') else 'Unknown error'
                logger.error(f"Transaction failed: {error_msg}")
                raise Exception(f"Transaction execution failed: {error_msg}")
            
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
    
    def check_sponsor_health(self) -> Dict:
        """
        Check the health status of the sponsor wallet.
        
        Returns:
            Dict: Health status with balance, warnings, and recommendations
            
        Requirements: 3.3 - Sponsor wallet management
        """
        try:
            if not self.sponsor_keypair:
                return {
                    'healthy': False,
                    'error': 'Sponsor keypair not configured',
                    'recommendation': 'Configure SUI_SPONSOR_PRIVATE_KEY in .env file'
                }
            
            sponsor_address = str(self.sponsor_keypair.to_address())
            balance = self.get_sponsor_balance()
            
            # Define balance thresholds
            CRITICAL_THRESHOLD = 50_000_000  # 0.05 SUI
            WARNING_THRESHOLD = 500_000_000  # 0.5 SUI
            HEALTHY_THRESHOLD = 1_000_000_000  # 1 SUI
            
            status = {
                'healthy': True,
                'sponsor_address': sponsor_address,
                'balance_mist': balance,
                'balance_sui': balance / 1_000_000_000,
                'network': self.network,
                'warnings': [],
                'recommendations': []
            }
            
            # Check balance levels
            if balance < CRITICAL_THRESHOLD:
                status['healthy'] = False
                status['warnings'].append(
                    f"CRITICAL: Balance extremely low ({balance / 1_000_000_000:.6f} SUI)"
                )
                status['recommendations'].append(
                    "Immediately fund sponsor wallet to continue NFT minting"
                )
            elif balance < WARNING_THRESHOLD:
                status['warnings'].append(
                    f"WARNING: Balance low ({balance / 1_000_000_000:.4f} SUI)"
                )
                status['recommendations'].append(
                    "Consider funding sponsor wallet soon"
                )
            elif balance < HEALTHY_THRESHOLD:
                status['warnings'].append(
                    f"INFO: Balance moderate ({balance / 1_000_000_000:.4f} SUI)"
                )
            
            # Estimate remaining transactions
            estimated_gas_per_tx = self.estimate_gas_cost()
            estimated_remaining_txs = balance // estimated_gas_per_tx if balance > 0 else 0
            
            status['estimated_remaining_transactions'] = estimated_remaining_txs
            
            if estimated_remaining_txs < 10:
                status['warnings'].append(
                    f"Only ~{estimated_remaining_txs} transactions remaining"
                )
            
            # Add funding instructions
            if balance < WARNING_THRESHOLD:
                if self.network in ['testnet', 'devnet']:
                    status['recommendations'].append(
                        f"Get test tokens: curl --location --request POST "
                        f"'https://faucet.{self.network}.sui.io/gas' "
                        f"--header 'Content-Type: application/json' "
                        f"--data-raw '{{\"FixedAmountRequest\":{{\"recipient\":\"{sponsor_address}\"}}}}''"
                    )
                else:
                    status['recommendations'].append(
                        f"Transfer SUI tokens to sponsor address: {sponsor_address}"
                    )
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to check sponsor health: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'recommendation': 'Check sponsor wallet configuration and network connectivity'
            }
    
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
