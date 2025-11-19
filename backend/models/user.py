"""
User model for storing user account information.
"""
from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel


class User(BaseModel):
    """
    User model representing a user account.
    Users authenticate via Google OAuth and have associated wallets and NFTs.
    """
    __tablename__ = 'users'
    
    # User fields
    email = Column(String(255), unique=True, nullable=False)
    google_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    
    # Referral fields
    referral_code = Column(String(20), unique=True, nullable=True)
    referred_by = Column(String(36), nullable=True)
    coins = Column(Integer, default=0)
    
    # Relationships
    wallets = relationship('Wallet', back_populates='user', cascade='all, delete-orphan')
    nft_mints = relationship('NFTMint', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    wifi_sessions = relationship('WiFiSession', back_populates='user')
    
    # Indexes
    __table_args__ = (
        Index('idx_google_id', 'google_id'),
        Index('idx_email', 'email'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert user to dictionary, excluding sensitive information by default.
        
        Args:
            exclude_fields (list): Additional fields to exclude
            
        Returns:
            dict: User data dictionary
        """
        if exclude_fields is None:
            exclude_fields = []
        
        # Always exclude google_id from public representation
        exclude_fields.append('google_id')
        
        return super().to_dict(exclude_fields=exclude_fields)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
