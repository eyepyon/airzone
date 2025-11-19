"""
XRPL Payment Service for managing XRP Ledger payments.
Handles payment creation, execution, and verification on XRPL blockchain.

Requirements: 5.5, 8.2, 8.6, 8.7
"""
import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session
from repositories.order_repository import OrderRepository
from repositories.wallet_repository import WalletRepository
from clients.xrpl_client import XRPLClient
from services.wallet_service import WalletService
from exceptions import ResourceNotFoundError, ValidationError
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class XRPLPaymentService:
    """
    Service for XRPL payment operations.
    Handles payment creation, execution, and verification on XRP Ledger.
    """
    
    def __init__(self, db_session: Session, xrpl_client: XRPLClient):
        """
        Initialize XRPLPaymentService.
        
        Args:
            db_session: SQLAlchemy database session
            xrpl_client: XRPL blockchain client
        """
        self.db_session = db_session
        self.xrpl_client = xrpl_client
        self.order_repo = OrderRepository(db_session)
        self.wallet_repo = WalletRepository(db_session)
    
    def create_payment_request(
        self,
        user_id: str,
        order_id: str,
        amount_xrp: float,
        destination: str
    ) -> Dict:
        """
        Create an XRPL payment request.
        
        Args:
            user_id: User's unique identifier
            order_id: Order UUID
            amount_xrp: Amount in XRP
            destination: Destination XRPL address
            
        Returns:
            Dict: Payment request details with QR code and payment URL
            
        Raises:
            ResourceNotFoundError: If order or wallet not found
            ValidationError: If validation fails
        """
        try:
            # Verify order exists and belongs to user
            order = self.order_repo.find_by_id(order_id)
            if not order:
                raise ResourceNotFoundError("Order", order_id)
            
            if order.user_id != user_id:
                raise ValidationError("Order does not belong to user")
            
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                raise ResourceNotFoundError("Wallet", f"user_id={user_id}")
            
            # Check wallet balance
            balance_drops = self.xrpl_client.get_wallet_balance(wallet.address)
            balance_xrp = balance_drops / 1_000_000
            
            if balance_xrp < amount_xrp:
                raise ValidationError(
                    f"Insufficient balance. Required: {amount_xrp} XRP, Available: {balance_xrp} XRP"
                )
            
            # Generate payment request ID
            payment_request_id = str(uuid.uuid4())
            
            # Create payment URL (for Xaman wallet)
            # Format: xrpl:{destination}?amount={amount}&dt={memo}
            memo = f"order:{order_id}"
            payment_url = f"xrpl:{destination}?amount={amount_xrp}&dt={memo}"
            
            # Generate QR code URL (using a QR code service)
            qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={payment_url}"
            
            logger.info(
                f"Created XRPL payment request",
                extra={
                    'user_id': user_id,
                    'order_id': order_id,
                    'amount_xrp': amount_xrp,
                    'wallet_address': wallet.address,
                    'destination': destination
                }
            )
            
            return {
                'payment_request_id': payment_request_id,
                'order_id': order_id,
                'amount_xrp': amount_xrp,
                'destination': destination,
                'source_address': wallet.address,
                'payment_url': payment_url,
                'qr_code': qr_code_url,
                'balance_xrp': balance_xrp,
                'network': self.xrpl_client.network,
                'created_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to create XRPL payment request: {str(e)}")
            raise
    
    def execute_payment(
        self,
        user_id: str,
        order_id: str
    ) -> Dict:
        """
        Execute XRPL payment from user's wallet.
        
        Args:
            user_id: User's unique identifier
            order_id: Order UUID
            
        Returns:
            Dict: Payment execution result with transaction hash
            
        Raises:
            ResourceNotFoundError: If order or wallet not found
            ValidationError: If validation fails
        """
        try:
            # Verify order exists and belongs to user
            order = self.order_repo.find_by_id(order_id)
            if not order:
                raise ResourceNotFoundError("Order", order_id)
            
            if order.user_id != user_id:
                raise ValidationError("Order does not belong to user")
            
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                raise ResourceNotFoundError("Wallet", f"user_id={user_id}")
            
            # Get wallet seed (decrypted)
            from services.wallet_service import WalletService
            from config import config
            wallet_service = WalletService(
                self.db_session,
                self.xrpl_client,
                config['development'].ENCRYPTION_KEY
            )
            wallet_seed = wallet_service.get_decrypted_seed(user_id)
            
            # Calculate amount in XRP
            # Assuming order.total_amount is in JPY
            xrp_jpy_rate = 150  # TODO: Get from API
            amount_xrp = order.total_amount / xrp_jpy_rate
            
            # Get destination address (sponsor address)
            from config import config
            destination = config['development'].XRPL_SPONSOR_ADDRESS
            
            # Execute payment on XRPL
            memo = f"order:{order_id}"
            result = self.xrpl_client.send_xrp(
                sender_wallet_seed=wallet_seed,
                recipient_address=destination,
                amount_xrp=amount_xrp,
                memo=memo
            )
            
            # Update order status
            order.status = 'completed'
            order.payment_method = 'xrpl'
            order.payment_status = 'completed'
            self.db_session.commit()
            
            logger.info(
                f"XRPL payment executed successfully",
                extra={
                    'user_id': user_id,
                    'order_id': order_id,
                    'transaction_hash': result['transaction_hash'],
                    'amount_xrp': amount_xrp
                }
            )
            
            return {
                'success': True,
                'order_id': order_id,
                'transaction_hash': result['transaction_hash'],
                'amount_xrp': result['amount_xrp'],
                'sender': result['sender'],
                'recipient': result['recipient'],
                'network': self.xrpl_client.network,
                'explorer_url': self._get_explorer_url(result['transaction_hash']),
                'completed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to execute XRPL payment: {str(e)}")
            self.db_session.rollback()
            raise
    
    def check_payment_status(
        self,
        user_id: str,
        order_id: str
    ) -> Dict:
        """
        Check XRPL payment status for an order.
        
        Args:
            user_id: User's unique identifier
            order_id: Order UUID
            
        Returns:
            Dict: Payment status
            
        Raises:
            ResourceNotFoundError: If order not found
        """
        try:
            # Verify order exists and belongs to user
            order = self.order_repo.find_by_id(order_id)
            if not order:
                raise ResourceNotFoundError("Order", order_id)
            
            if order.user_id != user_id:
                raise ValidationError("Order does not belong to user")
            
            # Check if payment is completed
            status = 'pending'
            if order.payment_status == 'completed':
                status = 'completed'
            elif order.payment_status == 'failed':
                status = 'failed'
            
            return {
                'order_id': order_id,
                'status': status,
                'payment_method': order.payment_method,
                'payment_status': order.payment_status,
                'total_amount': order.total_amount,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            }
            
        except Exception as e:
            logger.error(f"Failed to check XRPL payment status: {str(e)}")
            raise
    
    def verify_transaction(self, transaction_hash: str) -> Dict:
        """
        Verify XRPL transaction on blockchain.
        
        Args:
            transaction_hash: XRPL transaction hash
            
        Returns:
            Dict: Transaction details from blockchain
            
        Raises:
            ResourceNotFoundError: If transaction not found
        """
        try:
            # Get transaction details from XRPL
            from xrpl.models.requests import Tx
            
            tx_request = Tx(transaction=transaction_hash)
            response = self.xrpl_client.client.request(tx_request)
            
            if not response.is_successful():
                raise ResourceNotFoundError("Transaction", transaction_hash)
            
            tx_data = response.result
            
            # Extract relevant information
            transaction = {
                'hash': tx_data.get('hash'),
                'ledger_index': tx_data.get('ledger_index'),
                'date': tx_data.get('date'),
                'account': tx_data.get('Account'),
                'destination': tx_data.get('Destination'),
                'amount': tx_data.get('Amount'),
                'fee': tx_data.get('Fee'),
                'validated': tx_data.get('validated', False),
                'meta': tx_data.get('meta', {}),
                'explorer_url': self._get_explorer_url(transaction_hash)
            }
            
            logger.info(
                f"Verified XRPL transaction",
                extra={
                    'transaction_hash': transaction_hash,
                    'validated': transaction['validated']
                }
            )
            
            return transaction
            
        except Exception as e:
            logger.error(f"Failed to verify XRPL transaction: {str(e)}")
            raise
    
    def _get_explorer_url(self, transaction_hash: str) -> str:
        """
        Get XRPL explorer URL for a transaction.
        
        Args:
            transaction_hash: XRPL transaction hash
            
        Returns:
            str: Explorer URL
        """
        if self.xrpl_client.network == 'mainnet':
            return f"https://livenet.xrpl.org/transactions/{transaction_hash}"
        else:
            return f"https://testnet.xrpl.org/transactions/{transaction_hash}"
