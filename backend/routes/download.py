"""
Download Blueprint for Airzone API.
Handles product download tracking and file delivery.
"""
from flask import Blueprint, request, jsonify, g
from middleware.auth import jwt_required, get_current_user
from utils.activity_logger import activity_logger
import logging

logger = logging.getLogger(__name__)

download_blueprint = Blueprint('download', __name__)


@download_blueprint.route('/product/<product_id>', methods=['POST'])
@jwt_required
def track_download(product_id: str):
    """
    Track product download activity.
    
    This endpoint should be called when a user downloads a product.
    It records the download activity for DAU/MAU and download count tracking.
    
    Path Parameters:
        product_id: Product ID being downloaded
    
    Response:
        {
            "status": "success",
            "data": {
                "message": "Download tracked successfully"
            }
        }
    """
    try:
        # Get current user
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Log download activity
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        activity_logger.log_download(user_id, product_id, ip_address, user_agent)
        
        logger.info(
            f"Download tracked: user={user_id}, product={product_id}",
            extra={
                'user_id': user_id,
                'product_id': product_id
            }
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'message': 'Download tracked successfully'
            }
        }), 200
        
    except Exception as e:
        logger.error(
            f"Error tracking download: {str(e)}",
            extra={'error': str(e), 'product_id': product_id},
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Failed to track download',
            'code': 500
        }), 500
