"""
NFT Blueprint for Airzone API.
Handles NFT minting, retrieval, and status checking endpoints.

Requirements: 3.1, 3.4, 8.2, 8.6, 8.7
"""
from flask import Blueprint, request, jsonify, g, current_app
from middleware.auth import jwt_required, get_current_user
from services.nft_service import NFTService
from clients.sui_client import SuiClient
from tasks.task_manager import TaskManager
from models.nft_mint import NFTMintStatus
import logging

logger = logging.getLogger(__name__)

# Create NFT blueprint
nft_blueprint = Blueprint('nft', __name__)


def get_nft_service() -> NFTService:
    """
    Get NFTService instance with current database session.
    
    Returns:
        NFTService: Configured NFT service
    """
    db_session = g.db
    
    # Initialize Sui client with network, sponsor key, and package ID
    sui_client = SuiClient(
        network=current_app.config.get('SUI_NETWORK', 'testnet'),
        sponsor_private_key=current_app.config.get('SUI_SPONSOR_PRIVATE_KEY'),
        package_id=current_app.config.get('SUI_PACKAGE_ID')
    )
    
    # Initialize task manager
    task_manager = TaskManager(db_session=db_session)
    
    return NFTService(
        db_session=db_session,
        sui_client=sui_client,
        task_manager=task_manager
    )


@nft_blueprint.route('', methods=['GET'])
@jwt_required
def get_user_nfts():
    """
    Get all NFTs for the authenticated user.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Query Parameters:
        status: Optional status filter (pending, minting, completed, failed)
        limit: Maximum number of NFTs to return
    
    Response:
        {
            "status": "success",
            "data": {
                "nfts": [
                    {
                        "id": "string",
                        "user_id": "string",
                        "wallet_address": "string",
                        "nft_object_id": "string",
                        "transaction_digest": "string",
                        "status": "string",
                        "metadata": {},
                        "created_at": "string",
                        "updated_at": "string"
                    }
                ],
                "count": 0
            }
        }
    
    Requirements:
        - 3.4: User NFT list retrieval
        - 8.2: GET /api/v1/nfts endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Get query parameters
        status_str = request.args.get('status')
        limit_str = request.args.get('limit')
        
        # Parse status filter
        status = None
        if status_str:
            try:
                status = NFTMintStatus(status_str.lower())
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'error': f'Invalid status: {status_str}',
                    'code': 400
                }), 400
        
        # Parse limit
        limit = None
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
        
        # Get NFTs
        nft_service = get_nft_service()
        nfts = nft_service.get_user_nfts(user_id, status=status, limit=limit)
        
        logger.info(
            f"Retrieved {len(nfts)} NFTs for user: {user_id}",
            extra={'user_id': user_id, 'count': len(nfts)}
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'nfts': nfts,
                'count': len(nfts)
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving NFTs: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve NFTs',
            'code': 500
        }), 500


@nft_blueprint.route('/mint', methods=['POST'])
@jwt_required
def mint_nft():
    """
    Request NFT minting for the authenticated user.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        {
            "name": "string",
            "description": "string",
            "image_url": "string",
            "metadata": {}  # Optional additional metadata
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "task_id": "string",
                "message": "NFT minting task queued successfully"
            }
        }
    
    Requirements:
        - 3.1: NFT minting request
        - 8.2: POST /api/v1/nfts/mint endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Validate request body
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        # Validate required fields
        nft_name = data.get('name')
        nft_description = data.get('description')
        nft_image_url = data.get('image_url')
        
        if not nft_name:
            return jsonify({
                'status': 'error',
                'error': 'name is required',
                'code': 400
            }), 400
        
        if not nft_description:
            return jsonify({
                'status': 'error',
                'error': 'description is required',
                'code': 400
            }), 400
        
        if not nft_image_url:
            return jsonify({
                'status': 'error',
                'error': 'image_url is required',
                'code': 400
            }), 400
        
        # Get optional metadata
        metadata = data.get('metadata')
        
        # Queue NFT minting task
        nft_service = get_nft_service()
        task_id = nft_service.mint_nft(
            user_id=user_id,
            nft_name=nft_name,
            nft_description=nft_description,
            nft_image_url=nft_image_url,
            metadata=metadata
        )
        
        logger.info(
            f"NFT minting task queued for user: {user_id}",
            extra={
                'user_id': user_id,
                'task_id': task_id,
                'nft_name': nft_name
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'task_id': task_id,
                'message': 'NFT minting task queued successfully'
            }
        }), 202  # 202 Accepted for async operation
        
    except ValueError as e:
        logger.warning(
            f"NFT minting validation failed: {str(e)}",
            extra={'error': str(e)}
        )
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(
            f"Error queueing NFT mint: {str(e)}",
            extra={'error': str(e)},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to queue NFT minting',
            'code': 500
        }), 500


