"""
NFT minting tasks with retry logic.
Handles asynchronous NFT minting on Sui blockchain with exponential backoff.
"""
import time
import logging
from typing import Dict, Any, Optional
from functools import wraps


logger = logging.getLogger(__name__)


def exponential_backoff_retry(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for implementing exponential backoff retry logic.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay in seconds for exponential backoff (default: 1.0)
        
    Returns:
        Decorated function with retry logic
        
    Requirements: 3.5, 10.5
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"Attempt {attempt + 1}/{max_retries} for {func.__name__}")
                    result = func(*args, **kwargs)
                    
                    if attempt > 0:
                        logger.info(f"{func.__name__} succeeded after {attempt + 1} attempts")
                    
                    return result
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} failed on attempt {attempt + 1}/{max_retries}: {str(e)}"
                    )
                    
                    # Don't sleep after the last attempt
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2^attempt * base_delay
                        delay = (2 ** attempt) * base_delay
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            
            # All retries exhausted
            logger.error(
                f"{func.__name__} failed after {max_retries} attempts. "
                f"Last error: {str(last_exception)}"
            )
            raise last_exception
        
        return wrapper
    return decorator


@exponential_backoff_retry(max_retries=3, base_delay=1.0)
def mint_nft_task(
    wallet_address: str,
    nft_metadata: Dict[str, Any],
    sui_client: Any,
    nft_repo: Any
) -> Dict[str, Any]:
    """
    Mint an NFT on Sui blockchain with retry logic.
    
    This function is designed to be executed as a background task.
    It includes exponential backoff retry mechanism for handling
    transient failures.
    
    Args:
        wallet_address: Target wallet address for the NFT
        nft_metadata: NFT metadata (name, description, image_url, etc.)
        sui_client: Sui blockchain client instance
        nft_repo: NFT repository instance
        
    Returns:
        Dict[str, Any]: Result containing transaction details
        
    Raises:
        Exception: If NFT minting fails after all retries
        
    Requirements: 3.1, 3.2, 3.5, 10.5
    """
    logger.info(f"Starting NFT mint for wallet: {wallet_address}")
    
    try:
        # Call Sui client to mint NFT
        # This will use sponsored transaction to pay for gas
        transaction_result = sui_client.mint_nft(
            recipient_address=wallet_address,
            name=nft_metadata.get('name', 'Airzone NFT'),
            description=nft_metadata.get('description', ''),
            image_url=nft_metadata.get('image_url', ''),
            metadata=nft_metadata
        )
        
        # Extract transaction details
        nft_object_id = transaction_result.get('nft_object_id')
        transaction_digest = transaction_result.get('transaction_digest')
        
        logger.info(
            f"NFT minted successfully. "
            f"Object ID: {nft_object_id}, "
            f"Transaction: {transaction_digest}"
        )
        
        return {
            'success': True,
            'nft_object_id': nft_object_id,
            'transaction_digest': transaction_digest,
            'wallet_address': wallet_address,
            'metadata': nft_metadata
        }
        
    except Exception as e:
        logger.error(f"NFT minting failed for wallet {wallet_address}: {str(e)}")
        raise


def retry_failed_task(
    task_func: callable,
    *args,
    max_retries: int = 3,
    **kwargs
) -> Any:
    """
    Generic retry function for failed tasks.
    
    Args:
        task_func: Function to retry
        *args: Positional arguments for the function
        max_retries: Maximum number of retry attempts
        **kwargs: Keyword arguments for the function
        
    Returns:
        Any: Result of the function execution
        
    Raises:
        Exception: If task fails after all retries
        
    Requirements: 3.5, 10.5
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
            result = task_func(*args, **kwargs)
            logger.info(f"Task succeeded on retry attempt {attempt + 1}")
            return result
            
        except Exception as e:
            last_exception = e
            logger.warning(f"Retry attempt {attempt + 1} failed: {str(e)}")
            
            if attempt < max_retries - 1:
                # Exponential backoff
                delay = 2 ** attempt
                logger.info(f"Waiting {delay} seconds before next retry...")
                time.sleep(delay)
    
    logger.error(f"Task failed after {max_retries} retry attempts")
    raise last_exception


def process_nft_mint_queue(
    task_manager: Any,
    sui_client: Any,
    nft_repo: Any,
    user_id: str,
    wallet_address: str,
    nft_metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Queue an NFT minting task for asynchronous processing.
    
    Args:
        task_manager: TaskManager instance
        sui_client: Sui blockchain client
        nft_repo: NFT repository
        user_id: User ID
        wallet_address: Target wallet address
        nft_metadata: Optional NFT metadata
        
    Returns:
        str: Task ID for tracking
        
    Requirements: 3.1, 10.1, 10.2
    """
    if nft_metadata is None:
        nft_metadata = {
            'name': 'Airzone WiFi NFT',
            'description': 'NFT issued for WiFi connection',
            'image_url': ''
        }
    
    # Prepare payload for task tracking
    payload = {
        'user_id': user_id,
        'wallet_address': wallet_address,
        'nft_metadata': nft_metadata
    }
    
    # Submit task to task manager
    task_id = task_manager.submit_task(
        task_type='nft_mint',
        func=mint_nft_task,
        wallet_address=wallet_address,
        nft_metadata=nft_metadata,
        sui_client=sui_client,
        nft_repo=nft_repo,
        payload=payload,
        max_retries=3
    )
    
    logger.info(f"NFT mint task queued with ID: {task_id}")
    return task_id
