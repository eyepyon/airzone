"""
Product Blueprint for Airzone API.
Handles product CRUD operations for the e-commerce shop.

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 8.2, 8.6, 8.7
"""
from flask import Blueprint, request, jsonify, g, current_app
from middleware.auth import jwt_required, get_current_user, jwt_optional
from services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)

# Create product blueprint
product_blueprint = Blueprint('product', __name__)


def get_product_service() -> ProductService:
    """
    Get ProductService instance with current database session.
    
    Returns:
        ProductService: Configured product service
    """
    db_session = g.db
    return ProductService(db_session=db_session)


@product_blueprint.route('', methods=['GET'])
@jwt_optional
def get_products():
    """
    Get all products (public endpoint with optional authentication).
    
    Query Parameters:
        only_active: Filter by active status (default: true)
        limit: Maximum number of products to return
        offset: Number of products to skip
        search: Search term for name/description
        min_stock: Minimum stock quantity
        required_nft_id: Filter by NFT requirement
    
    Response:
        {
            "status": "success",
            "data": {
                "products": [
                    {
                        "id": "string",
                        "name": "string",
                        "description": "string",
                        "price": 0,
                        "stock_quantity": 0,
                        "image_url": "string",
                        "required_nft_id": "string",
                        "is_active": true,
                        "created_at": "string",
                        "updated_at": "string"
                    }
                ],
                "count": 0
            }
        }
    
    Requirements:
        - 4.1: Product listing
        - 8.2: GET /api/v1/products endpoint
    """
    try:
        # Get query parameters
        only_active = request.args.get('only_active', 'true').lower() == 'true'
        limit_str = request.args.get('limit')
        offset_str = request.args.get('offset')
        search = request.args.get('search')
        min_stock_str = request.args.get('min_stock')
        required_nft_id = request.args.get('required_nft_id')
        
        # Parse numeric parameters
        limit = None
        offset = None
        min_stock = None
        
        if limit_str:
            try:
                limit = int(limit_str)
                if limit <= 0:
                    raise ValueError("Limit must be positive")
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid limit parameter',
                    'code': 400
                }), 400
        
        if offset_str:
            try:
                offset = int(offset_str)
                if offset < 0:
                    raise ValueError("Offset must be non-negative")
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid offset parameter',
                    'code': 400
                }), 400
        
        if min_stock_str:
            try:
                min_stock = int(min_stock_str)
                if min_stock < 0:
                    raise ValueError("Min stock must be non-negative")
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid min_stock parameter',
                    'code': 400
                }), 400
        
        # Get products based on filters
        product_service = get_product_service()
        
        if search:
            products = product_service.search_products(
                search_term=search,
                only_active=only_active,
                limit=limit
            )
        elif min_stock is not None:
            products = product_service.get_available_products(
                min_stock=min_stock,
                only_active=only_active,
                limit=limit
            )
        elif required_nft_id is not None:
            products = product_service.get_products_by_nft_requirement(
                required_nft_id=required_nft_id if required_nft_id != 'null' else None,
                only_active=only_active
            )
            if limit:
                products = products[:limit]
        else:
            products = product_service.get_all_products(
                only_active=only_active,
                limit=limit,
                offset=offset
            )
        
        logger.info(
            f"Retrieved {len(products)} products",
            extra={'count': len(products), 'filters': request.args.to_dict()}
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'products': products,
                'count': len(products)
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving products: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve products',
            'code': 500
        }), 500


