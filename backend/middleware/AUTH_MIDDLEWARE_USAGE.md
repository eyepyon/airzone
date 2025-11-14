# JWT Authentication Middleware Usage Guide

## Overview

The JWT authentication middleware provides decorators and helper functions for protecting API routes with JWT token authentication.

**Location**: `backend/middleware/auth.py`

**Requirements**: 6.1, 6.7

## Components

### 1. `@jwt_required` Decorator

Protects routes by requiring a valid JWT access token in the Authorization header.

**Usage**:
```python
from flask import Blueprint, jsonify
from middleware.auth import jwt_required, get_current_user

api = Blueprint('api', __name__)

@api.route('/protected')
@jwt_required
def protected_route():
    user = get_current_user()
    return jsonify({
        'status': 'success',
        'data': {
            'message': f'Hello user {user["user_id"]}'
        }
    })
```

**Request Format**:
```
GET /api/v1/protected
Authorization: Bearer <jwt_token>
```

**Response on Success** (200):
```json
{
  "status": "success",
  "data": {
    "message": "Hello user 123"
  }
}
```

**Response on Failure** (401):
```json
{
  "status": "error",
  "error": "Authorization token is missing",
  "code": 401
}
```

### 2. `get_current_user()` Helper

Retrieves the authenticated user information from the request context.

**Usage**:
```python
from middleware.auth import jwt_required, get_current_user

@app.route('/user/profile')
@jwt_required
def get_profile():
    user = get_current_user()
    # user contains:
    # {
    #   'user_id': 'uuid',
    #   'token_type': 'access',
    #   'issued_at': timestamp,
    #   'expires_at': timestamp
    # }
    return jsonify({'user_id': user['user_id']})
```

### 3. `get_current_user_id()` Helper

Convenience function to get just the user ID.

**Usage**:
```python
from middleware.auth import jwt_required, get_current_user_id

@app.route('/user/orders')
@jwt_required
def get_orders():
    user_id = get_current_user_id()
    orders = order_service.get_user_orders(user_id)
    return jsonify({'orders': orders})
```

### 4. `@jwt_optional` Decorator

Allows routes to work with or without authentication.

**Usage**:
```python
from middleware.auth import jwt_optional, get_current_user

@app.route('/products')
@jwt_optional
def list_products():
    user = get_current_user()
    
    if user:
        # Show personalized products
        products = product_service.get_personalized_products(user['user_id'])
    else:
        # Show public products
        products = product_service.get_public_products()
    
    return jsonify({'products': products})
```

## Complete Example: Protected API Route

```python
from flask import Blueprint, jsonify, request, g
from middleware.auth import jwt_required, get_current_user, get_current_user_id
from services.nft_service import NFTService

nft_blueprint = Blueprint('nft', __name__)

@nft_blueprint.route('', methods=['GET'])
@jwt_required
def get_user_nfts():
    """
    Get all NFTs owned by the authenticated user.
    
    Requires: JWT access token
    Returns: List of NFTs
    """
    try:
        # Get authenticated user ID
        user_id = get_current_user_id()
        
        # Get database session
        db = g.db
        
        # Initialize service
        nft_service = NFTService(db)
        
        # Get user's NFTs
        nfts = nft_service.get_user_nfts(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'nfts': [nft.to_dict() for nft in nfts]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 500
        }), 500


@nft_blueprint.route('/mint', methods=['POST'])
@jwt_required
def mint_nft():
    """
    Request NFT minting for authenticated user.
    
    Requires: JWT access token
    Returns: Task ID for tracking mint status
    """
    try:
        user = get_current_user()
        user_id = user['user_id']
        
        # Get request data
        data = request.get_json()
        
        # Initialize service
        db = g.db
        nft_service = NFTService(db)
        
        # Queue NFT mint task
        task_id = nft_service.mint_nft(user_id, data)
        
        return jsonify({
            'status': 'success',
            'data': {
                'task_id': task_id,
                'message': 'NFT minting queued'
            }
        }), 202
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 500
        }), 500
```

## Error Handling

The middleware handles various authentication errors:

### Missing Token
```json
{
  "status": "error",
  "error": "Authorization token is missing",
  "code": 401
}
```

### Invalid Token Format
```json
{
  "status": "error",
  "error": "Invalid token",
  "code": 401
}
```

### Expired Token
```json
{
  "status": "error",
  "error": "Token has expired",
  "code": 401
}
```

### Invalid Token Type
```json
{
  "status": "error",
  "error": "Invalid token type",
  "code": 401
}
```

## Security Features

1. **Bearer Token Authentication**: Follows OAuth 2.0 standard
2. **Token Verification**: Validates signature, expiration, and type
3. **Secure Context**: User info stored in Flask `g` object (request-scoped)
4. **Logging**: All authentication events are logged for security auditing
5. **Error Handling**: Proper error messages without leaking sensitive info

## Integration with AuthService

The middleware works with the `AuthService` for token generation:

```python
from services.auth_service import AuthService
from middleware.auth import jwt_required, get_current_user

# Generate token (in auth route)
auth_service = AuthService(db, google_client, jwt_secret)
user_dict, access_token, refresh_token = auth_service.authenticate_google(id_token)

# Use token (in protected route)
@app.route('/protected')
@jwt_required
def protected():
    user = get_current_user()
    return jsonify({'user_id': user['user_id']})
```

## Testing

To test protected routes:

1. **Get a token** from the auth endpoint:
```bash
curl -X POST http://localhost:5000/api/v1/auth/google \
  -H "Content-Type: application/json" \
  -d '{"id_token": "google_id_token"}'
```

2. **Use the token** in protected routes:
```bash
curl http://localhost:5000/api/v1/nfts \
  -H "Authorization: Bearer <access_token>"
```

## Best Practices

1. **Always use `@jwt_required`** for routes that need authentication
2. **Use `get_current_user_id()`** when you only need the user ID
3. **Use `@jwt_optional`** for routes that can work with or without auth
4. **Handle exceptions** in your route handlers
5. **Log security events** for audit trails
6. **Never log tokens** in production

## Next Steps

After implementing this middleware, you can:

1. Create auth routes (task 8.2)
2. Protect NFT routes (task 8.3)
3. Protect product routes (task 8.4)
4. Protect order routes (task 8.5)
5. Protect payment routes (task 8.6)
6. Protect WiFi routes (task 8.7)
