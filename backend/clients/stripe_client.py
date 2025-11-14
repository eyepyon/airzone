"""
Stripe payment client for payment processing.
Handles Stripe Payment Intent creation and webhook signature verification.

This client provides the following functionality:
1. Payment Intent Creation: Create payment intents for order processing
2. Webhook Verification: Verify Stripe webhook signatures for security
3. Payment Confirmation: Retrieve payment intent details
4. Refund Processing: Handle payment refunds

Requirements:
- 5.5: Stripe Payment Intent creation and webhook handling

Note: All amounts are in the smallest currency unit (e.g., cents for USD, yen for JPY).
"""
from typing import Dict, Optional
import stripe
import logging


logger = logging.getLogger(__name__)


class StripeClient:
    """
    Client for Stripe payment operations.
    Handles payment intent creation and webhook verification.
    """
    
    def __init__(self, api_key: str, webhook_secret: Optional[str] = None):
        """
        Initialize StripeClient with API credentials.
        
        Args:
            api_key: Stripe secret API key
            webhook_secret: Stripe webhook signing secret for signature verification
            
        Requirements: 5.5
        """
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        
        # Set the Stripe API key
        stripe.api_key = api_key
        
        logger.info("Initialized Stripe client")
    
    def create_payment_intent(
        self,
        amount: int,
        currency: str = 'jpy',
        metadata: Optional[Dict] = None,
        description: Optional[str] = None,
        customer_email: Optional[str] = None
    ) -> Dict:
        """
        Create a Stripe Payment Intent.
        
        Args:
            amount: Payment amount in smallest currency unit (e.g., cents, yen)
            currency: Three-letter ISO currency code (default: 'jpy')
            metadata: Additional metadata to attach to the payment intent
            description: Description of the payment
            customer_email: Customer's email address
            
        Returns:
            Dict: Payment Intent object with client_secret and id
            
        Raises:
            Exception: If payment intent creation fails
            
        Requirements: 5.5 - Stripe Payment Intent creation
        """
        try:
            # Prepare payment intent parameters
            params = {
                'amount': amount,
                'currency': currency.lower(),
                'automatic_payment_methods': {
                    'enabled': True,
                },
            }
            
            # Add optional parameters
            if metadata:
                params['metadata'] = metadata
            
            if description:
                params['description'] = description
            
            if customer_email:
                params['receipt_email'] = customer_email
            
            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(**params)
            
            logger.info(
                f"Created payment intent: {payment_intent.id} "
                f"for amount {amount} {currency}"
            )
            
            return {
                'id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'status': payment_intent.status,
                'metadata': payment_intent.metadata,
            }
            
        except stripe.error.CardError as e:
            # Card was declined
            logger.error(f"Card error: {str(e)}")
            raise Exception(f"Card declined: {e.user_message}")
        
        except stripe.error.RateLimitError as e:
            # Too many requests to Stripe API
            logger.error(f"Rate limit error: {str(e)}")
            raise Exception("Too many requests to payment service. Please try again later.")
        
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters
            logger.error(f"Invalid request error: {str(e)}")
            raise Exception(f"Invalid payment request: {str(e)}")
        
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe failed
            logger.error(f"Authentication error: {str(e)}")
            raise Exception("Payment service authentication failed")
        
        except stripe.error.APIConnectionError as e:
            # Network communication failed
            logger.error(f"API connection error: {str(e)}")
            raise Exception("Failed to connect to payment service")
        
        except stripe.error.StripeError as e:
            # Generic Stripe error
            logger.error(f"Stripe error: {str(e)}")
            raise Exception(f"Payment processing error: {str(e)}")
        
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error creating payment intent: {str(e)}")
            raise Exception(f"Failed to create payment intent: {str(e)}")
    
    def retrieve_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Retrieve a payment intent by ID.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Payment intent details
            
        Raises:
            Exception: If retrieval fails
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            logger.info(f"Retrieved payment intent: {payment_intent_id}")
            
            return {
                'id': payment_intent.id,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
                'status': payment_intent.status,
                'metadata': payment_intent.metadata,
                'charges': payment_intent.charges.data if payment_intent.charges else [],
            }
            
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Invalid payment intent ID: {str(e)}")
            raise Exception(f"Payment intent not found: {payment_intent_id}")
        
        except Exception as e:
            logger.error(f"Error retrieving payment intent: {str(e)}")
            raise Exception(f"Failed to retrieve payment intent: {str(e)}")
    
    def confirm_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Confirm a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Confirmed payment intent details
            
        Raises:
            Exception: If confirmation fails
        """
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            
            logger.info(f"Confirmed payment intent: {payment_intent_id}")
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount,
                'currency': payment_intent.currency,
            }
            
        except Exception as e:
            logger.error(f"Error confirming payment intent: {str(e)}")
            raise Exception(f"Failed to confirm payment: {str(e)}")
    
    def cancel_payment_intent(self, payment_intent_id: str) -> Dict:
        """
        Cancel a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dict: Cancelled payment intent details
            
        Raises:
            Exception: If cancellation fails
        """
        try:
            payment_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            
            logger.info(f"Cancelled payment intent: {payment_intent_id}")
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
            }
            
        except Exception as e:
            logger.error(f"Error cancelling payment intent: {str(e)}")
            raise Exception(f"Failed to cancel payment: {str(e)}")
    
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
            reason: Reason for refund ('duplicate', 'fraudulent', 'requested_by_customer')
            
        Returns:
            Dict: Refund details
            
        Raises:
            Exception: If refund creation fails
        """
        try:
            params = {
                'payment_intent': payment_intent_id,
            }
            
            if amount:
                params['amount'] = amount
            
            if reason:
                params['reason'] = reason
            
            refund = stripe.Refund.create(**params)
            
            logger.info(
                f"Created refund {refund.id} for payment intent {payment_intent_id}"
            )
            
            return {
                'id': refund.id,
                'amount': refund.amount,
                'currency': refund.currency,
                'status': refund.status,
                'reason': refund.reason,
            }
            
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            raise Exception(f"Failed to create refund: {str(e)}")
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        signature_header: str
    ) -> Dict:
        """
        Verify Stripe webhook signature and construct event.
        
        Args:
            payload: Raw request body as bytes
            signature_header: Stripe-Signature header value
            
        Returns:
            Dict: Verified webhook event
            
        Raises:
            Exception: If signature verification fails
            
        Requirements: 5.5 - Webhook signature verification
        """
        if not self.webhook_secret:
            logger.error("Webhook secret not configured")
            raise Exception("Webhook secret not configured")
        
        try:
            # Verify signature and construct event
            event = stripe.Webhook.construct_event(
                payload,
                signature_header,
                self.webhook_secret
            )
            
            logger.info(
                f"Verified webhook signature for event: {event['type']} "
                f"(ID: {event['id']})"
            )
            
            return event
            
        except ValueError as e:
            # Invalid payload
            logger.error(f"Invalid webhook payload: {str(e)}")
            raise Exception("Invalid webhook payload")
        
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            logger.error(f"Webhook signature verification failed: {str(e)}")
            raise Exception("Invalid webhook signature")
        
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error verifying webhook: {str(e)}")
            raise Exception(f"Webhook verification failed: {str(e)}")
    
    def handle_webhook_event(self, event: Dict) -> Dict:
        """
        Process a verified webhook event.
        
        Args:
            event: Verified Stripe webhook event
            
        Returns:
            Dict: Processed event information
        """
        event_type = event['type']
        event_data = event['data']['object']
        
        logger.info(f"Processing webhook event: {event_type}")
        
        # Extract common information
        result = {
            'event_id': event['id'],
            'event_type': event_type,
            'created': event['created'],
        }
        
        # Handle different event types
        if event_type == 'payment_intent.succeeded':
            result['payment_intent_id'] = event_data['id']
            result['amount'] = event_data['amount']
            result['currency'] = event_data['currency']
            result['status'] = 'succeeded'
            logger.info(f"Payment succeeded: {event_data['id']}")
        
        elif event_type == 'payment_intent.payment_failed':
            result['payment_intent_id'] = event_data['id']
            result['amount'] = event_data['amount']
            result['currency'] = event_data['currency']
            result['status'] = 'failed'
            result['error'] = event_data.get('last_payment_error', {}).get('message')
            logger.warning(f"Payment failed: {event_data['id']}")
        
        elif event_type == 'payment_intent.canceled':
            result['payment_intent_id'] = event_data['id']
            result['status'] = 'canceled'
            logger.info(f"Payment canceled: {event_data['id']}")
        
        elif event_type == 'charge.refunded':
            result['charge_id'] = event_data['id']
            result['amount_refunded'] = event_data['amount_refunded']
            result['status'] = 'refunded'
            logger.info(f"Charge refunded: {event_data['id']}")
        
        else:
            logger.info(f"Unhandled event type: {event_type}")
            result['status'] = 'unhandled'
        
        return result
    
    def list_payment_methods(self, customer_id: str) -> list:
        """
        List payment methods for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            list: List of payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type='card'
            )
            
            logger.info(f"Retrieved payment methods for customer: {customer_id}")
            
            return [
                {
                    'id': pm.id,
                    'type': pm.type,
                    'card': {
                        'brand': pm.card.brand,
                        'last4': pm.card.last4,
                        'exp_month': pm.card.exp_month,
                        'exp_year': pm.card.exp_year,
                    } if pm.card else None,
                }
                for pm in payment_methods.data
            ]
            
        except Exception as e:
            logger.error(f"Error listing payment methods: {str(e)}")
            raise Exception(f"Failed to list payment methods: {str(e)}")
