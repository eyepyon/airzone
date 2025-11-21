"""
XRPL Payment Blueprint for managing XRP Ledger payments.
Provides endpoints for XRPL payment creation, verification, and status checking.

Requirements: 5.5, 8.2, 8.6, 8.7
"""
import logging
from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.security import validate_json_request, InputValidator
from services.xrpl_payment_service import XRPLPaymentService
from clients.xrpl_client import XRPLClient
from exceptions import (
    ValidationError,
    ResourceNotFoundError,
    AuthorizationError
)

logger = logging.getLogger(__name__)

# Create blueprint
xrpl_payment_blueprint = Blueprint('xrpl_payment', __name__)


@xrpl_payment_blueprint.route('/create', methods=['POST'])
@jwt_required()
@validate_json_request(required_fields=['order_id', 'amount_xrp'])
def create_xrpl_payment():
    """
    Create an XRPL payment request for an order.
    
    POST /api/v1/payments/xrpl/create
    
    Request Body:
        {
            "order_id": "uuid",
            "amount_xrp": 10.5,
            "destination": "rN7n7otQDd6FczFgLdSqtcsAUxDkw6fzRH"  // optional, defaults to sponsor
        }
    
    Returns:
        201: Payment request created successfully
        400: Validation error or invalid order
        401: Unauthorized
        403: Order does not belong to user
        404: Order not found
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get sanitized request data
        data = request.sanitized_data
        order_id = data.get('order_id')
        amount_xrp = float(data.get('amount_xrp'))
        destination = data.get('destination', current_app.config['XRPL_SPONSOR_ADDRESS'])
        
        # Validate order ID format
        try:
            order_id = InputValidator.validate_uuid(order_id)
        except ValidationError:
            raise ValidationError("Invalid order ID format", field='order_id')
        
        # Validate amount
        if amount_xrp <= 0:
            raise ValidationError("Amount must be positive", field='amount_xrp')
        
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
        
        # Create XRPL payment using service
        xrpl_client = XRPLClient(
            network=current_app.config['XRPL_NETWORK'],
            sponsor_seed=current_app.config['XRPL_SPONSOR_SEED']
        )
        xrpl_payment_service = XRPLPaymentService(g.db, xrpl_client)
        
        payment_request = xrpl_payment_service.create_payment_request(
            user_id=user_id,
            order_id=order_id,
            amount_xrp=amount_xrp,
            destination=destination
        )
        
        logger.info(
            f"XRPL payment request created successfully",
            extra={
                'user_id': user_id,
                'order_id': order_id,
                'amount_xrp': amount_xrp
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': payment_request
        }), 201
        
    except ValidationError as e:
        logger.warning(f"XRPL payment creation validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Order not found: {order_id}")
        return jsonify(e.to_dict()), e.code
    except AuthorizationError as e:
        return jsonify(e.to_dict()), e.code
    except ValueError as e:
        logger.warning(f"XRPL payment creation failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(
            f"Unexpected error creating XRPL payment: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to create XRPL payment',
            'code': 500
        }), 500


@xrpl_payment_blueprint.route('/execute', methods=['POST'])
@jwt_required()
@validate_json_request(required_fields=['order_id'])
def execute_xrpl_payment():
    """
    Execute XRPL payment from user's wallet.
    
    POST /api/v1/payments/xrpl/execute
    
    Request Body:
        {
            "order_id": "uuid"
        }
    
    Returns:
        200: Payment executed successfully
        400: Validation error or insufficient balance
        401: Unauthorized
        404: Order or wallet not found
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get sanitized request data
        data = request.sanitized_data
        order_id = data.get('order_id')
        
        # Validate order ID format
        try:
            order_id = InputValidator.validate_uuid(order_id)
        except ValidationError:
            raise ValidationError("Invalid order ID format", field='order_id')
        
        # Execute payment using service
        xrpl_client = XRPLClient(
            network=current_app.config['XRPL_NETWORK'],
            sponsor_seed=current_app.config['XRPL_SPONSOR_SEED']
        )
        xrpl_payment_service = XRPLPaymentService(g.db, xrpl_client)
        
        result = xrpl_payment_service.execute_payment(
            user_id=user_id,
            order_id=order_id
        )
        
        logger.info(
            f"XRPL payment executed successfully",
            extra={
                'user_id': user_id,
                'order_id': order_id,
                'transaction_hash': result['transaction_hash']
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except ValidationError as e:
        logger.warning(f"XRPL payment execution validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Resource not found: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ValueError as e:
        logger.warning(f"XRPL payment execution failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(
            f"Unexpected error executing XRPL payment: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to execute XRPL payment',
            'code': 500
        }), 500


@xrpl_payment_blueprint.route('/check/<order_id>', methods=['GET'])
@jwt_required()
def check_xrpl_payment(order_id: str):
    """
    Check XRPL payment status for an order.
    
    GET /api/v1/payments/xrpl/check/{order_id}
    
    Path Parameters:
        order_id: Order UUID
    
    Returns:
        200: Payment status
        400: Invalid order ID format
        401: Unauthorized
        404: Order not found
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Validate order ID format
        try:
            order_id = InputValidator.validate_uuid(order_id)
        except ValidationError:
            raise ValidationError("Invalid order ID format", field='order_id')
        
        # Check payment status using service
        xrpl_client = XRPLClient(
            network=current_app.config['XRPL_NETWORK'],
            sponsor_seed=current_app.config['XRPL_SPONSOR_SEED']
        )
        xrpl_payment_service = XRPLPaymentService(g.db, xrpl_client)
        
        status = xrpl_payment_service.check_payment_status(
            user_id=user_id,
            order_id=order_id
        )
        
        return jsonify({
            'status': 'success',
            'data': status
        }), 200
        
    except ValidationError as e:
        logger.warning(f"XRPL payment check validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Order not found: {order_id}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error checking XRPL payment: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to check XRPL payment status',
            'code': 500
        }), 500


@xrpl_payment_blueprint.route('/verify/<transaction_hash>', methods=['GET'])
@jwt_required()
def verify_xrpl_transaction(transaction_hash: str):
    """
    Verify XRPL transaction on blockchain.
    
    GET /api/v1/payments/xrpl/verify/{transaction_hash}
    
    Path Parameters:
        transaction_hash: XRPL transaction hash
    
    Returns:
        200: Transaction details
        400: Invalid transaction hash
        401: Unauthorized
        404: Transaction not found
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Verify transaction using service
        xrpl_client = XRPLClient(
            network=current_app.config['XRPL_NETWORK'],
            sponsor_seed=current_app.config['XRPL_SPONSOR_SEED']
        )
        xrpl_payment_service = XRPLPaymentService(g.db, xrpl_client)
        
        transaction = xrpl_payment_service.verify_transaction(transaction_hash)
        
        return jsonify({
            'status': 'success',
            'data': transaction
        }), 200
        
    except ResourceNotFoundError as e:
        logger.info(f"Transaction not found: {transaction_hash}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error verifying XRPL transaction: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to verify XRPL transaction',
            'code': 500
        }), 500
