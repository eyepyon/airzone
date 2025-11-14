"""
Payment repository for managing payment transaction data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from models.payment import Payment, PaymentStatus
from repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository for Payment model operations.
    Provides custom queries for payment filtering and status management.
    
    Requirements: 5.5, 5.6
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
        
        Args:
            order_id: Order ID
            
        Returns:
            List[Payment]: List of payment instances
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id
        ).order_by(Payment.created_at.desc()).all()
    
    def find_by_stripe_payment_intent_id(self, stripe_payment_intent_id: str) -> Optional[Payment]:
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
    
    def find_with_order(self, payment_id: str) -> Optional[Payment]:
        """
        Find a payment by ID with its order eagerly loaded.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Optional[Payment]: Payment instance with order if found, None otherwise
        """
        return self.db_session.query(Payment).options(
            joinedload(Payment.order)
        ).filter(Payment.id == payment_id).first()
    
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
    
    def update_status_by_stripe_intent(
        self, 
        stripe_payment_intent_id: str, 
        status: PaymentStatus
    ) -> Optional[Payment]:
        """
        Update payment status by Stripe Payment Intent ID.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID
            status: New payment status
            
        Returns:
            Optional[Payment]: Updated payment instance if found, None otherwise
        """
        payment = self.find_by_stripe_payment_intent_id(stripe_payment_intent_id)
        if not payment:
            return None
        
        return self.update(payment.id, status=status)
    
    def get_total_amount_by_status(self, status: PaymentStatus) -> int:
        """
        Calculate total amount of payments with a specific status.
        
        Args:
            status: Payment status to filter by
            
        Returns:
            int: Total amount in smallest currency unit
        """
        payments = self.find_by_status(status)
        return sum(payment.amount for payment in payments)
    
    def count_by_status(self, status: PaymentStatus) -> int:
        """
        Count payments with a specific status.
        
        Args:
            status: Payment status to filter by
            
        Returns:
            int: Number of payments
        """
        return self.db_session.query(Payment).filter(
            Payment.status == status
        ).count()
    
    def find_successful_payments_by_order(self, order_id: str) -> List[Payment]:
        """
        Find all successful payments for a specific order.
        
        Args:
            order_id: Order ID
            
        Returns:
            List[Payment]: List of successful payment instances
        """
        return self.db_session.query(Payment).filter(
            Payment.order_id == order_id,
            Payment.status == PaymentStatus.SUCCEEDED
        ).order_by(Payment.created_at.desc()).all()
    
    def has_successful_payment(self, order_id: str) -> bool:
        """
        Check if an order has at least one successful payment.
        
        Args:
            order_id: Order ID
            
        Returns:
            bool: True if order has successful payment, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(Payment).filter(
                Payment.order_id == order_id,
                Payment.status == PaymentStatus.SUCCEEDED
            ).exists()
        ).scalar()
    
    def stripe_payment_intent_exists(self, stripe_payment_intent_id: str) -> bool:
        """
        Check if a Stripe Payment Intent ID already exists.
        
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
