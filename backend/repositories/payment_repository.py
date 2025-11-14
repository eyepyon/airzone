"""
Payment repository for managing payment data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.payment import Payment, PaymentStatus
from repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository for Payment model operations.
    Provides custom queries for payment lookup and status management.
    
    Requirements: 5.3, 5.4, 5.5, 5.6
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize PaymentRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Payment, db_session)
    
    def find_by_order_id(self, order_id: str) -> List[Payment]:
        """
        Find all payments for a specific order.
        
        Args:
            order_id: Order ID
            
        Returns:
            List[Payment]: List of payment instances
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id
        ).order_by(Payment.created_at.desc()).all()
    
    def find_by_stripe_payment_intent_id(self, 
                                         stripe_payment_intent_id: str) -> Optional[Payment]:
        """
        Find a payment by Stripe Payment Intent ID.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID
            
        Returns:
            Optional[Payment]: Payment instance if found, None otherwise
        """
        return self.db_session.query(Payment).filter(
            Payment.stripe_payment_intent_id == stripe_payment_intent_id
        ).first()
    
    def find_by_status(self, status: PaymentStatus) -> List[Payment]:
        """
        Find all payments with a specific status.
        
        Args:
            status: Payment status to filter by
            
        Returns:
            List[Payment]: List of payment instances
        """
        return self.db_session.query(Payment).filter(
            Payment.status == status
        ).order_by(Payment.created_at.desc()).all()
    
    def update_status(self, payment_id: str, status: PaymentStatus) -> Optional[Payment]:
        """
        Update the status of a payment.
        
        Args:
            payment_id: Payment ID
            status: New payment status
            
        Returns:
            Optional[Payment]: Updated payment instance if found, None otherwise
        """
        return self.update(payment_id, status=status)
    
    def find_successful_payments(self) -> List[Payment]:
        """
        Find all successful payments.
        
        Returns:
            List[Payment]: List of successful payment instances
        """
        return self.find_by_status(PaymentStatus.SUCCEEDED)
    
    def find_pending_payments(self) -> List[Payment]:
        """
        Find all pending payments.
        
        Returns:
            List[Payment]: List of pending payment instances
        """
        return self.find_by_status(PaymentStatus.PENDING)
    
    def find_failed_payments(self) -> List[Payment]:
        """
        Find all failed payments.
        
        Returns:
            List[Payment]: List of failed payment instances
        """
        return self.find_by_status(PaymentStatus.FAILED)
    
    def count_by_status(self, status: PaymentStatus) -> int:
        """
        Count payments with a specific status.
        
        Args:
            status: Payment status to count
            
        Returns:
            int: Number of payments with the given status
        """
        return self.db_session.query(Payment).filter(
            Payment.status == status
        ).count()
    
    def get_total_amount_by_status(self, status: PaymentStatus) -> int:
        """
        Calculate total amount of payments with a specific status.
        
        Args:
            status: Payment status to sum
            
        Returns:
            int: Total amount of payments with the given status
        """
        from sqlalchemy import func
        
        result = self.db_session.query(
            func.sum(Payment.amount)
        ).filter(
            Payment.status == status
        ).scalar()
        
        return result or 0