@nft_blueprint.route('/<nft_id>', methods=['GET'])
@jwt_required
def get_nft_details(nft_id: str):
    """
    Get details of a specific NFT.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        nft_id: NFT mint record ID
    
    Response:
        {
            "status": "success",
            "data": {
                "nft": {
                    "id": "string",
                    "user_id": "string",
                    "wallet_address": "string",
                    "nft_object_id": "string",
                    "transaction_digest": "string",
                    "status": "string",
                    "metadata": {},
                    "error_message": "string",
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 3.4: NFT detail retrieval
        - 8.2: GET /api/v1/nfts/{id} endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Get NFT details
        nft_service = get_nft_service()
        nft = nft_service.get_nft_by_id(nft_id)
        
        if not nft:
            return jsonify({
                'status': 'error',
                'error': 'NFT not found',
                'code': 404
            }), 404
        
        # Verify ownership
        if nft['user_id'] != user_id:
            logger.warning(
                f"User {user_id} attempted to access NFT {nft_id} owned by {nft['user_id']}",
                extra={
                    'user_id': user_id,
                    'nft_id': nft_id,
                    'owner_id': nft['user_id']
                }
            )
            return jsonify({
                'status': 'error',
                'error': 'Access denied',
                'code': 403
            }), 403
        
        logger.info(
            f"Retrieved NFT details: {nft_id}",
            extra={'user_id': user_id, 'nft_id': nft_id}
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'nft': nft
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving NFT details: {str(e)}",
            extra={'error': str(e), 'nft_id': nft_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve NFT details',
            'code': 500
        }), 500


@nft_blueprint.route('/status/<task_id>', methods=['GET'])
@jwt_required
def get_mint_status(task_id: str):
    """
    Get the status of an NFT minting task.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        task_id: Task ID returned from mint request
    
    Response:
        {
            "status": "success",
            "data": {
                "task": {
                    "id": "string",
                    "task_type": "string",
                    "status": "string",
                    "payload": {},
                    "result": {},
                    "error_message": "string",
                    "retry_count": 0,
                    "created_at": "string",
                    "updated_at": "string"
                }
            }
        }
    
    Requirements:
        - 3.1: NFT minting status tracking
        - 8.2: GET /api/v1/nfts/status/{task_id} endpoint
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Get task status
        nft_service = get_nft_service()
        task_status = nft_service.task_manager.get_task_status(task_id)
        
        if not task_status:
            return jsonify({
                'status': 'error',
                'error': 'Task not found',
                'code': 404
            }), 404
        
        # Verify task belongs to user (check payload)
        payload = task_status.get('payload', {})
        task_user_id = payload.get('user_id')
        
        if task_user_id and task_user_id != user_id:
            logger.warning(
                f"User {user_id} attempted to access task {task_id} owned by {task_user_id}",
                extra={
                    'user_id': user_id,
                    'task_id': task_id,
                    'owner_id': task_user_id
                }
            )
            return jsonify({
                'status': 'error',
                'error': 'Access denied',
                'code': 403
            }), 403
        
        logger.info(
            f"Retrieved task status: {task_id}",
            extra={
                'user_id': user_id,
                'task_id': task_id,
                'task_status': task_status.get('status')
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'task': task_status
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error retrieving task status: {str(e)}",
            extra={'error': str(e), 'task_id': task_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to retrieve task status',
            'code': 500
        }), 500