@product_blueprint.route('/<product_id>', methods=['GET'])
@jwt_optional
def get_product_details(product_id: str):
    """
    Get details of a specific product (public endpoint).
    
    Path Parameters:
        product_id: Product ID
    
    Response:
        {
            "status": "success",
            "data": {
                "product": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "price": 0,
                    "stock_quantity": 0,
                    "image_url": "string",
                    "required_nft_id": "string",
                    "is_active": true,
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 4.2: Product detail retrieval
        - 8.2: GET /api/v1/products/{id} endpoint
    """
    try:
        product_service = get_product_service()
        product = product_service.get_product(product_id)
        
        if not product:
            return jsonify({
                'status': 'error',
                'error': 'Product not found',
                'code': 404
            }), 404
        
        logger.info(
            f"Retrieved product details: {product_id}",
            extra={'product_id': product_id}
        )
        
        return jsonify({
            'status': 'success',
            'data': product
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving product details: {str(e)}",
            extra={'error': str(e), 'product_id': product_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve product details',
            'code': 500
        }), 500


@product_blueprint.route('', methods=['POST'])
@jwt_required
def create_product():
    """
    Create a new product (admin only).
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        {
            "name": "string",
            "price": 0,
            "description": "string",
            "stock_quantity": 0,
            "image_url": "string",
            "required_nft_id": "string",
            "is_active": true
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "product": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "price": 0,
                    "stock_quantity": 0,
                    "image_url": "string",
                    "required_nft_id": "string",
                    "is_active": true,
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 4.2: Product creation
        - 8.2: POST /api/v1/products endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # TODO: Add admin role check when RBAC is implemented
        # For now, any authenticated user can create products
        
        # Validate request body
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        # Validate required fields
        name = data.get('name')
        price = data.get('price')
        
        if not name:
            return jsonify({
                'status': 'error',
                'error': 'name is required',
                'code': 400
            }), 400
        
        if price is None:
            return jsonify({
                'status': 'error',
                'error': 'price is required',
                'code': 400
            }), 400
        
        try:
            price = int(price)
            if price < 0:
                raise ValueError("Price must be non-negative")
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'error': 'Invalid price value',
                'code': 400
            }), 400
        
        # Get optional fields
        description = data.get('description')
        stock_quantity = data.get('stock_quantity', 0)
        image_url = data.get('image_url')
        required_nft_id = data.get('required_nft_id')
        is_active = data.get('is_active', True)
        
        # Validate stock quantity
        try:
            stock_quantity = int(stock_quantity)
            if stock_quantity < 0:
                raise ValueError("Stock quantity must be non-negative")
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'error': 'Invalid stock_quantity value',
                'code': 400
            }), 400
        
        # Create product
        product_service = get_product_service()
        product = product_service.create_product(
            name=name,
            price=price,
            description=description,
            stock_quantity=stock_quantity,
            image_url=image_url,
            required_nft_id=required_nft_id,
            is_active=is_active
        )
        
        logger.info(
            f"Product created: {product['id']}",
            extra={
                'user_id': user_id,
                'product_id': product['id'],
                'product_name': name
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'product': product
            }
        }), 201
        
    except Exception as e:
        logger.error(
            f"Error creating product: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to create product',
            'code': 500
        }), 500


@product_blueprint.route('/<product_id>', methods=['PUT'])
@jwt_required
def update_product(product_id: str):
    """
    Update a product (admin only).
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        product_id: Product ID
    
    Request Body:
        {
            "name": "string",
            "price": 0,
            "description": "string",
            "stock_quantity": 0,
            "image_url": "string",
            "required_nft_id": "string",
            "is_active": true
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "product": {
                    "id": "string",
                    "name": "string",
                    "description": "string",
                    "price": 0,
                    "stock_quantity": 0,
                    "image_url": "string",
                    "required_nft_id": "string",
                    "is_active": true,
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 4.4: Product update
        - 8.2: PUT /api/v1/products/{id} endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # TODO: Add admin role check when RBAC is implemented
        
        # Validate request body
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        # Prepare update fields
        update_fields = {}
        
        if 'name' in data:
            update_fields['name'] = data['name']
        
        if 'price' in data:
            try:
                price = int(data['price'])
                if price < 0:
                    raise ValueError("Price must be non-negative")
                update_fields['price'] = price
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid price value',
                    'code': 400
                }), 400
        
        if 'description' in data:
            update_fields['description'] = data['description']
        
        if 'stock_quantity' in data:
            try:
                stock_quantity = int(data['stock_quantity'])
                if stock_quantity < 0:
                    raise ValueError("Stock quantity must be non-negative")
                update_fields['stock_quantity'] = stock_quantity
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'error': 'Invalid stock_quantity value',
                    'code': 400
                }), 400
        
        if 'image_url' in data:
            update_fields['image_url'] = data['image_url']
        
        if 'required_nft_id' in data:
            update_fields['required_nft_id'] = data['required_nft_id']
        
        if 'is_active' in data:
            update_fields['is_active'] = bool(data['is_active'])
        
        # Update product
        product_service = get_product_service()
        product = product_service.update_product(product_id, **update_fields)
        
        if not product:
            return jsonify({
                'status': 'error',
                'error': 'Product not found',
                'code': 404
            }), 404
        
        logger.info(
            f"Product updated: {product_id}",
            extra={
                'user_id': user_id,
                'product_id': product_id,
                'updated_fields': list(update_fields.keys())
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'product': product
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error updating product: {str(e)}",
            extra={'error': str(e), 'product_id': product_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to update product',
            'code': 500
        }), 500


@product_blueprint.route('/<product_id>', methods=['DELETE'])
@jwt_required
def delete_product(product_id: str):
    """
    Delete (deactivate) a product (admin only).
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        product_id: Product ID
    
    Response:
        {
            "status": "success",
            "data": {
                "message": "Product deleted successfully"
            }
        }
    
    Requirements:
        - 4.5: Product deletion
        - 8.2: DELETE /api/v1/products/{id} endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # TODO: Add admin role check when RBAC is implemented
        
        # Delete product
        product_service = get_product_service()
        success = product_service.delete_product(product_id)
        
        if not success:
            return jsonify({
                'status': 'error',
                'error': 'Product not found',
                'code': 404
            }), 404
        
        logger.info(
            f"Product deleted: {product_id}",
            extra={
                'user_id': user_id,
                'product_id': product_id
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'message': 'Product deleted successfully'
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error deleting product: {str(e)}",
            extra={'error': str(e), 'product_id': product_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to delete product',
            'code': 500
        }), 500
