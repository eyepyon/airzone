"""
User Importance Service for calculating user importance scores.
"""
from typing import Dict, Optional
import logging
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserImportanceService:
    """Service for calculating and managing user importance scores."""
    
    # スコア配点設定
    SCORE_WEIGHTS = {
        'purchase': 100,              # 購入1回あたり
        'referral_completed': 50,     # 紹介成功1件あたり
        'referral_click': 5,          # リファラルクリック1回あたり
        'login': 2,                   # ログイン1回あたり
        'nft_mint': 30,              # NFT発行1回あたり
        'order_amount': 0.1,         # 購入金額1円あたり
    }
    
    # 重要度レベル閾値
    IMPORTANCE_LEVELS = {
        'bronze': 0,
        'silver': 500,
        'gold': 1500,
        'platinum': 3000,
        'diamond': 5000,
    }
    
    def __init__(self, db_session: Session):
        """Initialize UserImportanceService."""
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
    
    def calculate_user_score(self, user_id: str) -> Dict:
        """
        ユーザーの重要度スコアを計算
        
        Args:
            user_id: ユーザーID
            
        Returns:
            Dict: スコア詳細
        """
        try:
            from models.user import User
            from models.referral import Referral
            from models.order import Order
            from models.nft_mint import NFTMint
            
            # 購入数
            purchase_count = self.db_session.query(func.count(Order.id))\
                .filter(Order.user_id == user_id, Order.status == 'completed')\
                .scalar() or 0
            
            # 購入金額合計
            total_purchase_amount = self.db_session.query(func.sum(Order.total_amount))\
                .filter(Order.user_id == user_id, Order.status == 'completed')\
                .scalar() or 0
            
            # 紹介成功数
            referral_count = self.db_session.query(func.count(Referral.id))\
                .filter(Referral.referrer_id == user_id, Referral.status == 'completed')\
                .scalar() or 0
            
            # リファラルクリック数
            referral_clicks = self.db_session.execute(
                """
                SELECT COUNT(*) FROM referral_clicks 
                WHERE referrer_id = :user_id
                """,
                {'user_id': user_id}
            ).scalar() or 0
            
            # ログイン数（過去90日）
            ninety_days_ago = datetime.utcnow() - timedelta(days=90)
            login_count = self.db_session.execute(
                """
                SELECT COUNT(DISTINCT DATE(created_at)) 
                FROM user_activities 
                WHERE user_id = :user_id 
                AND activity_type = 'login'
                AND created_at >= :since
                """,
                {'user_id': user_id, 'since': ninety_days_ago}
            ).scalar() or 0
            
            # NFT発行数
            nft_count = self.db_session.query(func.count(NFTMint.id))\
                .filter(NFTMint.user_id == user_id, NFTMint.status == 'completed')\
                .scalar() or 0
            
            # スコア計算
            scores = {
                'purchase_score': purchase_count * self.SCORE_WEIGHTS['purchase'],
                'referral_score': referral_count * self.SCORE_WEIGHTS['referral_completed'],
                'click_score': referral_clicks * self.SCORE_WEIGHTS['referral_click'],
                'login_score': login_count * self.SCORE_WEIGHTS['login'],
                'nft_score': nft_count * self.SCORE_WEIGHTS['nft_mint'],
                'amount_score': int(total_purchase_amount * self.SCORE_WEIGHTS['order_amount']),
            }
            
            total_score = sum(scores.values())
            
            # 重要度レベルを判定
            importance_level = self._get_importance_level(total_score)
            
            return {
                'user_id': user_id,
                'total_score': total_score,
                'importance_level': importance_level,
                'breakdown': scores,
                'metrics': {
                    'purchase_count': purchase_count,
                    'total_purchase_amount': total_purchase_amount,
                    'referral_count': referral_count,
                    'referral_clicks': referral_clicks,
                    'login_count': login_count,
                    'nft_count': nft_count,
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating user score: {str(e)}")
            raise
    
    def update_user_score(self, user_id: str, reason: str = 'manual_update') -> Dict:
        """
        ユーザーのスコアを更新
        
        Args:
            user_id: ユーザーID
            reason: 更新理由
            
        Returns:
            Dict: 更新結果
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            
            # 現在のスコアを保存
            old_score = user.importance_score or 0
            old_level = user.importance_level or 'bronze'
            
            # 新しいスコアを計算
            score_data = self.calculate_user_score(user_id)
            new_score = score_data['total_score']
            new_level = score_data['importance_level']
            
            # ユーザー情報を更新
            user.importance_score = new_score
            user.importance_level = new_level
            user.last_score_updated = datetime.utcnow()
            
            # スコア履歴を記録
            self.db_session.execute(
                """
                INSERT INTO user_score_history 
                (id, user_id, score_before, score_after, score_change, reason, details, created_at)
                VALUES (:id, :user_id, :before, :after, :change, :reason, :details, :created_at)
                """,
                {
                    'id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'before': old_score,
                    'after': new_score,
                    'change': new_score - old_score,
                    'reason': reason,
                    'details': str(score_data['breakdown']),
                    'created_at': datetime.utcnow()
                }
            )
            
            self.db_session.commit()
            
            logger.info(f"Updated user score: {user_id}, {old_score} -> {new_score}")
            
            return {
                'user_id': user_id,
                'old_score': old_score,
                'new_score': new_score,
                'score_change': new_score - old_score,
                'old_level': old_level,
                'new_level': new_level,
                'level_changed': old_level != new_level,
            }
            
        except Exception as e:
            logger.error(f"Error updating user score: {str(e)}")
            self.db_session.rollback()
            raise
    
    def update_all_user_scores(self, limit: Optional[int] = None) -> Dict:
        """
        全ユーザーのスコアを更新
        
        Args:
            limit: 更新するユーザー数の上限
            
        Returns:
            Dict: 更新結果
        """
        try:
            from models.user import User
            
            query = self.db_session.query(User)
            if limit:
                query = query.limit(limit)
            
            users = query.all()
            
            updated_count = 0
            errors = []
            
            for user in users:
                try:
                    self.update_user_score(user.id, reason='batch_update')
                    updated_count += 1
                except Exception as e:
                    errors.append({'user_id': user.id, 'error': str(e)})
            
            return {
                'total_users': len(users),
                'updated_count': updated_count,
                'error_count': len(errors),
                'errors': errors,
            }
            
        except Exception as e:
            logger.error(f"Error updating all user scores: {str(e)}")
            raise
    
    def get_top_users(self, limit: int = 100) -> list:
        """
        重要度スコアトップユーザーを取得
        
        Args:
            limit: 取得件数
            
        Returns:
            list: トップユーザーリスト
        """
        try:
            from models.user import User
            
            users = self.db_session.query(User)\
                .filter(User.importance_score > 0)\
                .order_by(User.importance_score.desc())\
                .limit(limit)\
                .all()
            
            return [
                {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'importance_score': user.importance_score,
                    'importance_level': user.importance_level,
                    'last_updated': user.last_score_updated.isoformat() if user.last_score_updated else None,
                }
                for user in users
            ]
            
        except Exception as e:
            logger.error(f"Error getting top users: {str(e)}")
            return []
    
    def track_referral_click(self, referral_code: str, ip_address: str, user_agent: str) -> Dict:
        """
        リファラルクリックを追跡
        
        Args:
            referral_code: 紹介コード
            ip_address: IPアドレス
            user_agent: ユーザーエージェント
            
        Returns:
            Dict: クリック情報
        """
        try:
            from models.user import User
            
            # 紹介者を検索
            referrer = self.db_session.query(User).filter_by(referral_code=referral_code).first()
            
            click_id = str(uuid.uuid4())
            
            self.db_session.execute(
                """
                INSERT INTO referral_clicks 
                (id, referral_code, referrer_id, ip_address, user_agent, clicked_at)
                VALUES (:id, :code, :referrer_id, :ip, :ua, :clicked_at)
                """,
                {
                    'id': click_id,
                    'code': referral_code,
                    'referrer_id': referrer.id if referrer else None,
                    'ip': ip_address,
                    'ua': user_agent,
                    'clicked_at': datetime.utcnow()
                }
            )
            
            self.db_session.commit()
            
            logger.info(f"Tracked referral click: {referral_code}")
            
            return {
                'click_id': click_id,
                'referral_code': referral_code,
                'referrer_id': referrer.id if referrer else None,
            }
            
        except Exception as e:
            logger.error(f"Error tracking referral click: {str(e)}")
            self.db_session.rollback()
            raise
    
    def _get_importance_level(self, score: int) -> str:
        """
        スコアから重要度レベルを判定
        
        Args:
            score: スコア
            
        Returns:
            str: 重要度レベル
        """
        if score >= self.IMPORTANCE_LEVELS['diamond']:
            return 'diamond'
        elif score >= self.IMPORTANCE_LEVELS['platinum']:
            return 'platinum'
        elif score >= self.IMPORTANCE_LEVELS['gold']:
            return 'gold'
        elif score >= self.IMPORTANCE_LEVELS['silver']:
            return 'silver'
        else:
            return 'bronze'
    
    def get_level_badge(self, level: str) -> str:
        """
        レベルに応じたバッジを取得
        
        Args:
            level: 重要度レベル
            
        Returns:
            str: バッジ絵文字
        """
        badges = {
            'bronze': '🥉',
            'silver': '🥈',
            'gold': '🥇',
            'platinum': '💎',
            'diamond': '👑',
        }
        return badges.get(level, '🥉')
