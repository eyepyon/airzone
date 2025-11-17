"""
Referral Service for managing referral system.
"""
from typing import Optional, Dict, List
import logging
import uuid
import random
import string
from sqlalchemy.orm import Session
from models.referral import Referral, ReferralStatus, CoinTransaction
from repositories.user_repository import UserRepository
from datetime import datetime

logger = logging.getLogger(__name__)


class ReferralService:
    """Service for referral operations."""
    
    # 設定
    REFERRAL_BONUS_COINS = 100  # 紹介成功時のコイン
    REFERRAL_CODE_LENGTH = 8
    
    def __init__(self, db_session: Session):
        """Initialize ReferralService."""
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
    
    def generate_referral_code(self, user_id: str) -> str:
        """
        ユーザーの紹介コードを生成
        
        Args:
            user_id: ユーザーID
            
        Returns:
            str: 紹介コード
        """
        try:
            # ユーザーを取得
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            
            # 既に紹介コードがある場合は返す
            if user.referral_code:
                return user.referral_code
            
            # 新しい紹介コードを生成（ユニークになるまで）
            while True:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.REFERRAL_CODE_LENGTH))
                
                # 既存チェック
                existing = self.db_session.query(self.user_repo.model).filter_by(referral_code=code).first()
                if not existing:
                    break
            
            # ユーザーに紹介コードを設定
            user.referral_code = code
            self.db_session.commit()
            
            logger.info(f"Generated referral code for user {user_id}: {code}")
            return code
            
        except Exception as e:
            logger.error(f"Error generating referral code: {str(e)}")
            self.db_session.rollback()
            raise
    
    def get_referral_link(self, user_id: str, base_url: str = "https://airz.one") -> str:
        """
        紹介リンクを取得
        
        Args:
            user_id: ユーザーID
            base_url: ベースURL
            
        Returns:
            str: 紹介リンク
        """
        code = self.generate_referral_code(user_id)
        return f"{base_url}?ref={code}"
    
    def apply_referral_code(self, new_user_id: str, referral_code: str) -> Optional[Dict]:
        """
        紹介コードを適用
        
        Args:
            new_user_id: 新規ユーザーID
            referral_code: 紹介コード
            
        Returns:
            Optional[Dict]: 紹介情報
        """
        try:
            # 新規ユーザーを取得
            new_user = self.user_repo.find_by_id(new_user_id)
            if not new_user:
                raise ValueError(f"User not found: {new_user_id}")
            
            # 既に紹介済みの場合はエラー
            if new_user.referred_by:
                raise ValueError("User already has a referrer")
            
            # 紹介者を検索
            referrer = self.db_session.query(self.user_repo.model).filter_by(referral_code=referral_code).first()
            if not referrer:
                raise ValueError(f"Invalid referral code: {referral_code}")
            
            # 自己紹介チェック
            if referrer.id == new_user_id:
                raise ValueError("Cannot refer yourself")
            
            # 紹介関係を作成
            referral = Referral(
                id=str(uuid.uuid4()),
                referrer_id=referrer.id,
                referred_id=new_user_id,
                status=ReferralStatus.PENDING,
                coins_awarded=0
            )
            self.db_session.add(referral)
            
            # 新規ユーザーに紹介者を設定
            new_user.referred_by = referrer.id
            
            self.db_session.commit()
            
            logger.info(f"Applied referral code {referral_code} for user {new_user_id}")
            
            return {
                'referral_id': referral.id,
                'referrer_id': referrer.id,
                'referrer_name': referrer.name,
            }
            
        except Exception as e:
            logger.error(f"Error applying referral code: {str(e)}")
            self.db_session.rollback()
            raise
    
    def complete_referral(self, referral_id: str) -> Dict:
        """
        紹介を完了してコインを付与
        
        Args:
            referral_id: 紹介ID
            
        Returns:
            Dict: 完了情報
        """
        try:
            # 紹介を取得
            referral = self.db_session.query(Referral).filter_by(id=referral_id).first()
            if not referral:
                raise ValueError(f"Referral not found: {referral_id}")
            
            # 既に完了している場合はスキップ
            if referral.status == ReferralStatus.COMPLETED:
                return {'already_completed': True}
            
            # 紹介者を取得
            referrer = self.user_repo.find_by_id(referral.referrer_id)
            if not referrer:
                raise ValueError(f"Referrer not found: {referral.referrer_id}")
            
            # コインを付与
            coins_to_award = self.REFERRAL_BONUS_COINS
            old_balance = referrer.coins or 0
            new_balance = old_balance + coins_to_award
            referrer.coins = new_balance
            
            # 紹介ステータスを更新
            referral.status = ReferralStatus.COMPLETED
            referral.coins_awarded = coins_to_award
            referral.completed_at = datetime.utcnow()
            
            # コイン取引履歴を記録
            transaction = CoinTransaction(
                id=str(uuid.uuid4()),
                user_id=referrer.id,
                amount=coins_to_award,
                transaction_type='referral_bonus',
                description=f'紹介ボーナス（紹介ID: {referral_id}）',
                balance_after=new_balance,
                related_id=referral_id
            )
            self.db_session.add(transaction)
            
            self.db_session.commit()
            
            logger.info(f"Completed referral {referral_id}, awarded {coins_to_award} coins to user {referrer.id}")
            
            return {
                'referral_id': referral_id,
                'coins_awarded': coins_to_award,
                'new_balance': new_balance,
            }
            
        except Exception as e:
            logger.error(f"Error completing referral: {str(e)}")
            self.db_session.rollback()
            raise
    
    def get_user_referrals(self, user_id: str) -> List[Dict]:
        """
        ユーザーの紹介履歴を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            List[Dict]: 紹介履歴
        """
        try:
            referrals = self.db_session.query(Referral).filter_by(referrer_id=user_id).all()
            return [r.to_dict() for r in referrals]
        except Exception as e:
            logger.error(f"Error getting user referrals: {str(e)}")
            return []
    
    def get_user_coins(self, user_id: str) -> int:
        """
        ユーザーのコイン残高を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            int: コイン残高
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return 0
            return user.coins or 0
        except Exception as e:
            logger.error(f"Error getting user coins: {str(e)}")
            return 0
    
    def get_coin_transactions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        ユーザーのコイン取引履歴を取得
        
        Args:
            user_id: ユーザーID
            limit: 取得件数
            
        Returns:
            List[Dict]: 取引履歴
        """
        try:
            transactions = self.db_session.query(CoinTransaction)\
                .filter_by(user_id=user_id)\
                .order_by(CoinTransaction.created_at.desc())\
                .limit(limit)\
                .all()
            return [t.to_dict() for t in transactions]
        except Exception as e:
            logger.error(f"Error getting coin transactions: {str(e)}")
            return []
    
    def is_referred_user(self, user_id: str) -> bool:
        """
        ユーザーが紹介経由かチェック
        
        Args:
            user_id: ユーザーID
            
        Returns:
            bool: 紹介経由の場合True
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return False
            return user.referred_by is not None
        except Exception as e:
            logger.error(f"Error checking if user is referred: {str(e)}")
            return False
