"""
NFT Service for managing NFT minting and ownership verification.
Handles NFT minting task queuing, ownership verification, and NFT retrieval.

Requirements: 3.1, 3.2, 3.4, 3.5
"""
from typing import List, Dict, Optional
import logging
from sqlalchemy.orm import Session
from repositories.nft_repository import NFTRepository
from repositories.wallet_repository import WalletRepository
from repositories.user_repository import UserRepository
from clients.sui_client import SuiClient
from tasks.task_manager import TaskManager
from models.nft_mint import NFTMintStatus


logger = logging.getLogger(__name__)


class NFTService:
    """
    Service for NFT operations.
    Handles NFT minting, ownership verification, and NFT retrieval.
    """
    
    def __init__(
        self,
        db_session: Session,
        sui_client: SuiClient,
        task_manager: TaskManager
    ):
        """
        Initialize NFTService.
        
        Args:
            db_session: SQLAlchemy database session
            sui_client: Sui blockchain client
            task_manager: Task manager for async operations
        """
        self.db_session = db_session
        self.nft_repo = NFTRepository(db_session)
        self.wallet_repo = WalletRepository(db_session)
        self.user_repo = UserRepository(db_session)
        self.sui_client = sui_client
        self.task_manager = task_manager
    
    def mint_nft(
        self,
        user_id: str,
        nft_name: str,
        nft_description: str,
        nft_image_url: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Queue NFT minting task for a user.
        Creates a pending NFT mint record and submits async task.
        
        Args:
            user_id: User's unique identifier
            nft_name: Name of the NFT
            nft_description: Description of the NFT
            nft_image_url: URL of the NFT image
            metadata: Additional metadata for the NFT
            
        Returns:
            str: Task ID for tracking mint status
            
        Raises:
            ValueError: If user not found or has no wallet
            
        Requirements:
            - 3.1: NFT minting task queuing
            - 3.2: NFT minting via Move smart contract
        """
        try:
            # Verify user exists
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                raise ValueError(f"User {user_id} has no wallet")
            
            # Prepare NFT metadata
            nft_metadata = {
                'name': nft_name,
                'description': nft_description,
                'image_url': nft_image_url
            }
            if metadata:
                nft_metadata.update(metadata)
            
            # Create pending NFT mint record
            nft_mint = self.nft_repo.create(
                user_id=user_id,
                wallet_address=wallet.address,
                status=NFTMintStatus.PENDING,
                nft_metadata=nft_metadata
            )
            self.db_session.commit()
            
            logger.info(f"Created NFT mint record: {nft_mint.id} for user: {user_id}")
            
            # Submit minting task to task manager
            task_id = self.task_manager.submit_task(
                task_type='nft_mint',
                func=self._execute_nft_mint,
                nft_mint_id=nft_mint.id,
                wallet_address=wallet.address,
                nft_name=nft_name,
                nft_description=nft_description,
                nft_image_url=nft_image_url,
                metadata=metadata,
                payload={
                    'nft_mint_id': nft_mint.id,
                    'user_id': user_id,
                    'wallet_address': wallet.address,
                    'nft_metadata': nft_metadata
                }
            )
            
            logger.info(f"Submitted NFT mint task: {task_id} for NFT: {nft_mint.id}")
            
            return task_id
            
        except ValueError as e:
            logger.error(f"NFT minting failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during NFT minting: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Failed to queue NFT mint: {str(e)}")
    
    def _execute_nft_mint(
        self,
        nft_mint_id: str,
        wallet_address: str,
        nft_name: str,
        nft_description: str,
        nft_image_url: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Execute NFT minting operation (called by task manager).
        
        Args:
            nft_mint_id: NFT mint record ID
            wallet_address: Recipient wallet address
            nft_name: Name of the NFT
            nft_description: Description of the NFT
            nft_image_url: URL of the NFT image
            metadata: Additional metadata
            
        Returns:
            Dict: Minting result with transaction details
            
        Requirements:
            - 3.2: NFT minting via blockchain
            - 3.5: Retry mechanism with exponential backoff
        """
        try:
            # Update status to minting
            self.nft_repo.update_status(nft_mint_id, NFTMintStatus.MINTING)
            self.db_session.commit()
            
            logger.info(f"Starting NFT mint for record: {nft_mint_id}")
            
            # Call Sui client to mint NFT
            result = self.sui_client.mint_nft(
                recipient_address=wallet_address,
                nft_name=nft_name,
                nft_description=nft_description,
                nft_image_url=nft_image_url,
                metadata=metadata,
                use_sponsor=True
            )
            
            # Update NFT mint record with result
            self.nft_repo.update_status(
                nft_mint_id,
                NFTMintStatus.COMPLETED,
                nft_object_id=result.get('nft_object_id'),
                transaction_digest=result.get('transaction_digest')
            )
            self.db_session.commit()
            
            logger.info(f"NFT mint completed: {nft_mint_id}")
            
            return result
            
        except Exception as e:
            # Update status to failed
            error_message = str(e)
            self.nft_repo.update_status(
                nft_mint_id,
                NFTMintStatus.FAILED,
                error_message=error_message
            )
            self.db_session.commit()
            
            logger.error(f"NFT mint failed for {nft_mint_id}: {error_message}")
            raise
    
    def get_user_nfts(
        self,
        user_id: str,
        status: Optional[NFTMintStatus] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get all NFTs for a user.
        
        Args:
            user_id: User's unique identifier
            status: Optional status filter
            limit: Maximum number of NFTs to return
            
        Returns:
            List[Dict]: List of NFT mint records
            
        Requirements: 3.4 - User NFT list retrieval
        """
        nfts = self.nft_repo.find_by_user(user_id, status=status, limit=limit)
        return [nft.to_dict() for nft in nfts]
    
    def get_nft_by_id(self, nft_id: str) -> Optional[Dict]:
        """
        Get NFT mint record by ID.
        
        Args:
            nft_id: NFT mint record ID
            
        Returns:
            Optional[Dict]: NFT mint record or None if not found
        """
        nft = self.nft_repo.find_by_id(nft_id)
        if not nft:
            return None
        
        return nft.to_dict()
    
    def get_mint_status(self, nft_id: str) -> Optional[Dict]:
        """
        Get minting status for an NFT.
        
        Args:
            nft_id: NFT mint record ID
            
        Returns:
            Optional[Dict]: Status information or None if not found
        """
        nft = self.nft_repo.find_by_id(nft_id)
        if not nft:
            return None
        
        return {
            'id': nft.id,
            'status': nft.status.value,
            'nft_object_id': nft.nft_object_id,
            'transaction_digest': nft.transaction_digest,
            'error_message': nft.error_message,
            'created_at': nft.created_at.isoformat() if nft.created_at else None,
            'updated_at': nft.updated_at.isoformat() if nft.updated_at else None
        }
    
    def verify_nft_ownership(self, user_id: str, nft_object_id: str) -> bool:
        """
        Verify if a user owns a specific NFT.
        
        Args:
            user_id: User's unique identifier
            nft_object_id: NFT object ID on blockchain
            
        Returns:
            bool: True if user owns the NFT, False otherwise
            
        Requirements: 3.4 - NFT ownership verification
        """
        try:
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                logger.warning(f"User {user_id} has no wallet")
                return False
            
            # Check blockchain for ownership
            owns_nft = self.sui_client.verify_nft_ownership(
                wallet.address,
                nft_object_id
            )
            
            logger.info(
                f"NFT ownership verification for user {user_id}, "
                f"NFT {nft_object_id}: {owns_nft}"
            )
            
            return owns_nft
            
        except Exception as e:
            logger.error(f"Error verifying NFT ownership: {str(e)}")
            return False
    
    def has_completed_nft(self, user_id: str) -> bool:
        """
        Check if user has at least one completed NFT.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            bool: True if user has completed NFT, False otherwise
        """
        # Get user's wallet
        wallet = self.wallet_repo.find_by_user_id(user_id)
        if not wallet:
            return False
        
        return self.nft_repo.has_completed_nft(user_id, wallet.address)
    
    def get_nft_count(self, user_id: str, status: Optional[NFTMintStatus] = None) -> int:
        """
        Get count of NFTs for a user.
        
        Args:
            user_id: User's unique identifier
            status: Optional status filter
            
        Returns:
            int: Number of NFTs
        """
        return self.nft_repo.count_by_user(user_id, status=status)
    
    def get_wallet_nfts(self, wallet_address: str) -> List[Dict]:
        """
        Get all NFTs for a wallet address.
        
        Args:
            wallet_address: Sui blockchain wallet address
            
        Returns:
            List[Dict]: List of NFT mint records
        """
        nfts = self.nft_repo.find_by_wallet(wallet_address)
        return [nft.to_dict() for nft in nfts]
