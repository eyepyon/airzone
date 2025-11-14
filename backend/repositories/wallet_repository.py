"""
Wallet repository for managing Sui blockchain wallet data access.
Provides custom queries for finding wallets by user and address.

Requirements: 1.3
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.wallet import Wallet
from repositories.base import BaseRepository


class WalletRepository(BaseRepository[Wallet]):
    """
    Repository for Wallet model with custom query methods.
    Handles wallet creation and lookup operations for Sui blockchain integration.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize WalletRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Wallet, db_session)
    
    def find_by_user_id(self, user_id: str) -> Optional[Wallet]:
        """
        Find a wallet by user ID.
        Each user should have exactly one wallet.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Optional[Wallet]: Wallet instance if found, None otherwise
            
        Requirements: 1.3 - Wallet management for users
        """
        return self.db_session.query(Wallet).filter(
            Wallet.user_id == user_id
        ).first()
    
    def find_by_address(self, address: str) -> Optional[Wallet]:
        """
        Find a wallet by its blockchain address.
        Used for wallet lookup and verification.
        
        Args:
            address: Sui blockchain wallet address
            
        Returns:
            Optional[Wallet]: Wallet instance if found, None otherwise
            
        Requirements: 1.3 - Wallet address lookup
        """
        return self.db_session.query(Wallet).filter(
            Wallet.address == address
        ).first()
    
    def find_all_by_user_id(self, user_id: str) -> List[Wallet]:
        """
        Find all wallets associated with a user.
        While typically one wallet per user, this supports future multi-wallet scenarios.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            List[Wallet]: List of wallet instances
        """
        return self.db_session.query(Wallet).filter(
            Wallet.user_id == user_id
        ).all()
    
    def create_wallet(self, user_id: str, address: str, private_key_encrypted: str) -> Wallet:
        """
        Create a new wallet for a user.
        
        Args:
            user_id: User's unique identifier
            address: Sui blockchain wallet address
            private_key_encrypted: Encrypted private key
            
        Returns:
            Wallet: Created wallet instance
            
        Requirements: 1.3 - Create Sui wallet on user registration
        """
        return self.create(
            user_id=user_id,
            address=address,
            private_key_encrypted=private_key_encrypted
        )
    
    def address_exists(self, address: str) -> bool:
        """
        Check if a wallet address already exists.
        
        Args:
            address: Sui blockchain wallet address to check
            
        Returns:
            bool: True if address exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(Wallet).filter(
                Wallet.address == address
            ).exists()
        ).scalar()
    
    def user_has_wallet(self, user_id: str) -> bool:
        """
        Check if a user already has a wallet.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            bool: True if user has a wallet, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(Wallet).filter(
                Wallet.user_id == user_id
            ).exists()
        ).scalar()
