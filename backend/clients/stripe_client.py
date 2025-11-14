"""
Stripe payment client for handling payment processing.
Manages payment intents and webhook verification.

Requirements: 5.5
"""
from typing import Dict, Optional
import stripe
import logging


logger = logging.getLogger(__name__)


class StripeClient:
    """
    Client for Stripe payment processing.
    Handles payment intent creation and webhook signature verification.
    """
    
    def __init__(self, secret_key: str, webhook_secret: Optional[str] = None):
        """
        Initialize StripeClient with API credentials.
        
        Args:
            secret_key: Stripe secret API key
            webhook_secret: Stripe webhook signing secret
        """
        self.secret_key = secret_key
        self.webhook_secret = webhook_secret
        stripe.api_key = secret_key
        
        logger.info("Initialized StripeClient")
    
    def create_payment_intent(
        self,
        amount: int,
        currency: str = 'jpy',
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Stripe Payment Intent.
        
        Args:
            amount: Payment amount in smallest currency unit (e.g., cents for USD, yen for JPY)
            currency: Three-letter ISO currency code (default: 'jpy')
            metadata: Optional metadata to attach to the payment intent
            
        Returns:
            Dict: Payment intent details including client_secret
            
        Requirements: 5.5 - Create Stripe Payment Intent
        """
        try:
            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                }
            )
            
            result = {
                'id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'status': payment_intent.status,
                'metadata': payment_intent.metadata
            }
            
            logger.info(
                f"Created payment intent: {payment_intent.id} "
                f"for amount {amount} {currency}"
            )
            
            return result
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            raise Exception(f"Failed to create payment intent: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error creating payment intent: {str(e)}")
            raise Exception(f"Payment intent creation failed: {str(e)}")
    
    def retrieve_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Retrieve a payment intent by ID.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Payment intent details
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'id': payment_intent.id,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'status': payment_intent.status,
                'metadata': payment_intent.metadata,
                'charges': payment_intent.charges
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error retrieving payment intent: {str(e)}")
            raise Exception(f"Failed to retrieve payment intent: {str(e)}")
    
    def confirm_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Confirm a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Confirmed payment intent details
        """
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            
            logger.info(f"Confirmed payment intent: {payment_intent_id}")
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error confirming payment intent: {str(e)}")
            raise Exception(f"Failed to confirm payment intent: {str(e)}")
    
    def cancel_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Cancel a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Cancelled payment intent details
        """
        try:
            payment_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            
            logger.info(f"Cancelled payment intent: {payment_intent_id}")
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error cancelling payment intent: {str(e)}")
            raise Exception(f"Failed to cancel payment intent: {str(e)}")
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> Dict:
        """
        Verify Stripe webhook signature and parse event.
        
        Args:
            payload: Raw request body from Stripe webhook
            signature: Stripe-Signature header value
            
        Returns:
            Dict: Parsed webhook event
            
        Raises:
            ValueError: If signature verification fails
            
        Requirements: 5.5 - Verify webhook signatures
        """
        if not self.webhook_secret:
            raise ValueError("Webhook secret not configured")
        
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.webhook_secret
            )
            
            logger.info(f"Verified webhook event: {event['type']}")
            
            return {
                'id': event['id'],
                'type': event['type'],
                'data': event['data'],
                'created': event['created']
            }
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {str(e)}")
            raise ValueError(f"Invalid webhook signature: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            raise Exception(f"Webhook processing failed: {str(e)}")
    
    def handle_webhook_event(self, event: Dict) -> Dict:
        """
        Process a verified webhook event.
        
        Args:
            event: Verified webhook event from Stripe
            
        Returns:
            Dict: Processing result
        """
        event_type = event.get('type')
        event_data = event.get('data', {}).get('object', {})
        
        logger.info(f"Processing webhook event: {event_type}")
        
        # Return event details for service layer to handle
        return {
            'type': event_type,
            'payment_intent_id': event_data.get('id'),
            'status': event_data.get('status'),
            'amount': event_data.get('amount'),
            'metadata': event_data.get('metadata', {})
        }
    
    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> Dict:
        """
        Create a refund for a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund (if None, refunds full amount)
            reason: Reason for refund
            
        Returns:
            Dict: Refund details
        """
        try:
            refund_params = {
                'payment_intent': payment_intent_id
            }
            
            if amount is not None:
                refund_params['amount'] = amount
            
            if reason:
                refund_params['reason'] = reason
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Created refund for payment intent: {payment_intent_id}")
            
            return {
                'id': refund.id,
                'amount': refund.amount,
                'status': refund.status,
                'payment_intent': refund.payment_intent
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating refund: {str(e)}")
            raise Exception(f"Failed to create refund: {str(e)}")
