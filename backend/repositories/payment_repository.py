"""
PaymentRepository for managing payment transaction data access.
Provides methods for payment CRUD operations and status management.

Requirements: 5.5, 5.6
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from models.payment import Payment, PaymentStatus


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository for Payment model.
    Handles payment creation, retrieval, and status updates.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize PaymentRepository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Payment, db_session)
    
    def find_by_order(self, order_id: str) -> List[Payment]:
        """
        Find all payments for a specific order.
        
        Args:
            order_id: The order ID to filter by
            
        Returns:
            List[Payment]: List of payments for the order
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id
        ).order_by(Payment.created_at.desc()).all()
    
    def find_by_stripe_payment_intent_id(self, stripe_payment_intent_id: str) -> Optional[Payment]:
        """
        Find a payment by Stripe Payment Intent ID.
        
        Args:
            stripe_payment_intent_id: The Stripe Payment Intent ID
            
        Returns:
            Optional[Payment]: Payment if found, None otherwise
        """
        return self.db_session.query(Payment).filter(
            Payment.stripe_payment_intent_id == stripe_payment_intent_id
        ).first()
    
    def find_by_status(self, status: PaymentStatus, limit: Optional[int] = None) -> List[Payment]:
        """
        Find payments by status.
        
        Args:
            status: The payment status to filter by
            limit: Maximum number of records to return
            
        Returns:
            List[Payment]: List of payments with the specified status
        """
        query = self.db_session.query(Payment).filter(
            Payment.status == status
        ).order_by(Payment.created_at.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def update_status(self, payment_id: str, status: PaymentStatus) -> Optional[Payment]:
        """
        Update the status of a payment.
        
        Args:
            payment_id: The payment ID to update
            status: The new status
            
        Returns:
            Optional[Payment]: Updated payment if found, None otherwise
        """
        return self.update(payment_id, status=status)
    
    def update_status_by_stripe_intent(self, stripe_payment_intent_id: str, 
                                       status: PaymentStatus) -> Optional[Payment]:
        """
        Update payment status by Stripe Payment Intent ID.
        
        Args:
            stripe_payment_intent_id: The Stripe Payment Intent ID
            status: The new status
            
        Returns:
            Optional[Payment]: Updated payment if found, None otherwise
        """
        payment = self.find_by_stripe_payment_intent_id(stripe_payment_intent_id)
        if payment:
            return self.update_status(payment.id, status)
        return None
    
    def create_payment(self, order_id: str, stripe_payment_intent_id: str, 
                      amount: int, currency: str = 'jpy') -> Payment:
        """
        Create a new payment record.
        
        Args:
            order_id: The order ID
            stripe_payment_intent_id: The Stripe Payment Intent ID
            amount: Payment amount in smallest currency unit
            currency: Currency code (default: 'jpy')
            
        Returns:
            Payment: Created payment record
        """
        return self.create(
            order_id=order_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.PENDING
        )
