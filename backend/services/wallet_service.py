"""
Wallet Service for managing Sui blockchain wallets.
Handles wallet creation, encryption, and retrieval.

Requirements: 1.3, 6.2
"""
from typing import Optional, Dict
import logging
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from repositories.wallet_repository import WalletRepository
from repositories.user_repository import UserRepository
from clients.sui_client import SuiClient


logger = logging.getLogger(__name__)


class WalletService:
    """
    Service for wallet operations.
    Handles Sui wallet generation, private key encryption, and wallet management.
    """
    
    def __init__(
        self,
        db_session: Session,
        sui_client: SuiClient,
        encryption_key: str
    ):
        """
        Initialize WalletService.
        
        Args:
            db_session: SQLAlchemy database session
            sui_client: Sui blockchain client
            encryption_key: Encryption key for private key storage
        """
        self.db_session = db_session
        self.wallet_repo = WalletRepository(db_session)
        self.user_repo = UserRepository(db_session)
        self.sui_client = sui_client
        
        # Initialize Fernet cipher for encryption
        self.cipher = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
    
    def create_wallet(self, user_id: str) -> Dict:
        """
        Create a new Sui wallet for a user.
        Generates wallet address and private key, encrypts private key, and stores in database.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Dict: Wallet information (without private key)
            
        Raises:
            ValueError: If user not found or already has wallet
            Exception: If wallet creation fails
            
        Requirements:
            - 1.3: Automatic Sui wallet creation for new users
            - 6.2: Private key encryption and secure storage
        """
        try:
            # Verify user exists
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            
            # Check if user already has a wallet
            existing_wallet = self.wallet_repo.find_by_user_id(user_id)
            if existing_wallet:
                logger.warning(f"User {user_id} already has a wallet")
                return existing_wallet.to_dict()
            
            # Generate new Sui wallet
            logger.info(f"Generating new Sui wallet for user: {user_id}")
            address, private_key = self.sui_client.generate_wallet()
            
            # Encrypt private key
            encrypted_private_key = self._encrypt_private_key(private_key)
            
            # Create wallet record
            wallet = self.wallet_repo.create_wallet(
                user_id=user_id,
                address=address,
                private_key_encrypted=encrypted_private_key
            )
            
            self.db_session.commit()
            logger.info(f"Created wallet for user {user_id}: {address}")
            
            return wallet.to_dict()
            
        except ValueError as e:
            logger.error(f"Wallet creation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating wallet: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Failed to create wallet: {str(e)}")
    
    def get_user_wallet(self, user_id: str) -> Optional[Dict]:
        """
        Get wallet for a user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Optional[Dict]: Wallet information or None if not found
        """
        wallet = self.wallet_repo.find_by_user_id(user_id)
        if not wallet:
            logger.info(f"No wallet found for user: {user_id}")
            return None
        
        return wallet.to_dict()
    
    def get_wallet_by_address(self, address: str) -> Optional[Dict]:
        """
        Get wallet by blockchain address.
        
        Args:
            address: Sui blockchain wallet address
            
        Returns:
            Optional[Dict]: Wallet information or None if not found
        """
        wallet = self.wallet_repo.find_by_address(address)
        if not wallet:
            logger.info(f"No wallet found for address: {address}")
            return None
        
        return wallet.to_dict()
    
    def get_wallet_balance(self, user_id: str) -> int:
        """
        Get SUI token balance for user's wallet.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            int: Balance in MIST (1 SUI = 1,000,000,000 MIST)
            
        Raises:
            ValueError: If user has no wallet
        """
        wallet = self.wallet_repo.find_by_user_id(user_id)
        if not wallet:
            raise ValueError(f"User {user_id} has no wallet")
        
        balance = self.sui_client.get_wallet_balance(wallet.address)
        logger.info(f"Retrieved balance for user {user_id}: {balance} MIST")
        
        return balance
    
    def get_decrypted_private_key(self, user_id: str) -> str:
        """
        Get decrypted private key for a user's wallet.
        WARNING: This should only be used for internal operations like signing transactions.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            str: Decrypted private key
            
        Raises:
            ValueError: If user has no wallet
            
        Requirements: 6.2 - Private key decryption for transaction signing
        """
        wallet = self.wallet_repo.find_by_user_id(user_id)
        if not wallet:
            raise ValueError(f"User {user_id} has no wallet")
        
        private_key = self._decrypt_private_key(wallet.private_key_encrypted)
        logger.info(f"Decrypted private key for user: {user_id}")
        
        return private_key
    
    def _encrypt_private_key(self, private_key: str) -> str:
        """
        Encrypt a private key using Fernet symmetric encryption.
        
        Args:
            private_key: Plain text private key
            
        Returns:
            str: Encrypted private key
            
        Requirements: 6.2 - Private key encryption
        """
        encrypted = self.cipher.encrypt(private_key.encode())
        return encrypted.decode()
    
    def _decrypt_private_key(self, encrypted_private_key: str) -> str:
        """
        Decrypt an encrypted private key.
        
        Args:
            encrypted_private_key: Encrypted private key
            
        Returns:
            str: Decrypted private key
            
        Requirements: 6.2 - Private key decryption
        """
        decrypted = self.cipher.decrypt(encrypted_private_key.encode())
        return decrypted.decode()
    
    def ensure_user_has_wallet(self, user_id: str) -> Dict:
        """
        Ensure user has a wallet, creating one if necessary.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Dict: Wallet information
        """
        wallet = self.get_user_wallet(user_id)
        if not wallet:
            logger.info(f"User {user_id} has no wallet, creating one")
            wallet = self.create_wallet(user_id)
        
        return wallet
