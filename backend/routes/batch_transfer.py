"""
Batch Transfer API Routes
XRPLのBatch Transactions機能を使った一括送金API
"""
from flask import Blueprint, request, jsonify
from services.batch_transfer_service import BatchTransferService
from clients.xrpl_client import XRPLClient
from middleware.auth import require_auth, require_admin
import os
import logging

logger = logging.getLogger(__name__)

batch_transfer_bp = Blueprint('batch_transfer', __name__)

# XRPL Client初期化
xrpl_network = os.getenv('XRPL_NETWORK', 'testnet')
xrpl_sponsor_seed = os.getenv('XRPL_SPONSOR_SEED')
xrpl_client = XRPLClient(network=xrpl_network, sponsor_seed=xrpl_sponsor_seed)

# Batch Transfer Service初期化
batch_transfer_service = BatchTransferService(xrpl_client)


@batch_transfer_bp.route('/batch-transfer/send', methods=['POST'])
@require_admin
def send_batch_transfer(current_user):
    """
    複数のユーザーに一括でXRPを送信
    
    Request Body:
        {
            "user_ids": [1, 2, 3, ...],
            "amount_xrp": 10.0,
            "reason": "Monthly reward"
        }
    """
    try:
        data = request.get_json()
        
        user_ids = data.get('user_ids', [])
        amount_xrp = data.get('amount_xrp')
        reason = data.get('reason', 'Batch transfer')
        
        if not user_ids:
            return jsonify({'error': 'user_ids is required'}), 400
        
        if not amount_xrp or amount_xrp <= 0:
            return jsonify({'error': 'Valid amount_xrp is required'}), 400
        
        # スポンサーウォレットから送信
        if not xrpl_sponsor_seed:
            return jsonify({'error': 'Sponsor wallet not configured'}), 500
        
        result = batch_transfer_service.send_batch_rewards(
            sender_wallet_seed=xrpl_sponsor_seed,
            user_ids=user_ids,
            amount_xrp=amount_xrp,
            reason=reason
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Batch transfer failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@batch_transfer_bp.route('/batch-transfer/send-to-vip', methods=['POST'])
@require_admin
def send_batch_to_vip(current_user):
    """
    VIPユーザーに一括でXRPを送信
    
    Request Body:
        {
            "min_importance_level": "Gold",
            "amount_xrp": 10.0,
            "reason": "VIP monthly reward"
        }
    """
    try:
        data = request.get_json()
        
        min_importance_level = data.get('min_importance_level', 'Bronze')
        amount_xrp = data.get('amount_xrp')
        reason = data.get('reason', 'VIP reward')
        
        if not amount_xrp or amount_xrp <= 0:
            return jsonify({'error': 'Valid amount_xrp is required'}), 400
        
        valid_levels = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
        if min_importance_level not in valid_levels:
            return jsonify({'error': f'Invalid importance level. Must be one of: {valid_levels}'}), 400
        
        # スポンサーウォレットから送信
        if not xrpl_sponsor_seed:
            return jsonify({'error': 'Sponsor wallet not configured'}), 500
        
        result = batch_transfer_service.send_batch_to_vip_users(
            sender_wallet_seed=xrpl_sponsor_seed,
            min_importance_level=min_importance_level,
            amount_xrp=amount_xrp,
            reason=reason
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"VIP batch transfer failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@batch_transfer_bp.route('/batch-transfer/send-to-top-referrers', methods=['POST'])
@require_admin
def send_batch_to_top_referrers(current_user):
    """
    トップ紹介者に一括でXRPを送信
    
    Request Body:
        {
            "top_n": 10,
            "amount_xrp": 50.0,
            "reason": "Top referrer reward"
        }
    """
    try:
        data = request.get_json()
        
        top_n = data.get('top_n', 10)
        amount_xrp = data.get('amount_xrp')
        reason = data.get('reason', 'Top referrer reward')
        
        if not amount_xrp or amount_xrp <= 0:
            return jsonify({'error': 'Valid amount_xrp is required'}), 400
        
        if top_n <= 0 or top_n > 1000:
            return jsonify({'error': 'top_n must be between 1 and 1000'}), 400
        
        # スポンサーウォレットから送信
        if not xrpl_sponsor_seed:
            return jsonify({'error': 'Sponsor wallet not configured'}), 500
        
        result = batch_transfer_service.send_batch_to_top_referrers(
            sender_wallet_seed=xrpl_sponsor_seed,
            top_n=top_n,
            amount_xrp=amount_xrp,
            reason=reason
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Top referrer batch transfer failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@batch_transfer_bp.route('/batch-transfer/history', methods=['GET'])
@require_admin
def get_batch_transfer_history(current_user):
    """
    バッチ送信履歴を取得
    
    Query Parameters:
        - limit: 取得件数（デフォルト: 100）
        - offset: オフセット（デフォルト: 0）
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        result = batch_transfer_service.get_batch_transfer_history(
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Failed to get batch transfer history: {str(e)}")
        return jsonify({'error': str(e)}), 500


@batch_transfer_bp.route('/batch-transfer/preview', methods=['POST'])
@require_admin
def preview_batch_transfer(current_user):
    """
    バッチ送信のプレビュー（実際には送信しない）
    
    Request Body:
        {
            "user_ids": [1, 2, 3, ...],
            "amount_xrp": 10.0
        }
    """
    try:
        from backend.database.connection import get_db_connection
        
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        amount_xrp = data.get('amount_xrp', 0)
        
        if not user_ids:
            return jsonify({'error': 'user_ids is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ユーザー情報を取得
        placeholders = ','.join(['%s'] * len(user_ids))
        query = f"""
            SELECT id, email, wallet_address, importance_level
            FROM users
            WHERE id IN ({placeholders})
        """
        cursor.execute(query, user_ids)
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # プレビュー情報を作成
        valid_users = [u for u in users if u['wallet_address']]
        invalid_users = [u for u in users if not u['wallet_address']]
        
        total_amount = len(valid_users) * amount_xrp
        
        return jsonify({
            'total_users': len(users),
            'valid_users': len(valid_users),
            'invalid_users': len(invalid_users),
            'amount_per_user_xrp': amount_xrp,
            'total_amount_xrp': total_amount,
            'users': valid_users,
            'users_without_wallet': [{'id': u['id'], 'email': u['email']} for u in invalid_users]
        }), 200
        
    except Exception as e:
        logger.error(f"Preview failed: {str(e)}")
        return jsonify({'error': str(e)}), 500
