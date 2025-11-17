"""
Referral Blueprint for referral system.
"""
from flask import Blueprint, request, jsonify, g, current_app
from middleware.auth import jwt_required, get_current_user
from services.referral_service import ReferralService
import logging

logger = logging.getLogger(__name__)

referral_blueprint = Blueprint('referral', __name__)


@referral_blueprint.route('/code', methods=['GET'])
@jwt_required
def get_referral_code():
    """
    自分の紹介コードを取得
    
    Response:
        {
            "status": "success",
            "data": {
                "referral_code": "ABC12345",
                "referral_link": "https://airz.one?ref=ABC12345",
                "share_links": {
                    "twitter": "...",
                    "facebook": "...",
                    "line": "..."
                }
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        referral_service = ReferralService(g.db)
        
        # 紹介コードを生成/取得
        code = referral_service.generate_referral_code(user_id)
        base_url = current_app.config.get('FRONTEND_URL', 'https://airz.one')
        link = referral_service.get_referral_link(user_id, base_url)
        
        # SNSシェアリンク
        share_text = "Airzoneに参加しよう！限定商品が買えるよ🎁"
        share_links = {
            'twitter': f"https://twitter.com/intent/tweet?text={share_text}&url={link}",
            'facebook': f"https://www.facebook.com/sharer/sharer.php?u={link}",
            'line': f"https://line.me/R/msg/text/?{share_text}%20{link}",
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'referral_code': code,
                'referral_link': link,
                'share_links': share_links,
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting referral code: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get referral code',
            'code': 500
        }), 500


@referral_blueprint.route('/apply', methods=['POST'])
@jwt_required
def apply_referral():
    """
    紹介コードを適用
    
    Request Body:
        {
            "referral_code": "ABC12345"
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "referrer_name": "John Doe",
                "message": "紹介コードが適用されました"
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        data = request.get_json()
        if not data or 'referral_code' not in data:
            return jsonify({
                'status': 'error',
                'error': 'referral_code is required',
                'code': 400
            }), 400
        
        referral_code = data['referral_code'].strip().upper()
        
        referral_service = ReferralService(g.db)
        result = referral_service.apply_referral_code(user_id, referral_code)
        
        return jsonify({
            'status': 'success',
            'data': {
                'referrer_name': result['referrer_name'],
                'message': '紹介コードが適用されました！限定商品が購入可能になりました。',
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 400
        }), 400
    except Exception as e:
        logger.error(f"Error applying referral code: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to apply referral code',
            'code': 500
        }), 500


@referral_blueprint.route('/stats', methods=['GET'])
@jwt_required
def get_referral_stats():
    """
    紹介統計を取得
    
    Response:
        {
            "status": "success",
            "data": {
                "total_referrals": 10,
                "completed_referrals": 8,
                "pending_referrals": 2,
                "total_coins_earned": 800,
                "current_coins": 500
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        referral_service = ReferralService(g.db)
        
        # 紹介履歴を取得
        referrals = referral_service.get_user_referrals(user_id)
        
        # 統計を計算
        total = len(referrals)
        completed = sum(1 for r in referrals if r['status'] == 'completed')
        pending = sum(1 for r in referrals if r['status'] == 'pending')
        total_coins_earned = sum(r['coins_awarded'] for r in referrals)
        current_coins = referral_service.get_user_coins(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_referrals': total,
                'completed_referrals': completed,
                'pending_referrals': pending,
                'total_coins_earned': total_coins_earned,
                'current_coins': current_coins,
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting referral stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get referral stats',
            'code': 500
        }), 500


@referral_blueprint.route('/history', methods=['GET'])
@jwt_required
def get_referral_history():
    """
    紹介履歴を取得
    
    Response:
        {
            "status": "success",
            "data": {
                "referrals": [...],
                "coin_transactions": [...]
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        referral_service = ReferralService(g.db)
        
        referrals = referral_service.get_user_referrals(user_id)
        transactions = referral_service.get_coin_transactions(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'referrals': referrals,
                'coin_transactions': transactions,
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting referral history: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get referral history',
            'code': 500
        }), 500


@referral_blueprint.route('/coins', methods=['GET'])
@jwt_required
def get_coins():
    """
    コイン残高を取得
    
    Response:
        {
            "status": "success",
            "data": {
                "coins": 500
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        referral_service = ReferralService(g.db)
        coins = referral_service.get_user_coins(user_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'coins': coins
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting coins: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get coins',
            'code': 500
        }), 500
