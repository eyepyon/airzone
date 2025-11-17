"""
Referral model for tracking user referrals.
"""
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models.base import Base


class ReferralStatus(enum.Enum):
    """Referral status enumeration."""
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Referral(Base):
    """
    Referral model for tracking user referrals.
    """
    __tablename__ = 'referrals'
    
    id = Column(String(36), primary_key=True)
    referrer_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    referred_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    status = Column(Enum(ReferralStatus), default=ReferralStatus.PENDING)
    coins_awarded = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP, nullable=True)
    
    # Relationships
    referrer = relationship('User', foreign_keys=[referrer_id], backref='referrals_made')
    referred = relationship('User', foreign_keys=[referred_id], backref='referral_received')
    
    def to_dict(self):
        """Convert referral to dictionary."""
        return {
            'id': self.id,
            'referrer_id': self.referrer_id,
            'referred_id': self.referred_id,
            'status': self.status.value,
            'coins_awarded': self.coins_awarded,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class CoinTransaction(Base):
    """
    Coin transaction model for tracking coin movements.
    """
    __tablename__ = 'coin_transactions'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    description = Column(String(500))
    balance_after = Column(Integer, nullable=False)
    related_id = Column(String(36), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='coin_transactions')
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'balance_after': self.balance_after,
            'related_id': self.related_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
