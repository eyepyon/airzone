"""
Wallet Blueprint for wallet connection and management.
Handles Xaman Wallet connection and external wallet linking.
"""
from flask import Blueprint, request, jsonify, g
from middleware.auth import jwt_required, get_current_user
from services.wallet_service import WalletService
from clients.xrpl_client import XRPLClient
import logging

logger = logging.getLogger(__name__)

wallet_blueprint = Blueprint('wallet', __name__)


@wallet_blueprint.route('/xaman/signin', methods=['POST'])
@jwt_required
def xaman_signin():
    """
    Create Xaman sign-in request.
    
    Request Body:
        {
            "network": "testnet"
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "uuid": "xxx-xxx-xxx",
                "qr_code": "https://...",
                "deep_link": "xaman://...",
                "websocket": "wss://..."
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        data = request.get_json() or {}
        network = data.get('network', 'testnet')
        
        # Xaman APIでサインインペイロードを作成
        from config import Config
        
        # Xaman API設定を確認
        xaman_api_key = getattr(Config, 'XAMAN_API_KEY', None)
        xaman_api_secret = getattr(Config, 'XAMAN_API_SECRET', None)
        
        if xaman_api_key and xaman_api_secret:
            # 実際のXaman APIを使用
            from clients.xaman_client import XamanClient
            
            xaman_client = XamanClient(xaman_api_key, xaman_api_secret)
            payload = xaman_client.create_signin_payload()
            
            return jsonify({
                'status': 'success',
                'data': {
                    'uuid': payload['uuid'],
                    'qr_code': payload['refs']['qr_png'],
                    'deep_link': payload['next']['always'],
                    'websocket': payload['refs']['websocket_status'],
                }
            }), 200
        else:
            # フォールバック: 簡易版（開発用）
            logger.warning("Xaman API credentials not configured, using fallback")
            
            import uuid as uuid_lib
            request_uuid = str(uuid_lib.uuid4())
            
            # QRコード生成（簡易版）
            qr_data = f"xaman://signin?uuid={request_uuid}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_data}"
            
            return jsonify({
                'status': 'success',
                'data': {
                    'uuid': request_uuid,
                    'qr_code': qr_url,
                    'deep_link': qr_data,
                    'websocket': f"wss://xumm.app/sign/{request_uuid}",
                    'message': 'Xamanアプリで署名してください（開発モード）'
                }
            }), 200
        
    except Exception as e:
        logger.error(f"Error creating Xaman sign-in request: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to create sign-in request',
            'code': 500
        }), 500


@wallet_blueprint.route('/walletconnect/session', methods=['POST'])
@jwt_required
def create_walletconnect_session():
    """
    Create WalletConnect session.
    
    Response:
        {
            "status": "success",
            "data": {
                "uri": "wc:...",
                "qrCode": "https://..."
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # WalletConnectセッションを作成（簡易版）
        import uuid as uuid_lib
        session_id = str(uuid_lib.uuid4())
        
        # WalletConnect URI（簡易版）
        uri = f"wc:{session_id}@2?relay-protocol=irn&symKey=..."
        
        # QRコード生成
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={uri}"
        
        # セッション情報を一時保存（実際にはRedisなどを使用）
        # ここでは簡易的にメモリに保存
        
        logger.info(f"Created WalletConnect session for user {user_id}: {session_id}")
        
        return jsonify({
            'status': 'success',
            'data': {
                'session_id': session_id,
                'uri': uri,
                'qrCode': qr_url,
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error creating WalletConnect session: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to create WalletConnect session',
            'code': 500
        }), 500


@wallet_blueprint.route('/walletconnect/status', methods=['GET'])
@jwt_required
def get_walletconnect_status():
    """
    Get WalletConnect connection status.
    
    Response:
        {
            "status": "success",
            "data": {
                "connected": true,
                "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "network": "testnet"
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # セッションステータスを確認（簡易版）
        # 実際にはRedisやデータベースから取得
        
        # ここでは既存のウォレット情報を返す
        from repositories.wallet_repository import WalletRepository
        wallet_repo = WalletRepository(g.db)
        wallet = wallet_repo.find_by_user_id(user_id)
        
        if wallet and wallet.address:
            return jsonify({
                'status': 'success',
                'data': {
                    'connected': True,
                    'address': wallet.address,
                    'network': 'testnet',
                }
            }), 200
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'connected': False,
                    'address': None,
                    'network': None,
                }
            }), 200
        
    except Exception as e:
        logger.error(f"Error getting WalletConnect status: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get WalletConnect status',
            'code': 500
        }), 500


@wallet_blueprint.route('/connect', methods=['POST'])
@jwt_required
def connect_wallet():
    """
    Connect external wallet (Xaman) to user account.
    
    Request Body:
        {
            "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "wallet_type": "xaman"
        }
    
    Response:
        {
            "status": "success",
            "data": {
                "wallet": {
                    "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "wallet_type": "xaman",
                    "connected": true
                }
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
        
        address = data.get('address')
        wallet_type = data.get('wallet_type', 'xaman')
        
        if not address:
            return jsonify({
                'status': 'error',
                'error': 'address is required',
                'code': 400
            }), 400
        
        # Validate XRPL address format
        if not address.startswith('r') or len(address) < 25:
            return jsonify({
                'status': 'error',
                'error': 'Invalid XRPL address format',
                'code': 400
            }), 400
        
        # Get wallet service
        from config import Config
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        wallet_service = WalletService(
            db_session=g.db,
            xrpl_client=xrpl_client,
            encryption_key=Config.ENCRYPTION_KEY
        )
        
        # Check if user already has a wallet
        existing_wallet = wallet_service.get_user_wallet(user_id)
        
        if existing_wallet:
            # Update existing wallet address
            from repositories.wallet_repository import WalletRepository
            wallet_repo = WalletRepository(g.db)
            wallet = wallet_repo.find_by_user_id(user_id)
            
            # Update address (keep encrypted seed as backup)
            wallet.address = address
            g.db.commit()
            
            logger.info(f"Updated wallet address for user {user_id}: {address}")
        else:
            # Create new wallet record with external address
            # Note: We don't have the private key for external wallets
            from repositories.wallet_repository import WalletRepository
            wallet_repo = WalletRepository(g.db)
            wallet = wallet_repo.create_wallet(
                user_id=user_id,
                address=address,
                private_key_encrypted=''  # External wallet, no private key
            )
            g.db.commit()
            
            logger.info(f"Connected external wallet for user {user_id}: {address}")
        
        return jsonify({
            'status': 'success',
            'data': {
                'wallet': {
                    'address': address,
                    'wallet_type': wallet_type,
                    'connected': True
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error connecting wallet: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to connect wallet',
            'code': 500
        }), 500


@wallet_blueprint.route('/disconnect', methods=['POST'])
@jwt_required
def disconnect_wallet():
    """
    Disconnect external wallet from user account.
    
    Response:
        {
            "status": "success",
            "data": {
                "message": "Wallet disconnected successfully"
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Get wallet service
        from config import Config
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        wallet_service = WalletService(
            db_session=g.db,
            xrpl_client=xrpl_client,
            encryption_key=Config.ENCRYPTION_KEY
        )
        
        # Generate new auto-managed wallet
        wallet = wallet_service.create_wallet(user_id)
        
        logger.info(f"Disconnected external wallet for user {user_id}, created new auto-managed wallet")
        
        return jsonify({
            'status': 'success',
            'data': {
                'message': 'Wallet disconnected successfully',
                'wallet': wallet
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error disconnecting wallet: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to disconnect wallet',
            'code': 500
        }), 500


@wallet_blueprint.route('/balance', methods=['GET'])
@jwt_required
def get_wallet_balance():
    """
    Get wallet balance for current user.
    
    Response:
        {
            "status": "success",
            "data": {
                "balance_drops": 1000000,
                "balance_xrp": 1.0,
                "address": "rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            }
        }
    """
    try:
        current_user = get_current_user()
        user_id = current_user['user_id']
        
        # Get wallet service
        from config import Config
        xrpl_client = XRPLClient(
            network=Config.XRPL_NETWORK,
            sponsor_seed=Config.XRPL_SPONSOR_SEED
        )
        wallet_service = WalletService(
            db_session=g.db,
            xrpl_client=xrpl_client,
            encryption_key=Config.ENCRYPTION_KEY
        )
        
        # Get wallet
        wallet = wallet_service.get_user_wallet(user_id)
        if not wallet:
            return jsonify({
                'status': 'error',
                'error': 'Wallet not found',
                'code': 404
            }), 404
        
        # Get balance
        balance_drops = wallet_service.get_wallet_balance(user_id)
        balance_xrp = balance_drops / 1_000_000
        
        return jsonify({
            'status': 'success',
            'data': {
                'balance_drops': balance_drops,
                'balance_xrp': balance_xrp,
                'address': wallet['address']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting wallet balance: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Failed to get wallet balance',
            'code': 500
        }), 500
