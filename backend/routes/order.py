"""
Order Blueprint for managing e-commerce orders.
Provides endpoints for order creation, retrieval, and management.

Requirements: 5.1, 5.2, 5.3, 5.4, 8.2, 8.6, 8.7
"""
import logging
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.security import validate_json_request, sanitize_query_params, InputValidator
from services.order_service import OrderService
from utils.activity_logger import activity_logger
from exceptions import (
    ValidationError,
    ResourceNotFoundError,
    AuthorizationError
)

logger = logging.getLogger(__name__)

# Create blueprint
order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('', methods=['POST'])
@jwt_required()
@validate_json_request(required_fields=['items'])
def create_order():
    """
    Create a new order.
    
    POST /api/v1/orders
    
    Request Body:
        {
            "items": [
                {
                    "product_id": "uuid",
                    "quantity": 1
                }
            ]
        }
    
    Returns:
        201: Order created successfully
        400: Validation error
        401: Unauthorized
        403: NFT requirement not met
        409: Insufficient stock
        
    Requirements: 5.1, 5.2, 5.3, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get sanitized request data
        data = request.sanitized_data
        items = data.get('items', [])
        
        # Validate items structure
        if not isinstance(items, list) or len(items) == 0:
            raise ValidationError("Items must be a non-empty array")
        
        # Validate each item
        validated_items = []
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValidationError(f"Item at index {idx} must be an object")
            
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            if not product_id:
                raise ValidationError(
                    f"product_id is required for item at index {idx}",
                    field=f"items[{idx}].product_id"
                )
            
            # Validate UUID format
            try:
                product_id = InputValidator.validate_uuid(product_id)
            except ValidationError:
                raise ValidationError(
                    f"Invalid product_id format at index {idx}",
                    field=f"items[{idx}].product_id"
                )
            
            # Validate quantity
            try:
                quantity = InputValidator.validate_positive_integer(quantity)
            except ValidationError:
                raise ValidationError(
                    f"Quantity must be a positive integer at index {idx}",
                    field=f"items[{idx}].quantity"
                )
            
            validated_items.append({
                'product_id': product_id,
                'quantity': quantity
            })
        
        # Create order using service
        order_service = OrderService(g.db)
        order = order_service.create_order(user_id, validated_items)
        
        # Log purchase activity for tracking
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            activity_logger.log_purchase(
                user_id,
                order['id'],
                order['total_amount'],
                ip_address,
                user_agent
            )
        except Exception as e:
            logger.warning(f"Failed to log purchase activity: {e}")
        
        logger.info(
            f"Order created successfully",
            extra={
                'user_id': user_id,
                'order_id': order['id'],
                'total_amount': order['total_amount']
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': order
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Order creation validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ValueError as e:
        # Handle business logic errors from service
        logger.warning(f"Order creation failed: {str(e)}")
        error_msg = str(e)
        
        # Determine appropriate error code
        if 'NFT' in error_msg or 'nft' in error_msg.lower():
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 403
            }), 403
        elif 'stock' in error_msg.lower():
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 409
            }), 409
        else:
            return jsonify({
                'status': 'error',
                'error': error_msg,
                'code': 400
            }), 400
    except Exception as e:
        logger.error(
            f"Unexpected error creating order: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to create order',
            'code': 500
        }), 500


@order_blueprint.route('', methods=['GET'])
@jwt_required()
@sanitize_query_params()
def get_user_orders():
    """
    Get user's order history.
    
    GET /api/v1/orders?status=completed&limit=10
    
    Query Parameters:
        status (optional): Filter by order status (pending, processing, completed, failed, cancelled)
        limit (optional): Maximum number of orders to return (default: 50, max: 100)
    
    Returns:
        200: List of orders
        400: Invalid query parameters
        401: Unauthorized
        
    Requirements: 5.4, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get query parameters
        status_param = request.args.get('status')
        limit_param = request.args.get('limit', '50')
        
        # Validate and parse status
        status = None
        if status_param:
            from models.order import OrderStatus
            try:
                status = OrderStatus(status_param.lower())
            except ValueError:
                valid_statuses = [s.value for s in OrderStatus]
                raise ValidationError(
                    f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                    field='status'
                )
        
        # Validate and parse limit
        try:
            limit = InputValidator.validate_integer(limit_param, min_value=1, max_value=100)
        except ValidationError:
            raise ValidationError(
                "Limit must be an integer between 1 and 100",
                field='limit'
            )
        
        # Get orders using service
        order_service = OrderService(g.db)
        orders = order_service.get_user_orders(user_id, status=status, limit=limit)
        
        logger.info(
            f"Retrieved {len(orders)} orders for user",
            extra={
                'user_id': user_id,
                'status_filter': status.value if status else None,
                'count': len(orders)
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'orders': orders,
                'count': len(orders)
            }
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Get orders validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving orders: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve orders',
            'code': 500
        }), 500


@order_blueprint.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order_detail(order_id: str):
    """
    Get order details by ID.
    
    GET /api/v1/orders/{order_id}
    
    Path Parameters:
        order_id: Order UUID
    
    Returns:
        200: Order details
        400: Invalid order ID format
        401: Unauthorized
        403: Order does not belong to user
        404: Order not found
        
    Requirements: 5.4, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Validate order ID format
        try:
            order_id = InputValidator.validate_uuid(order_id)
        except ValidationError:
            raise ValidationError("Invalid order ID format", field='order_id')
        
        # Get order using service
        order_service = OrderService(g.db)
        order = order_service.get_order(order_id)
        
        if not order:
            raise ResourceNotFoundError("Order", order_id)
        
        # Verify order belongs to user
        if order['user_id'] != user_id:
            logger.warning(
                f"User attempted to access another user's order",
                extra={
                    'user_id': user_id,
                    'order_id': order_id,
                    'order_user_id': order['user_id']
                }
            )
            raise AuthorizationError("You do not have permission to access this order")
        
        logger.info(
            f"Retrieved order details",
            extra={
                'user_id': user_id,
                'order_id': order_id
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': order
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Get order validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"Order not found: {order_id}")
        return jsonify(e.to_dict()), e.code
    except AuthorizationError as e:
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving order: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve order',
            'code': 500
        }), 500
