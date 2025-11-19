"""
Xaman (旧XUMM) API Client
Xaman Walletとの連携を提供
"""
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class XamanClient:
    """
    Xaman API クライアント
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Xaman Client.
        
        Args:
            api_key: Xaman API Key
            api_secret: Xaman API Secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://xumm.app/api/v1/platform'
        self.headers = {
            'X-API-Key': api_key,
            'X-API-Secret': api_secret,
            'Content-Type': 'application/json',
        }
    
    def create_signin_payload(self) -> Dict:
        """
        サインインペイロードを作成
        
        Returns:
            Dict: ペイロード情報
        """
        try:
            payload = {
                'txjson': {
                    'TransactionType': 'SignIn',
                },
                'options': {
                    'submit': False,
                    'expire': 5,  # 5分
                },
            }
            
            response = requests.post(
                f'{self.base_url}/payload',
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Created signin payload: {data.get('uuid')}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to create signin payload: {str(e)}")
            raise Exception(f"Xaman API error: {str(e)}")
    
    def create_payment_payload(
        self,
        destination: str,
        amount_drops: str,
        memo: Optional[str] = None
    ) -> Dict:
        """
        支払いペイロードを作成
        
        Args:
            destination: 送金先アドレス
            amount_drops: 送金額（drops）
            memo: メモ（オプション）
            
        Returns:
            Dict: ペイロード情報
        """
        try:
            txjson = {
                'TransactionType': 'Payment',
                'Destination': destination,
                'Amount': amount_drops,
            }
            
            if memo:
                txjson['Memos'] = [
                    {
                        'Memo': {
                            'MemoType': self._string_to_hex('order_id'),
                            'MemoData': self._string_to_hex(memo),
                        }
                    }
                ]
            
            payload = {
                'txjson': txjson,
                'options': {
                    'submit': True,
                    'expire': 5,  # 5分
                },
            }
            
            response = requests.post(
                f'{self.base_url}/payload',
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Created payment payload: {data.get('uuid')}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to create payment payload: {str(e)}")
            raise Exception(f"Xaman API error: {str(e)}")
    
    def get_payload_status(self, uuid: str) -> Dict:
        """
        ペイロードのステータスを取得
        
        Args:
            uuid: ペイロードUUID
            
        Returns:
            Dict: ペイロード情報
        """
        try:
            response = requests.get(
                f'{self.base_url}/payload/{uuid}',
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to get payload status: {str(e)}")
            raise Exception(f"Xaman API error: {str(e)}")
    
    def _string_to_hex(self, text: str) -> str:
        """
        文字列を16進数に変換
        
        Args:
            text: 変換する文字列
            
        Returns:
            str: 16進数文字列
        """
        return text.encode('utf-8').hex().upper()
