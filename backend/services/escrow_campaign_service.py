"""
Escrow Campaign Service for XRP staking campaigns.
"""
from typing import Dict, Optional, List
import logging
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from clients.xrpl_client import XRPLClient
import time

logger = logging.getLogger(__name__)


class EscrowCampaignService:
    """Service for managing XRP escrow staking campaigns."""
    
    def __init__(self, db_session: Session, xrpl_client: XRPLClient):
        """Initialize EscrowCampaignService."""
        self.db_session = db_session
        self.xrpl_client = xrpl_client
        self.user_repo = UserRepository(db_session)
    
    def create_campaign_escrow(
        self,
        user_id: str,
        campaign_id: str,
        amount_xrp: float,
        lock_days: int
    ) -> Dict:
        """
        キャンペーン用のEscrowを作成
        
        Args:
            user_id: ユーザーID
            campaign_id: キャンペーンID
            amount_xrp: ロックするXRP量
            lock_days: ロック日数
            
        Returns:
            Dict: Escrow情報
        """
        try:
            # ユーザーのウォレットを取得
            from repositories.wallet_repository import WalletRepository
            wallet_repo = WalletRepository(self.db_session)
            wallet = wallet_repo.find_by_user_id(user_id)
            
            if not wallet:
                raise ValueError(f"User {user_id} has no wallet")
            
            # ウォレットシードを復号化
            from services.wallet_service import WalletService
            from config import Config
            wallet_service = WalletService(
                self.db_session,
                self.xrpl_client,
                Config.ENCRYPTION_KEY
            )
            wallet_seed = wallet_service.get_decrypted_seed(user_id)
            
            # ロック期間を計算
            finish_after = int(time.time()) + (lock_days * 24 * 60 * 60)
            amount_drops = int(amount_xrp * 1_000_000)
            
            # Escrowを作成（自分自身に送る）
            result = self.xrpl_client.create_escrow(
                sender_wallet_seed=wallet_seed,
                recipient_address=wallet.address,
                amount_drops=amount_drops,
                finish_after=finish_after
            )
            
            # データベースに記録
            escrow_id = str(uuid.uuid4())
            self.db_session.execute(
                """
                INSERT INTO escrow_stakes 
                (id, user_id, campaign_id, wallet_address, amount_drops, 
                 lock_days, finish_after, escrow_sequence, transaction_hash, 
                 status, created_at)
                VALUES (:id, :user_id, :campaign_id, :wallet, :amount, 
                        :days, :finish, :sequence, :tx_hash, :status, :created)
                """,
                {
                    'id': escrow_id,
                    'user_id': user_id,
                    'campaign_id': campaign_id,
                    'wallet': wallet.address,
                    'amount': amount_drops,
                    'days': lock_days,
                    'finish': datetime.fromtimestamp(finish_after),
                    'sequence': result['escrow_sequence'],
                    'tx_hash': result['transaction_hash'],
                    'status': 'active',
                    'created': datetime.utcnow()
                }
            )
            
            self.db_session.commit()
            
            logger.info(f"Created escrow stake for user {user_id}: {amount_xrp} XRP for {lock_days} days")
            
            return {
                'escrow_id': escrow_id,
                'amount_xrp': amount_xrp,
                'lock_days': lock_days,
                'finish_after': finish_after,
                'transaction_hash': result['transaction_hash'],
            }
            
        except Exception as e:
            logger.error(f"Error creating campaign escrow: {str(e)}")
            self.db_session.rollback()
            raise
    
    def check_and_complete_escrows(self) -> Dict:
        """
        完了可能なEscrowをチェックして完了処理
        
        Returns:
            Dict: 処理結果
        """
        try:
            # 完了可能なEscrowを取得
            now = datetime.utcnow()
            
            escrows = self.db_session.execute(
                """
                SELECT * FROM escrow_stakes 
                WHERE status = 'active' 
                AND finish_after <= :now
                """,
                {'now': now}
            ).fetchall()
            
            completed_count = 0
            errors = []
            
            for escrow in escrows:
                try:
                    # Escrowを完了
                    # 注: 実際には受取人が実行する必要がある
                    # ここではスポンサーウォレットで代行
                    
                    # ステータスを更新
                    self.db_session.execute(
                        """
                        UPDATE escrow_stakes 
                        SET status = 'completed', completed_at = :completed
                        WHERE id = :id
                        """,
                        {'id': escrow['id'], 'completed': datetime.utcnow()}
                    )
                    
                    # NFTを発行
                    self._award_campaign_nft(escrow['user_id'], escrow['campaign_id'])
                    
                    completed_count += 1
                    
                except Exception as e:
                    errors.append({'escrow_id': escrow['id'], 'error': str(e)})
            
            self.db_session.commit()
            
            return {
                'total_checked': len(escrows),
                'completed_count': completed_count,
                'error_count': len(errors),
                'errors': errors,
            }
            
        except Exception as e:
            logger.error(f"Error checking escrows: {str(e)}")
            self.db_session.rollback()
            raise
    
    def get_user_escrows(self, user_id: str) -> List[Dict]:
        """
        ユーザーのEscrow一覧を取得
        
        Args:
            user_id: ユーザーID
            
        Returns:
            List[Dict]: Escrow一覧
        """
        try:
            escrows = self.db_session.execute(
                """
                SELECT es.*, ec.name as campaign_name, ec.nft_reward_name
                FROM escrow_stakes es
                LEFT JOIN escrow_campaigns ec ON es.campaign_id = ec.id
                WHERE es.user_id = :user_id
                ORDER BY es.created_at DESC
                """,
                {'user_id': user_id}
            ).fetchall()
            
            return [
                {
                    'id': e['id'],
                    'campaign_id': e['campaign_id'],
                    'campaign_name': e['campaign_name'],
                    'amount_drops': e['amount_drops'],
                    'lock_days': e['lock_days'],
                    'finish_after': e['finish_after'].isoformat(),
                    'status': e['status'],
                    'nft_reward': e['nft_reward_name'],
                    'transaction_hash': e['transaction_hash'],
                    'escrow_sequence': e['escrow_sequence'],
                    'created_at': e['created_at'].isoformat(),
                }
                for e in escrows
            ]
            
        except Exception as e:
            logger.error(f"Error getting user escrows: {str(e)}")
            return []
    
    def _award_campaign_nft(self, user_id: str, campaign_id: str):
        """
        キャンペーンNFTを付与
        
        Args:
            user_id: ユーザーID
            campaign_id: キャンペーンID
        """
        try:
            # キャンペーン情報を取得
            campaign = self.db_session.execute(
                "SELECT * FROM escrow_campaigns WHERE id = :id",
                {'id': campaign_id}
            ).fetchone()
            
            if not campaign:
                raise ValueError(f"Campaign not found: {campaign_id}")
            
            # NFT発行タスクを作成
            from services.nft_service import NFTService
            from tasks.task_manager import TaskManager
            
            task_manager = TaskManager(self.db_session)
            nft_service = NFTService(
                self.db_session,
                self.xrpl_client,
                task_manager
            )
            
            nft_service.mint_nft(
                user_id=user_id,
                nft_name=campaign['nft_reward_name'],
                nft_description=campaign['nft_reward_description'],
                nft_image_url=campaign['nft_reward_image_url'],
                metadata={'campaign_id': campaign_id, 'type': 'escrow_reward'}
            )
            
            logger.info(f"Awarded campaign NFT to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error awarding campaign NFT: {str(e)}")
            raise
