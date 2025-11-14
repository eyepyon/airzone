"""
WiFi Blueprint for managing WiFi captive portal sessions.
Provides endpoints for WiFi connection session creation and history retrieval.

Requirements: 2.1, 2.2, 2.3, 2.4, 8.2, 8.6, 8.7
"""
import logging
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.security import validate_json_request, sanitize_query_params, InputValidator
from repositories.wifi_session_repository import WiFiSessionRepository
from exceptions import (
    ValidationError,
    ResourceNotFoundError
)

logger = logging.getLogger(__name__)

# Create blueprint
wifi_blueprint = Blueprint('wifi', __name__)


@wifi_blueprint.route('/connect', methods=['POST'])
@validate_json_request(required_fields=[])
def create_wifi_session():
    """
    Create a new WiFi connection session.
    
    POST /api/v1/wifi/connect
    
    Request Body:
        {
            "mac_address": "AA:BB:CC:DD:EE:FF",  // optional
            "ip_address": "192.168.1.100",       // optional
            "user_id": "uuid"                     // optional
        }
    
    Returns:
        201: WiFi session created successfully
        400: Validation error
        
    Requirements: 2.1, 2.2, 8.2, 8.6, 8.7
    
    Note: This endpoint does not require JWT authentication as it's called
    during the captive portal flow before user authentication.
    """
    try:
        # Get sanitized request data
        data = request.sanitized_data
        mac_address = data.get('mac_address')
        ip_address = data.get('ip_address')
        user_id = data.get('user_id')
        
        # Validate MAC address format if provided
        if mac_address:
            try:
                mac_address = InputValidator.validate_mac_address(mac_address)
            except ValidationError:
                raise ValidationError("Invalid MAC address format", field='mac_address')
        
        # Validate IP address format if provided
        if ip_address:
            try:
                ip_address = InputValidator.validate_ip_address(ip_address)
            except ValidationError:
                raise ValidationError("Invalid IP address format", field='ip_address')
        
        # Validate user ID format if provided
        if user_id:
            try:
                user_id = InputValidator.validate_uuid(user_id)
            except ValidationError:
                raise ValidationError("Invalid user ID format", field='user_id')
        
        # Create WiFi session using repository
        wifi_repo = WiFiSessionRepository(g.db)
        session = wifi_repo.create_session(
            user_id=user_id,
            mac_address=mac_address,
            ip_address=ip_address
        )
        
        logger.info(
            f"WiFi session created successfully",
            extra={
                'session_id': session.id,
                'user_id': user_id,
                'mac_address': mac_address,
                'ip_address': ip_address
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': session.to_dict()
        }), 201
        
    except ValidationError as e:
        logger.warning(f"WiFi session creation validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error creating WiFi session: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to create WiFi session',
            'code': 500
        }), 500


@wifi_blueprint.route('/sessions', methods=['GET'])
@jwt_required()
@sanitize_query_params()
def get_wifi_sessions():
    """
    Get WiFi session history for the authenticated user.
    
    GET /api/v1/wifi/sessions?limit=10
    
    Query Parameters:
        limit (optional): Maximum number of sessions to return (default: 50, max: 100)
    
    Returns:
        200: List of WiFi sessions
        400: Invalid query parameters
        401: Unauthorized
        
    Requirements: 2.4, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Get query parameters
        limit_param = request.args.get('limit', '50')
        
        # Validate and parse limit
        try:
            limit = InputValidator.validate_integer(limit_param, min_value=1, max_value=100)
        except ValidationError:
            raise ValidationError(
                "Limit must be an integer between 1 and 100",
                field='limit'
            )
        
        # Get WiFi sessions using repository
        wifi_repo = WiFiSessionRepository(g.db)
        sessions = wifi_repo.find_by_user(user_id, limit=limit)
        
        # Convert to dict
        sessions_data = [session.to_dict() for session in sessions]
        
        logger.info(
            f"Retrieved {len(sessions_data)} WiFi sessions for user",
            extra={
                'user_id': user_id,
                'count': len(sessions_data)
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'sessions': sessions_data,
                'count': len(sessions_data)
            }
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Get WiFi sessions validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error retrieving WiFi sessions: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve WiFi sessions',
            'code': 500
        }), 500


@wifi_blueprint.route('/sessions/<session_id>/disconnect', methods=['POST'])
@jwt_required()
def disconnect_wifi_session(session_id: str):
    """
    Mark a WiFi session as disconnected.
    
    POST /api/v1/wifi/sessions/{session_id}/disconnect
    
    Path Parameters:
        session_id: WiFi session UUID
    
    Returns:
        200: Session disconnected successfully
        400: Invalid session ID format
        401: Unauthorized
        404: Session not found
        
    Requirements: 2.3, 8.2, 8.6, 8.7
    """
    try:
        # Get current user
        user_id = get_jwt_identity()
        
        # Validate session ID format
        try:
            session_id = InputValidator.validate_uuid(session_id)
        except ValidationError:
            raise ValidationError("Invalid session ID format", field='session_id')
        
        # Get and verify session
        wifi_repo = WiFiSessionRepository(g.db)
        session = wifi_repo.find_by_id(session_id)
        
        if not session:
            raise ResourceNotFoundError("WiFi session", session_id)
        
        # Verify session belongs to user
        if session.user_id != user_id:
            logger.warning(
                f"User attempted to disconnect another user's session",
                extra={
                    'user_id': user_id,
                    'session_id': session_id,
                    'session_user_id': session.user_id
                }
            )
            return jsonify({
                'status': 'error',
                'error': 'You do not have permission to disconnect this session',
                'code': 403
            }), 403
        
        # Disconnect session
        updated_session = wifi_repo.disconnect_session(session_id)
        
        logger.info(
            f"WiFi session disconnected",
            extra={
                'user_id': user_id,
                'session_id': session_id
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': updated_session.to_dict()
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Disconnect session validation error: {str(e)}")
        return jsonify(e.to_dict()), e.code
    except ResourceNotFoundError as e:
        logger.info(f"WiFi session not found: {session_id}")
        return jsonify(e.to_dict()), e.code
    except Exception as e:
        logger.error(
            f"Unexpected error disconnecting WiFi session: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to disconnect WiFi session',
            'code': 500
        }), 500
