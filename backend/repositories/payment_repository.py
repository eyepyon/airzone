"""
Payment repository for managing payment transaction data access.
Provides custom queries for payment tracking and status updates.

Requirements: 5.5, 5.6
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.payment import Payment, PaymentStatus
from repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository for Payment model with custom query methods.
    Handles payment creation, retrieval, and status management operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize PaymentRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Payment, db_session)
    
    def find_by_order(self, order_id: str) -> List[Payment]:
        """
        Find all payments for a specific order.
        An order may have multiple payment attempts.
        
        Args:
            order_id: Order's ID
            
        Returns:
            List[Payment]: List of payments for the order
            
        Requirements: 5.5 - Payment tracking for orders
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id
        ).order_by(Payment.created_at.desc()).all()
    
    def find_by_stripe_payment_intent_id(self, stripe_payment_intent_id: str) -> Optional[Payment]:
        """
        Find a payment by Stripe Payment Intent ID.
        Used during webhook processing to locate the payment record.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID
            
        Returns:
            Optional[Payment]: Payment instance if found, None otherwise
            
        Requirements: 5.5 - Stripe webhook payment lookup
        """
        return self.db_session.query(Payment).filter(
            Payment.stripe_payment_intent_id == stripe_payment_intent_id
        ).first()
    
    def find_by_status(self, status: PaymentStatus, limit: Optional[int] = None) -> List[Payment]:
        """
        Find all payments with a specific status.
        Used for payment monitoring and reconciliation.
        
        Args:
            status: Payment status to filter by
            limit: Maximum number of payments to return
            
        Returns:
            List[Payment]: List of payments with the specified status
            
        Requirements: 5.6 - Payment status tracking
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
        Used during payment processing and webhook handling.
        
        Args:
            payment_id: Payment's ID
            status: New payment status
            
        Returns:
            Optional[Payment]: Updated payment instance if found, None otherwise
            
        Requirements: 5.6 - Payment status updates during processing
        """
        return self.update(payment_id, status=status)
    
    def update_status_by_stripe_intent(self, stripe_payment_intent_id: str, 
                                       status: PaymentStatus) -> Optional[Payment]:
        """
        Update payment status by Stripe Payment Intent ID.
        Convenience method for webhook processing.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID
            status: New payment status
            
        Returns:
            Optional[Payment]: Updated payment instance if found, None otherwise
            
        Requirements: 5.6 - Webhook-triggered payment status updates
        """
        payment = self.find_by_stripe_payment_intent_id(stripe_payment_intent_id)
        if payment:
            return self.update(payment.id, status=status)
        return None
    
    def create_payment(self, order_id: str, stripe_payment_intent_id: str, 
                      amount: int, currency: str = 'jpy') -> Payment:
        """
        Create a new payment record.
        
        Args:
            order_id: Order's ID
            stripe_payment_intent_id: Stripe Payment Intent ID
            amount: Payment amount in smallest currency unit
            currency: Currency code (default: 'jpy')
            
        Returns:
            Payment: Created payment instance
            
        Requirements: 5.5 - Payment record creation
        """
        return self.create(
            order_id=order_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.PENDING
        )
    
    def count_by_status(self, status: PaymentStatus) -> int:
        """
        Count payments with a specific status.
        
        Args:
            status: Payment status to count
            
        Returns:
            int: Number of payments with the status
        """
        return self.db_session.query(Payment).filter(
            Payment.status == status
        ).count()
    
    def get_successful_payments_by_order(self, order_id: str) -> List[Payment]:
        """
        Get all successful payments for an order.
        
        Args:
            order_id: Order's ID
            
        Returns:
            List[Payment]: List of successful payments
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id,
            Payment.status == PaymentStatus.SUCCEEDED
        ).all()
    
    def stripe_intent_exists(self, stripe_payment_intent_id: str) -> bool:
        """
        Check if a Stripe Payment Intent ID already exists.
        Prevents duplicate payment records.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(Payment).filter(
                Payment.stripe_payment_intent_id == stripe_payment_intent_id
            ).exists()
        ).scalar()
