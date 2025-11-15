"""
Authentication Blueprint for Airzone API.
Handles Google OAuth authentication, token refresh, and user information endpoints.

Requirements: 1.1, 1.4, 1.5, 8.2, 8.6, 8.7
"""
from flask import Blueprint, request, jsonify, g, current_app
from middleware.auth import jwt_required, get_current_user
from services.auth_service import AuthService
from clients.google_auth import GoogleAuthClient
import logging

logger = logging.getLogger(__name__)

# Create auth blueprint
auth_blueprint = Blueprint('auth', __name__)


def get_auth_service() -> AuthService:
    """
    Get AuthService instance with current database session.
    
    Returns:
        AuthService: Configured authentication service
    """
    db_session = g.db
    google_client = GoogleAuthClient(
        client_id=current_app.config['GOOGLE_CLIENT_ID']
    )
    jwt_secret = current_app.config['JWT_SECRET_KEY']
    
    # Get JWT expiration times (convert timedelta to seconds if needed)
    jwt_access_expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)
    jwt_refresh_expires = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000)
    
    # Convert timedelta to seconds if necessary
    if hasattr(jwt_access_expires, 'total_seconds'):
        jwt_access_expires = int(jwt_access_expires.total_seconds())
    if hasattr(jwt_refresh_expires, 'total_seconds'):
        jwt_refresh_expires = int(jwt_refresh_expires.total_seconds())
    
    return AuthService(
        db_session=db_session,
        google_client=google_client,
        jwt_secret=jwt_secret,
        jwt_access_expires=jwt_access_expires,
        jwt_refresh_expires=jwt_refresh_expires
    )


@auth_blueprint.route('/google', methods=['POST'])
def google_auth():
    """
    Authenticate user with Google OAuth ID token.
    
    Request Body:
        {
            "id_token": "string"  # Google OAuth ID token
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "user": {
                    "id": "string",
                    "email": "string",
                    "name": "string",
                    "created_at": "string",
                    "updated_at": "string"
                },
                "access_token": "string",
                "refresh_token": "string",
                "token_type": "Bearer",
                "expires_in": 3600
            }
        }
    
    Requirements:
        - 1.1: Google OAuth authentication
        - 1.4: JWT access token generation (1 hour expiration)
        - 1.5: JWT refresh token generation (30 days expiration)
        - 8.2: POST /api/v1/auth/google endpoint
    """
    try:
        # Validate request body
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        id_token = data.get('id_token')
        if not id_token:
            return jsonify({
                'status': 'error',
                'error': 'id_token is required',
                'code': 400
            }), 400
        
        # Authenticate with Google
        auth_service = get_auth_service()
        user_dict, access_token, refresh_token = auth_service.authenticate_google(id_token)
        
        logger.info(
            f"User authenticated successfully: {user_dict['id']}",
            extra={
                'user_id': user_dict['id'],
                'email': user_dict['email']
            }
        )
        
        # Get expires_in and convert to seconds if needed
        expires_in = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)
        if hasattr(expires_in, 'total_seconds'):
            expires_in = int(expires_in.total_seconds())
        
        # Return success response
        return jsonify({
            'status': 'success',
            'data': {
                'user': user_dict,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': expires_in
            }
        }), 200
        
    except ValueError as e:
        logger.warning(
            f"Authentication failed: {str(e)}",
            extra={'error': str(e)}
        )
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 401
        }), 401
    except Exception as e:
        logger.error(
            f"Unexpected error during authentication: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Authentication failed',
            'code': 500
        }), 500


@auth_blueprint.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh access token using refresh token.
    
    Request Body:
        {
            "refresh_token": "string"  # JWT refresh token
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "access_token": "string",
                "token_type": "Bearer",
                "expires_in": 3600
            }
        }
    
    Requirements:
        - 1.5: Token refresh functionality
        - 8.2: POST /api/v1/auth/refresh endpoint
    """
    try:
        # Validate request body
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        refresh_token_str = data.get('refresh_token')
        if not refresh_token_str:
            return jsonify({
                'status': 'error',
                'error': 'refresh_token is required',
                'code': 400
            }), 400
        
        # Refresh access token
        auth_service = get_auth_service()
        new_access_token = auth_service.refresh_access_token(refresh_token_str)
        
        logger.info("Access token refreshed successfully")
        
        # Get expires_in and convert to seconds if needed
        expires_in = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)
        if hasattr(expires_in, 'total_seconds'):
            expires_in = int(expires_in.total_seconds())
        
        # Return success response
        return jsonify({
            'status': 'success',
            'data': {
                'access_token': new_access_token,
                'token_type': 'Bearer',
                'expires_in': expires_in
            }
        }), 200
        
    except ValueError as e:
        logger.warning(
            f"Token refresh failed: {str(e)}",
            extra={'error': str(e)}
        )
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 401
        }), 401
    except Exception as e:
        logger.error(
            f"Unexpected error during token refresh: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Token refresh failed',
            'code': 500
        }), 500


@auth_blueprint.route('/me', methods=['GET'])
@jwt_required
def get_current_user_info():
    """
    Get current authenticated user information.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "status": "success",
            "data": {
                "user": {
                    "id": "string",
                    "email": "string",
                    "name": "string",
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 6.1: JWT authentication verification
        - 8.2: GET /api/v1/auth/me endpoint
    """
    try:
        # Get current user from request context (set by jwt_required decorator)
        current_user = get_current_user()
        
        if not current_user:
            return jsonify({
                'status': 'error',
                'error': 'User not found',
                'code': 404
            }), 404
        
        user_id = current_user['user_id']
        
        # Get full user information from database
        auth_service = get_auth_service()
        from repositories.user_repository import UserRepository
        from repositories.wallet_repository import WalletRepository
        
        user_repo = UserRepository(g.db)
        wallet_repo = WalletRepository(g.db)
        
        user = user_repo.find_by_id(user_id)
        
        if not user:
            logger.warning(
                f"User not found in database: {user_id}",
                extra={'user_id': user_id}
            )
            return jsonify({
                'status': 'error',
                'error': 'User not found',
                'code': 404
            }), 404
        
        # Get user's wallet
        wallet = wallet_repo.find_by_user_id(user_id)
        
        logger.info(
            f"Retrieved user information: {user_id}",
            extra={'user_id': user_id}
        )
        
        # Return user and wallet information
        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_dict(),
                'wallet': wallet.to_dict() if wallet else None
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving user information: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve user information',
            'code': 500
        }), 500
