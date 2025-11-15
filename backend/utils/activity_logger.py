"""
ユーザーアクティビティロガー
DAU/MAU/DL数などの効果測定のためのアクティビティを記録
"""
import mysql.connector
from datetime import datetime
from typing import Optional, Dict, Any
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ActivityLogger:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'airzone'),
        }
    
    def log_activity(
        self,
        user_id: str,
        activity_type: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        ユーザーアクティビティを記録
        
        Args:
            user_id: ユーザーID
            activity_type: アクティビティタイプ (login, download, purchase, etc.)
            ip_address: IPアドレス
            user_agent: ユーザーエージェント
            metadata: 追加のメタデータ
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = """
                INSERT INTO user_activities 
                (user_id, activity_type, ip_address, user_agent, metadata, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute(query, (
                user_id,
                activity_type,
                ip_address,
                user_agent,
                metadata_json,
                datetime.now()
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error logging activity: {e}")
    
    def log_login(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """ログインアクティビティを記録"""
        self.log_activity(user_id, 'login', ip_address, user_agent)
    
    def log_download(
        self,
        user_id: str,
        product_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """ダウンロードアクティビティを記録"""
        metadata = {'product_id': product_id} if product_id else None
        self.log_activity(user_id, 'download', ip_address, user_agent, metadata)
    
    def log_purchase(
        self,
        user_id: str,
        order_id: str,
        amount: float,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """購入アクティビティを記録"""
        metadata = {'order_id': order_id, 'amount': amount}
        self.log_activity(user_id, 'purchase', ip_address, user_agent, metadata)

# シングルトンインスタンス
activity_logger = ActivityLogger()
