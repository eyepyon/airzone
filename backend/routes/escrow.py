"""
Escrow Blueprint for XRP staking campaigns.
"""
from flask import Blueprint, request, jsonify, g, current_app
from middleware.auth import jwt_required, get_current_user
from services.escrow_campaign_service import EscrowCampaignService
from clients.xrpl_client import XRPLClient
import logging

logger = logging.getLogger(__name__)

escrow_blueprint = Blueprint('escrow', __name__)


@escrow_blueprint.route('/campaigns', methods=['GET'])
def get_campaigns():
    """
    アクティブなキャンペーン一覧を取得
    
    Response:
        {
            "status": "success",
            "data": {
                "campaigns": [...]
            }
        }
    """
    try:
        campaigns = g.db.execute(
            """
            SELECT * FROM escrow_campaigns 
            WHERE is_active = TRUE 
            AND start_date <= NOW() 
            AND end_date >= NOW()
            ORDER BY created_at DESC
            """
        ).fetchall()
        
        return jsonify({
            'status': 'success',
            'data': {
                'campaigns': [
                    {
                        'id': c['id'],
                        'name': c['name'],
                        'description': c['description'],
                        'min_amount_xrp': c['min_amount_drops'] / 1_000_000,
                        'lock_days': c['lock_days'],
                        'nft_reward': {
                            'name': c['nft_reward_name'],
                            'description': c['nft_reward_description'],
                            'image_url': c['nft_reward_image_url'],
                        },
                        'start_date': c['start_date'].isoformat(),
                        'end_date': c['end_date'].isoformat(),
                        'max_participants': c['max_participants'],
                        'current_participants': c['current_participants'],
                    }
                    for c in campaigns
                ]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting campaigns: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get campaigns',
            'code': 500
        }), 500


@escrow_blueprint.route('/stake', methods=['POST'])
@jwt_required
def create_stake():
    """
    Escrowステークを作成
    
    Request Body:
        {
            "campaign_id": "uuid",
            "amount_xrp": 100
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "escrow_id": "uuid",
                "transaction_hash": "...",
                "finish_after": 1234567890
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': 'Request body is required',
                'code': 400
            }), 400
        
        campaign_id = data.get('campaign_id')
        amount_xrp = data.get('amount_xrp')
        
        if not campaign_id or not amount_xrp:
            return jsonify({
                'status': 'error',
                'error': 'campaign_id and amount_xrp are required',
                'code': 400
            }), 400
        
        # キャンペーン情報を取得
        campaign = g.db.execute(
            "SELECT * FROM escrow_campaigns WHERE id = :id AND is_active = TRUE",
            {'id': campaign_id}
        ).fetchone()
        
        if not campaign:
            return jsonify({
                'status': 'error',
                'error': 'Campaign not found or inactive',
                'code': 404
            }), 404
        
        # 最小金額チェック
        amount_drops = int(amount_xrp * 1_000_000)
        if amount_drops < campaign['min_amount_drops']:
            return jsonify({
                'status': 'error',
                'error': f"Minimum amount is {campaign['min_amount_drops'] / 1_000_000} XRP",
                'code': 400
            }), 400
        
        # Escrowを作成
        from config import Config
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        escrow_service = EscrowCampaignService(g.db, xrpl_client)
        result = escrow_service.create_campaign_escrow(
            user_id=user_id,
            campaign_id=campaign_id,
            amount_xrp=amount_xrp,
            lock_days=campaign['lock_days']
        )
        
        # 参加者数を更新
        g.db.execute(
            "UPDATE escrow_campaigns SET current_participants = current_participants + 1 WHERE id = :id",
            {'id': campaign_id}
        )
        g.db.commit()
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(f"Error creating stake: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to create stake',
            'code': 500
        }), 500


@escrow_blueprint.route('/my-stakes', methods=['GET'])
@jwt_required
def get_my_stakes():
    """
    自分のステーク一覧を取得
    
    Response:
        {
            "status": "success",
            "data": {
                "stakes": [...]
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        from config import Config
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        
        escrow_service = EscrowCampaignService(g.db, xrpl_client)
        stakes = escrow_service.get_user_escrows(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'stakes': stakes
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stakes: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get stakes',
            'code': 500
        }), 500
