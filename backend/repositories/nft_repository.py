"""
NFT Repository for managing NFT mint records.
Provides specialized queries for NFT operations.

Requirements: 3.4, 4.2, 4.3
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models.nft_mint import NFTMint, NFTMintStatus
from repositories.base import BaseRepository


class NFTRepository(BaseRepository[NFTMint]):
    """
    Repository for NFT mint operations.
    Provides methods to query NFTs by wallet, status, and other criteria.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize NFT repository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(NFTMint, db_session)
    
    def find_by_wallet(self, wallet_address: str, 
                       status: Optional[NFTMintStatus] = None,
                       limit: Optional[int] = None) -> List[NFTMint]:
        """
        Find all NFTs associated with a wallet address.
        
        Args:
            wallet_address: The wallet address to search for
            status: Optional status filter
            limit: Maximum number of records to return
            
        Returns:
            List[NFTMint]: List of NFT mint records
        """
        query = self.db_session.query(NFTMint).filter(
            NFTMint.wallet_address == wallet_address
        )
        
        if status:
            query = query.filter(NFTMint.status == status)
        
        query = query.order_by(NFTMint.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_status(self, status: NFTMintStatus, 
                       limit: Optional[int] = None) -> List[NFTMint]:
        """
        Find all NFTs with a specific status.
        
        Args:
            status: The status to filter by
            limit: Maximum number of records to return
            
        Returns:
            List[NFTMint]: List of NFT mint records
        """
        query = self.db_session.query(NFTMint).filter(
            NFTMint.status == status
        )
        
        query = query.order_by(NFTMint.created_at.asc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_user(self, user_id: str, 
                     status: Optional[NFTMintStatus] = None,
                     limit: Optional[int] = None) -> List[NFTMint]:
        """
        Find all NFTs for a specific user.
        
        Args:
            user_id: The user ID to search for
            status: Optional status filter
            limit: Maximum number of records to return
            
        Returns:
            List[NFTMint]: List of NFT mint records
        """
        query = self.db_session.query(NFTMint).filter(
            NFTMint.user_id == user_id
        )
        
        if status:
            query = query.filter(NFTMint.status == status)
        
        query = query.order_by(NFTMint.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_transaction_digest(self, transaction_digest: str) -> Optional[NFTMint]:
        """
        Find an NFT by its transaction digest.
        
        Args:
            transaction_digest: The blockchain transaction digest
            
        Returns:
            Optional[NFTMint]: NFT mint record if found, None otherwise
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.transaction_digest == transaction_digest
        ).first()
    
    def find_by_nft_object_id(self, nft_object_id: str) -> Optional[NFTMint]:
        """
        Find an NFT by its object ID on the blockchain.
        
        Args:
            nft_object_id: The NFT object ID on Sui blockchain
            
        Returns:
            Optional[NFTMint]: NFT mint record if found, None otherwise
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.nft_object_id == nft_object_id
        ).first()
    
    def update_status(self, nft_id: str, status: NFTMintStatus, 
                      **kwargs) -> Optional[NFTMint]:
        """
        Update the status of an NFT mint operation.
        
        Args:
            nft_id: The ID of the NFT mint record
            status: The new status
            **kwargs: Additional fields to update (e.g., error_message, nft_object_id)
            
        Returns:
            Optional[NFTMint]: Updated NFT mint record if found, None otherwise
        """
        kwargs['status'] = status
        return self.update(nft_id, **kwargs)
    
    def count_by_status(self, status: NFTMintStatus) -> int:
        """
        Count NFTs with a specific status.
        
        Args:
            status: The status to count
            
        Returns:
            int: Number of NFTs with the given status
        """
        return self.db_session.query(NFTMint).filter(
            NFTMint.status == status
        ).count()
    
    def count_by_user(self, user_id: str, 
                      status: Optional[NFTMintStatus] = None) -> int:
        """
        Count NFTs for a specific user.
        
        Args:
            user_id: The user ID
            status: Optional status filter
            
        Returns:
            int: Number of NFTs for the user
        """
        query = self.db_session.query(NFTMint).filter(
            NFTMint.user_id == user_id
        )
        
        if status:
            query = query.filter(NFTMint.status == status)
        
        return query.count()
    
    def has_completed_nft(self, user_id: str, wallet_address: str) -> bool:
        """
        Check if a user has at least one completed NFT.
        
        Args:
            user_id: The user ID
            wallet_address: The wallet address
            
        Returns:
            bool: True if user has completed NFT, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(NFTMint).filter(
                NFTMint.user_id == user_id,
                NFTMint.wallet_address == wallet_address,
                NFTMint.status == NFTMintStatus.COMPLETED
            ).exists()
        ).scalar()
