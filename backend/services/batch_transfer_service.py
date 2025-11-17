"""
Batch Transfer Service
XRPLのBatch Transactions機能を使った一括送金サービス
"""
import logging
from typing import Dict, List
from datetime import datetime
from clients.xrpl_client import XRPLClient
from database.connection import get_db_connection

logger = logging.getLogger(__name__)


class BatchTransferService:
    """バッチ送金サービス"""
    
    def __init__(self, xrpl_client: XRPLClient):
        self.xrpl_client = xrpl_client
    
    def send_batch_rewards(
        self,
        sender_wallet_seed: str,
        user_ids: List[int],
        amount_xrp: float,
        reason: str = "Batch reward"
    ) -> Dict:
        """
        複数のユーザーに一括でXRP報酬を送信
        
        Args:
            sender_wallet_seed: 送信者のウォレットシード
            user_ids: ユーザーIDリスト
            amount_xrp: 各ユーザーへの送信量
            reason: 送信理由
            
        Returns:
            Dict: 送信結果
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # ユーザーのウォレットアドレスを取得
            placeholders = ','.join(['%s'] * len(user_ids))
            query = f"""
                SELECT id, wallet_address, email
                FROM users
                WHERE id IN ({placeholders})
                AND wallet_address IS NOT NULL
            """
            cursor.execute(query, user_ids)
            users = cursor.fetchall()
            
            if not users:
                raise Exception("No valid users found with wallet addresses")
            
            logger.info(f"Found {len(users)} users with wallet addresses")
            
            # 受取人リストを作成
            recipients = [
                {
                    'address': user['wallet_address'],
                    'amount_xrp': amount_xrp,
                    'user_id': user['id']
                }
                for user in users
            ]
            
            # バッチ送信実行
            result = self.xrpl_client.batch_send_xrp(
                sender_wallet_seed=sender_wallet_seed,
                recipients=recipients,
                memo=reason
            )
            
            # データベースに記録
            for transaction in result['transactions']:
                try:
                    # ユーザーIDを取得
                    user_id = next(
                        (r['user_id'] for r in recipients if r['address'] == transaction['recipient']),
                        None
                    )
                    
                    if user_id:
                        # トランザクション履歴を記録
                        insert_query = """
                            INSERT INTO batch_transfers
                            (user_id, wallet_address, amount_xrp, transaction_hash, 
                             ticket_sequence, reason, status, created_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_query, (
                            user_id,
                            transaction['recipient'],
                            transaction['amount_xrp'],
                            transaction['transaction_hash'],
                            transaction.get('ticket_sequence'),
                            reason,
                            'success',
                            datetime.now()
                        ))
                except Exception as e:
                    logger.error(f"Failed to record transaction: {str(e)}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return result
            
        except Exception as e:
            logger.error(f"Batch reward transfer failed: {str(e)}")
            raise Exception(f"Batch reward transfer failed: {str(e)}")
    
    def send_batch_to_vip_users(
        self,
        sender_wallet_seed: str,
        min_importance_level: str,
        amount_xrp: float,
        reason: str = "VIP reward"
    ) -> Dict:
        """
        VIPユーザーに一括でXRP報酬を送信
        
        Args:
            sender_wallet_seed: 送信者のウォレットシード
            min_importance_level: 最小重要度レベル（Bronze, Silver, Gold, Platinum, Diamond）
            amount_xrp: 各ユーザーへの送信量
            reason: 送信理由
            
        Returns:
            Dict: 送信結果
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # レベル順序
            level_order = {
                'Bronze': 1,
                'Silver': 2,
                'Gold': 3,
                'Platinum': 4,
                'Diamond': 5
            }
            
            min_level_value = level_order.get(min_importance_level, 1)
            
            # 指定レベル以上のユーザーを取得
            query = """
                SELECT u.id, u.wallet_address, u.email, u.importance_level
                FROM users u
                WHERE u.wallet_address IS NOT NULL
                AND u.importance_level IN ('Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond')
                ORDER BY u.importance_score DESC
            """
            cursor.execute(query)
            all_users = cursor.fetchall()
            
            # レベルでフィルタリング
            users = [
                user for user in all_users
                if level_order.get(user['importance_level'], 0) >= min_level_value
            ]
            
            if not users:
                raise Exception(f"No VIP users found with level >= {min_importance_level}")
            
            logger.info(f"Found {len(users)} VIP users (>= {min_importance_level})")
            
            # ユーザーIDリストを作成
            user_ids = [user['id'] for user in users]
            
            cursor.close()
            conn.close()
            
            # バッチ送信実行
            return self.send_batch_rewards(
                sender_wallet_seed=sender_wallet_seed,
                user_ids=user_ids,
                amount_xrp=amount_xrp,
                reason=reason
            )
            
        except Exception as e:
            logger.error(f"VIP batch transfer failed: {str(e)}")
            raise Exception(f"VIP batch transfer failed: {str(e)}")
    
    def send_batch_to_top_referrers(
        self,
        sender_wallet_seed: str,
        top_n: int,
        amount_xrp: float,
        reason: str = "Top referrer reward"
    ) -> Dict:
        """
        トップ紹介者に一括でXRP報酬を送信
        
        Args:
            sender_wallet_seed: 送信者のウォレットシード
            top_n: 上位N人
            amount_xrp: 各ユーザーへの送信量
            reason: 送信理由
            
        Returns:
            Dict: 送信結果
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # トップ紹介者を取得
            query = """
                SELECT u.id, u.wallet_address, u.email, COUNT(r.id) as referral_count
                FROM users u
                LEFT JOIN referrals r ON u.id = r.referrer_id
                WHERE u.wallet_address IS NOT NULL
                GROUP BY u.id
                HAVING referral_count > 0
                ORDER BY referral_count DESC
                LIMIT %s
            """
            cursor.execute(query, (top_n,))
            users = cursor.fetchall()
            
            if not users:
                raise Exception("No top referrers found")
            
            logger.info(f"Found {len(users)} top referrers")
            
            # ユーザーIDリストを作成
            user_ids = [user['id'] for user in users]
            
            cursor.close()
            conn.close()
            
            # バッチ送信実行
            return self.send_batch_rewards(
                sender_wallet_seed=sender_wallet_seed,
                user_ids=user_ids,
                amount_xrp=amount_xrp,
                reason=reason
            )
            
        except Exception as e:
            logger.error(f"Top referrer batch transfer failed: {str(e)}")
            raise Exception(f"Top referrer batch transfer failed: {str(e)}")
    
    def get_batch_transfer_history(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        バッチ送信履歴を取得
        
        Args:
            limit: 取得件数
            offset: オフセット
            
        Returns:
            Dict: 送信履歴
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # 履歴取得
            query = """
                SELECT 
                    bt.*,
                    u.email,
                    u.importance_level
                FROM batch_transfers bt
                LEFT JOIN users u ON bt.user_id = u.id
                ORDER BY bt.created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (limit, offset))
            transfers = cursor.fetchall()
            
            # 総件数取得
            cursor.execute("SELECT COUNT(*) as total FROM batch_transfers")
            total = cursor.fetchone()['total']
            
            cursor.close()
            conn.close()
            
            return {
                'transfers': transfers,
                'total': total,
                'limit': limit,
                'offset': offset
            }
            
        except Exception as e:
            logger.error(f"Failed to get batch transfer history: {str(e)}")
            raise Exception(f"Failed to get batch transfer history: {str(e)}")
