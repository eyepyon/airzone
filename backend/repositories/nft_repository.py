"""
NFT repository for managing NFT mint data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.nft_mint import NFTMint, NFTMintStatus
from repositories.base import BaseRepository


class NFTRepository(BaseRepository[NFTMint]):
    """
    Repository for NFTMint model operations.
    Provides custom queries for NFT lookup by wallet, user, and status.
    
    Requirements: 3.4, 4.2, 4.3
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize NFTRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(NFTMint, db_session)
    
    def find_by_wallet(self, wallet_address: str) -> List[NFTMint]:
        """
        Find all NFTs associated with a wallet address.
        
        Args:
            wallet_address: Wallet's blockchain address
            
        Returns:
            List[NFTMint]: List of NFT mint instances
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.wallet_address == wallet_address
        ).order_by(NFTMint.created_at.desc()).all()
    
    def find_by_user_id(self, user_id: str) -> List[NFTMint]:
        """
        Find all NFTs belonging to a user.
        
        Args:
            user_id: User's ID
            
        Returns:
            List[NFTMint]: List of NFT mint instances
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.user_id == user_id
        ).order_by(NFTMint.created_at.desc()).all()
    
    def find_by_status(self, status: NFTMintStatus) -> List[NFTMint]:
        """
        Find all NFTs with a specific status.
        
        Args:
            status: NFT mint status to filter by
            
        Returns:
            List[NFTMint]: List of NFT mint instances
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.status == status
        ).order_by(NFTMint.created_at.desc()).all()
    
    def find_by_wallet_and_status(self, wallet_address: str, 
                                   status: NFTMintStatus) -> List[NFTMint]:
        """
        Find NFTs by wallet address and status.
        
        Args:
            wallet_address: Wallet's blockchain address
            status: NFT mint status to filter by
            
        Returns:
            List[NFTMint]: List of NFT mint instances
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.wallet_address == wallet_address,
            NFTMint.status == status
        ).order_by(NFTMint.created_at.desc()).all()
    
    def find_completed_by_wallet(self, wallet_address: str) -> List[NFTMint]:
        """
        Find all completed NFTs for a wallet address.
        
        Args:
            wallet_address: Wallet's blockchain address
            
        Returns:
            List[NFTMint]: List of completed NFT mint instances
        """
        return self.find_by_wallet_and_status(wallet_address, NFTMintStatus.COMPLETED)
    
    def find_by_nft_object_id(self, nft_object_id: str) -> Optional[NFTMint]:
        """
        Find an NFT by its blockchain object ID.
        
        Args:
            nft_object_id: NFT's blockchain object ID
            
        Returns:
            Optional[NFTMint]: NFT mint instance if found, None otherwise
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.nft_object_id == nft_object_id
        ).first()
    
    def find_by_transaction_digest(self, transaction_digest: str) -> Optional[NFTMint]:
        """
        Find an NFT by its transaction digest.
        
        Args:
            transaction_digest: Transaction digest from blockchain
            
        Returns:
            Optional[NFTMint]: NFT mint instance if found, None otherwise
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.transaction_digest == transaction_digest
        ).first()
    
    def update_status(self, nft_id: str, status: NFTMintStatus, 
                     **kwargs) -> Optional[NFTMint]:
        """
        Update the status of an NFT mint.
        
        Args:
            nft_id: NFT mint ID
            status: New status
            **kwargs: Additional fields to update
            
        Returns:
            Optional[NFTMint]: Updated NFT mint instance if found, None otherwise
        """
        kwargs['status'] = status
        return self.update(nft_id, **kwargs)
    
    def count_by_status(self, status: NFTMintStatus) -> int:
        """
        Count NFTs with a specific status.
        
        Args:
            status: NFT mint status to count
            
        Returns:
            int: Number of NFTs with the given status
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.status == status
        ).count()
