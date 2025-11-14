"""
NFT Mint model for tracking NFT minting operations.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Enum, Index, JSON
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum


class NFTMintStatus(enum.Enum):
    """Enum for NFT mint status"""
    PENDING = 'pending'
    MINTING = 'minting'
    COMPLETED = 'completed'
    FAILED = 'failed'


class NFTMint(BaseModel):
    """
    NFT Mint model representing an NFT minting operation.
    Tracks the status of NFT minting from request to completion.
    """
    __tablename__ = 'nft_mints'
    
    # NFT Mint fields
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    wallet_address = Column(String(255), nullable=False)
    nft_object_id = Column(String(255), nullable=True)
    transaction_digest = Column(String(255), nullable=True)
    status = Column(
        Enum(NFTMintStatus),
        default=NFTMintStatus.PENDING,
        nullable=False
    )
    nft_metadata = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='nft_mints')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_wallet_address', 'wallet_address'),
        Index('idx_status', 'status'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert NFT mint to dictionary.
        
        Args:
            exclude_fields (list): Fields to exclude
            
        Returns:
            dict: NFT mint data dictionary
        """
        result = super().to_dict(exclude_fields=exclude_fields)
        
        # Convert enum to string value
        if 'status' in result and isinstance(result['status'], NFTMintStatus):
            result['status'] = result['status'].value
        
        return result
    
    def __repr__(self):
        return f"<NFTMint(id={self.id}, user_id={self.user_id}, status={self.status.value})>"
