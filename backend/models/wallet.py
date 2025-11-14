"""
Wallet model for storing Sui blockchain wallet information.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Wallet(BaseModel):
    """
    Wallet model representing a Sui blockchain wallet.
    Each user has one wallet that stores their private key (encrypted) and address.
    """
    __tablename__ = 'wallets'
    
    # Wallet fields
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    address = Column(String(255), unique=True, nullable=False)
    private_key_encrypted = Column(Text, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='wallets')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_address', 'address'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert wallet to dictionary, excluding private key by default.
        
        Args:
            exclude_fields (list): Additional fields to exclude
            
        Returns:
            dict: Wallet data dictionary
        """
        if exclude_fields is None:
            exclude_fields = []
        
        # Always exclude encrypted private key from public representation
        exclude_fields.append('private_key_encrypted')
        
        return super().to_dict(exclude_fields=exclude_fields)
    
    def __repr__(self):
        return f"<Wallet(id={self.id}, user_id={self.user_id}, address={self.address})>"
