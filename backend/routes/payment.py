"""
Payment Blueprint for managing payment processing.
Provides endpoints for Stripe Payment Intent creation, webhook handling, and payment retrieval.

Requirements: 5.5, 5.6, 8.2, 8.6, 8.7
"""
import logging
from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.security import validate_json_request, InputValidator
from services.payment_service import PaymentService
from clients.stripe_client import StripeClient
from exceptions import (
    ValidationError,
    ResourceNotFoundError,
    AuthorizationError
)

logger = logging.getLogger(__name__)

# Create blueprint
payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/intent', methods=['POST'])
@jwt_required()
@validate_json_request(required_fields=['order_id'])
def create_payment_intent():
    """
    Create a Stripe Payment Intent for an order.
    
    POST /api/v1/payments/intent
    
    Request Body:
        {
            "order_id": "uuid",
            "customer_email": "user@example.com"  // optional
        }
    
    Returns:
        201: Payment intent created successfully
        400: Validation error or invalid order
        401: Unauthorized
        403: Order does not belong to user
        404: Order not found
        
    Requirements: 5.5, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get sanitized request data
        data = request.sanitized_data
        order_id = data.get('order_id')
        customer_email = data.get('customer_email')
        
        # Validate order ID format
        try:
            order_id = InputValidator.validate_uuid(order_id)
        except ValidationError:
            raise ValidationError("Invalid order ID format", field='order_id')
        
        # Validate customer email if provided
        if customer_email:
            try:
                customer_email = InputValidator.validate_email(customer_email)
            except ValidationError:
                raise ValidationError("Invalid email format", field='customer_email')
        
        # Verify order belongs to user
        from repositories.order_repository import OrderRepository
        order_repo = OrderRepository(g.db)
        order = order_repo.find_by_id(order_id)
        
        if not order:
            raise ResourceNotFoundError("Order", order_id)
        
        if order.user_id != user_id:
            logger.warning(
                f"User attempted to create payment for another user's order",
                extra={
                    'user_id': user_id,
                    'order_id': order_id,
                    'order_user_id': order.user_id
                }
            )
            raise AuthorizationError("You do not have permission to create payment for this order")
        
        # Create payment intent using service
        stripe_client = StripeClient(
            api_key=current_app.config['STRIPE_SECRET_KEY'],
            webhook_secret=current_app.config['STRIPE_WEBHOOK_SECRET']
        )
        payment_service = PaymentService(g.db, stripe_client)
        
        payment_intent = payment_service.create_payment_intent(
            order_id=order_id,
            customer_email=customer_email
        )
        
        logger.info(
            f"Payment intent created successfully",
            extra={
                'user_id': user_id,
                'order_id': order_id,
                'payment_id': payment_intent['payment_id']
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': payment_intent
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Payment intent creation validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Order not found: {order_id}")
        return jsonify(e.to_dict()), e.code
    except AuthorizationError as e:
        return jsonify(e.to_dict()), e.code
    except ValueError as e:
        # Handle business logic errors from service
        logger.warning(f"Payment intent creation failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(
            f"Unexpected error creating payment intent: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to create payment intent',
            'code': 500
        }), 500


@payment_blueprint.route('/webhook', methods=['POST'])
def handle_stripe_webhook():
    """
    Handle Stripe webhook events.
    
    POST /api/v1/payments/webhook
    
    Headers:
        Stripe-Signature: Webhook signature for verification
    
    Returns:
        200: Webhook processed successfully
        400: Invalid payload or signature
        
    Requirements: 5.5, 5.6, 8.2, 8.6, 8.7
    
    Note: This endpoint does not require JWT authentication as it's called by Stripe.
    """
    try:
        # Get raw payload and signature
        payload = request.get_data()
        signature_header = request.headers.get('Stripe-Signature')
        
        if not signature_header:
            logger.warning("Missing Stripe-Signature header")
            return jsonify({
                'status': 'error',
                'error': 'Missing signature header',
                'code': 400
            }), 400
        
        # Process webhook using service
        stripe_client = StripeClient(
            api_key=current_app.config['STRIPE_SECRET_KEY'],
            webhook_secret=current_app.config['STRIPE_WEBHOOK_SECRET']
        )
        payment_service = PaymentService(g.db, stripe_client)
        
        result = payment_service.handle_webhook(payload, signature_header)
        
        logger.info(
            f"Webhook processed successfully",
            extra={
                'event_type': result['event_type'],
                'event_id': result['event_id']
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(
            f"Webhook processing failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400


@payment_blueprint.route('/<payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id: str):
    """
    Get payment details by ID.
    
    GET /api/v1/payments/{payment_id}
    
    Path Parameters:
        payment_id: Payment UUID
    
    Returns:
        200: Payment details
        400: Invalid payment ID format
        401: Unauthorized
        403: Payment does not belong to user's order
        404: Payment not found
        
    Requirements: 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Validate payment ID format
        try:
            payment_id = InputValidator.validate_uuid(payment_id)
        except ValidationError:
            raise ValidationError("Invalid payment ID format", field='payment_id')
        
        # Get payment using service
        stripe_client = StripeClient(
            api_key=current_app.config['STRIPE_SECRET_KEY'],
            webhook_secret=current_app.config['STRIPE_WEBHOOK_SECRET']
        )
        payment_service = PaymentService(g.db, stripe_client)
        
        payment = payment_service.get_payment(payment_id)
        
        if not payment:
            raise ResourceNotFoundError("Payment", payment_id)
        
        # Verify payment belongs to user's order
        from repositories.order_repository import OrderRepository
        order_repo = OrderRepository(g.db)
        order = order_repo.find_by_id(payment['order_id'])
        
        if not order or order.user_id != user_id:
            logger.warning(
                f"User attempted to access another user's payment",
                extra={
                    'user_id': user_id,
                    'payment_id': payment_id,
                    'order_id': payment['order_id']
                }
            )
            raise AuthorizationError("You do not have permission to access this payment")
        
        logger.info(
            f"Retrieved payment details",
            extra={
                'user_id': user_id,
                'payment_id': payment_id
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': payment
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Get payment validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Payment not found: {payment_id}")
        return jsonify(e.to_dict()), e.code
    except AuthorizationError as e:
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving payment: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve payment',
            'code': 500
        }), 500
