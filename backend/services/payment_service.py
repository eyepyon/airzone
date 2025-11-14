"""
Payment Service for managing payment processing.
Handles Stripe Payment Intent creation, webhook processing, and payment status updates.

Requirements: 5.5, 5.6, 5.7
"""
from typing import Dict, Optional
import logging
from sqlalchemy.orm import Session
from repositories.payment_repository import PaymentRepository
from repositories.order_repository import OrderRepository
from clients.stripe_client import StripeClient
from models.payment import PaymentStatus
from models.order import OrderStatus


logger = logging.getLogger(__name__)


class PaymentService:
    """
    Service for payment operations.
    Handles payment intent creation, webhook processing, and order completion.
    """
    
    def __init__(
        self,
        db_session: Session,
        stripe_client: StripeClient
    ):
        """
        Initialize PaymentService.
        
        Args:
            db_session: SQLAlchemy database session
            stripe_client: Stripe payment client
        """
        self.db_session = db_session
        self.payment_repo = PaymentRepository(db_session)
        self.order_repo = OrderRepository(db_session)
        self.stripe_client = stripe_client
    
    def create_payment_intent(
        self,
        order_id: str,
        customer_email: Optional[str] = None
    ) -> Dict:
        """
        Create a Stripe Payment Intent for an order.
        
        Args:
            order_id: Order ID
            customer_email: Customer's email address
            
        Returns:
            Dict: Payment intent information with client_secret
            
        Raises:
            ValueError: If order not found or invalid
            
        Requirements: 5.5 - Stripe Payment Intent creation
        """
        try:
            # Get order
            order = self.order_repo.find_by_id(order_id)
            if not order:
                raise ValueError(f"Order not found: {order_id}")
            
            # Verify order is in pending status
            if order.status != OrderStatus.PENDING:
                raise ValueError(
                    f"Cannot create payment for order with status: {order.status.value}"
                )
            
            # Check if payment already exists for this order
            existing_payments = self.payment_repo.find_by_order(order_id)
            for payment in existing_payments:
                if payment.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]:
                    logger.warning(
                        f"Payment already exists for order {order_id}: {payment.id}"
                    )
                    return {
                        'payment_id': payment.id,
                        'client_secret': None,
                        'status': payment.status.value,
                        'message': 'Payment already in progress'
                    }
            
            # Create Stripe Payment Intent
            metadata = {
                'order_id': order_id,
                'user_id': order.user_id
            }
            
            payment_intent = self.stripe_client.create_payment_intent(
                amount=order.total_amount,
                currency='jpy',
                metadata=metadata,
                description=f"Order {order_id}",
                customer_email=customer_email
            )
            
            # Create payment record
            payment = self.payment_repo.create_payment(
                order_id=order_id,
                stripe_payment_intent_id=payment_intent['id'],
                amount=order.total_amount,
                currency='jpy'
            )
            
            # Update order status to processing
            self.order_repo.update_status(order_id, OrderStatus.PROCESSING)
            
            self.db_session.commit()
            logger.info(
                f"Created payment intent for order {order_id}: {payment.id}"
            )
            
            return {
                'payment_id': payment.id,
                'client_secret': payment_intent['client_secret'],
                'amount': payment.amount,
                'currency': payment.currency,
                'status': payment.status.value
            }
            
        except ValueError as e:
            logger.error(f"Payment intent creation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating payment intent: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Failed to create payment intent: {str(e)}")
    
    def handle_webhook(self, payload: bytes, signature_header: str) -> Dict:
        """
        Handle Stripe webhook event.
        Verifies signature and processes the event.
        
        Args:
            payload: Raw webhook payload
            signature_header: Stripe-Signature header
            
        Returns:
            Dict: Processing result
            
        Raises:
            Exception: If webhook verification fails
            
        Requirements: 5.5 - Webhook event processing
        """
        try:
            # Verify webhook signature
            event = self.stripe_client.verify_webhook_signature(
                payload,
                signature_header
            )
            
            # Process event
            result = self.stripe_client.handle_webhook_event(event)
            
            # Handle specific event types
            event_type = result['event_type']
            
            if event_type == 'payment_intent.succeeded':
                self._handle_payment_success(result)
            elif event_type == 'payment_intent.payment_failed':
                self._handle_payment_failure(result)
            elif event_type == 'payment_intent.canceled':
                self._handle_payment_cancellation(result)
            
            logger.info(f"Processed webhook event: {event_type}")
            
            return result
            
        except Exception as e:
            logger.error(f"Webhook handling failed: {str(e)}")
            raise
    
    def _handle_payment_success(self, event_data: Dict) -> None:
        """
        Handle successful payment event.
        Updates payment and order status.
        
        Args:
            event_data: Payment event data
            
        Requirements: 5.6 - Payment success handling and order completion
        """
        try:
            payment_intent_id = event_data['payment_intent_id']
            
            # Find payment by Stripe Payment Intent ID
            payment = self.payment_repo.find_by_stripe_payment_intent_id(
                payment_intent_id
            )
            
            if not payment:
                logger.warning(
                    f"Payment not found for intent: {payment_intent_id}"
                )
                return
            
            # Update payment status
            self.payment_repo.update_status(payment.id, PaymentStatus.SUCCEEDED)
            
            # Update order status to completed
            self.order_repo.update_status(payment.order_id, OrderStatus.COMPLETED)
            
            self.db_session.commit()
            logger.info(
                f"Payment succeeded for order {payment.order_id}: {payment.id}"
            )
            
        except Exception as e:
            logger.error(f"Failed to handle payment success: {str(e)}")
            self.db_session.rollback()
            raise
    
    def _handle_payment_failure(self, event_data: Dict) -> None:
        """
        Handle failed payment event.
        Updates payment and order status, restores stock.
        
        Args:
            event_data: Payment event data
            
        Requirements: 5.7 - Payment failure handling with stock restoration
        """
        try:
            payment_intent_id = event_data['payment_intent_id']
            
            # Find payment by Stripe Payment Intent ID
            payment = self.payment_repo.find_by_stripe_payment_intent_id(
                payment_intent_id
            )
            
            if not payment:
                logger.warning(
                    f"Payment not found for intent: {payment_intent_id}"
                )
                return
            
            # Update payment status
            self.payment_repo.update_status(payment.id, PaymentStatus.FAILED)
            
            # Update order status to failed and restore stock
            order = self.order_repo.find_by_id(payment.order_id)
            if order:
                # Restore stock for all items
                from repositories.product_repository import ProductRepository
                product_repo = ProductRepository(self.db_session)
                
                for item in order.order_items:
                    product_repo.update_stock(item.product_id, item.quantity)
                    logger.info(
                        f"Restored {item.quantity} units of product {item.product_id}"
                    )
                
                # Update order status
                self.order_repo.update_status(payment.order_id, OrderStatus.FAILED)
            
            self.db_session.commit()
            logger.info(
                f"Payment failed for order {payment.order_id}: {payment.id}"
            )
            
        except Exception as e:
            logger.error(f"Failed to handle payment failure: {str(e)}")
            self.db_session.rollback()
            raise
    
    def _handle_payment_cancellation(self, event_data: Dict) -> None:
        """
        Handle cancelled payment event.
        Updates payment and order status, restores stock.
        
        Args:
            event_data: Payment event data
            
        Requirements: 5.7 - Payment cancellation handling with stock restoration
        """
        try:
            payment_intent_id = event_data['payment_intent_id']
            
            # Find payment by Stripe Payment Intent ID
            payment = self.payment_repo.find_by_stripe_payment_intent_id(
                payment_intent_id
            )
            
            if not payment:
                logger.warning(
                    f"Payment not found for intent: {payment_intent_id}"
                )
                return
            
            # Update payment status
            self.payment_repo.update_status(payment.id, PaymentStatus.CANCELLED)
            
            # Update order status to cancelled and restore stock
            order = self.order_repo.find_by_id(payment.order_id)
            if order:
                # Restore stock for all items
                from repositories.product_repository import ProductRepository
                product_repo = ProductRepository(self.db_session)
                
                for item in order.order_items:
                    product_repo.update_stock(item.product_id, item.quantity)
                    logger.info(
                        f"Restored {item.quantity} units of product {item.product_id}"
                    )
                
                # Update order status
                self.order_repo.update_status(payment.order_id, OrderStatus.CANCELLED)
            
            self.db_session.commit()
            logger.info(
                f"Payment cancelled for order {payment.order_id}: {payment.id}"
            )
            
        except Exception as e:
            logger.error(f"Failed to handle payment cancellation: {str(e)}")
            self.db_session.rollback()
            raise
    
    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Get payment by ID.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Optional[Dict]: Payment information or None if not found
        """
        payment = self.payment_repo.find_by_id(payment_id)
        if not payment:
            return None
        
        return payment.to_dict()
    
    def get_order_payments(self, order_id: str) -> list:
        """
        Get all payments for an order.
        
        Args:
            order_id: Order ID
            
        Returns:
            list: List of payment records
        """
        payments = self.payment_repo.find_by_order(order_id)
        return [payment.to_dict() for payment in payments]
    
    def get_payment_by_stripe_intent(
        self,
        stripe_payment_intent_id: str
    ) -> Optional[Dict]:
        """
        Get payment by Stripe Payment Intent ID.
        
        Args:
            stripe_payment_intent_id: Stripe Payment Intent ID
            
        Returns:
            Optional[Dict]: Payment information or None if not found
        """
        payment = self.payment_repo.find_by_stripe_payment_intent_id(
            stripe_payment_intent_id
        )
        if not payment:
            return None
        
        return payment.to_dict()
    
    def cancel_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Cancel a payment and restore stock.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Optional[Dict]: Updated payment or None if not found
            
        Raises:
            ValueError: If payment cannot be cancelled
        """
        try:
            payment = self.payment_repo.find_by_id(payment_id)
            if not payment:
                return None
            
            # Only allow cancellation of pending or processing payments
            if payment.status not in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]:
                raise ValueError(
                    f"Cannot cancel payment with status: {payment.status.value}"
                )
            
            # Cancel Stripe Payment Intent
            self.stripe_client.cancel_payment_intent(
                payment.stripe_payment_intent_id
            )
            
            # Update payment status
            self.payment_repo.update_status(payment.id, PaymentStatus.CANCELLED)
            
            # Update order and restore stock
            order = self.order_repo.find_by_id(payment.order_id)
            if order:
                from repositories.product_repository import ProductRepository
                product_repo = ProductRepository(self.db_session)
                
                for item in order.order_items:
                    product_repo.update_stock(item.product_id, item.quantity)
                
                self.order_repo.update_status(payment.order_id, OrderStatus.CANCELLED)
            
            self.db_session.commit()
            logger.info(f"Cancelled payment: {payment_id}")
            
            return payment.to_dict()
            
        except ValueError as e:
            logger.error(f"Payment cancellation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to cancel payment: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Payment cancellation failed: {str(e)}")
