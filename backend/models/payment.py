"""
Payment model for tracking Stripe payment transactions.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum


class PaymentStatus(enum.Enum):
    """Enum for payment status"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class Payment(BaseModel):
    """
    Payment model representing a Stripe payment transaction.
    Links orders to Stripe payment intents and tracks payment status.
    """
    __tablename__ = 'payments'
    
    # Payment fields
    order_id = Column(String(36), ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=False)
    amount = Column(Integer, nullable=False)  # Amount in smallest currency unit
    currency = Column(String(3), default='jpy', nullable=False)
    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False
    )
    
    # Relationships
    order = relationship('Order', back_populates='payments')
    
    # Indexes
    __table_args__ = (
        Index('idx_order_id', 'order_id'),
        Index('idx_stripe_payment_intent_id', 'stripe_payment_intent_id'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert payment to dictionary.
        
        Args:
            exclude_fields (list): Fields to exclude
            
        Returns:
            dict: Payment data dictionary
        """
        result = super().to_dict(exclude_fields=exclude_fields)
        
        # Convert enum to string value
        if 'status' in result and isinstance(result['status'], PaymentStatus):
            result['status'] = result['status'].value
        
        return result
    
    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, amount={self.amount}, status={self.status.value})>"
