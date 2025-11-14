"""
Wallet repository for managing wallet data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.wallet import Wallet
from repositories.base import BaseRepository


class WalletRepository(BaseRepository[Wallet]):
    """
    Repository for Wallet model operations.
    Provides custom queries for wallet lookup by user and address.
    
    Requirements: 1.2, 1.3
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize WalletRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Wallet, db_session)
    
    def find_by_user_id(self, user_id: str) -> List[Wallet]:
        """
        Find all wallets belonging to a user.
        
        Args:
            user_id: User's ID
            
        Returns:
            List[Wallet]: List of wallet instances
        """
        return self.db_session.query(Wallet).filter(
            Wallet.user_id == user_id
        ).all()
    
    def find_by_address(self, address: str) -> Optional[Wallet]:
        """
        Find a wallet by its blockchain address.
        
        Args:
            address: Wallet's blockchain address
            
        Returns:
            Optional[Wallet]: Wallet instance if found, None otherwise
        """
        return self.db_session.query(Wallet).filter(
            Wallet.address == address
        ).first()
    
    def find_primary_wallet(self, user_id: str) -> Optional[Wallet]:
        """
        Find the primary (first) wallet for a user.
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[Wallet]: First wallet instance if found, None otherwise
        """
        return self.db_session.query(Wallet).filter(
            Wallet.user_id == user_id
        ).order_by(Wallet.created_at.asc()).first()
    
    def address_exists(self, address: str) -> bool:
        """
        Check if a wallet address already exists.
        
        Args:
            address: Wallet address to check
            
        Returns:
            bool: True if address exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(Wallet).filter(
                Wallet.address == address
            ).exists()
        ).scalar()
