"""
Order Service for managing e-commerce orders.
Handles order creation, validation, NFT requirement checking, and status updates.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7
"""
from typing import List, Dict, Optional
import logging
from sqlalchemy.orm import Session
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from repositories.nft_repository import NFTRepository
from repositories.wallet_repository import WalletRepository
from models.order import OrderStatus


logger = logging.getLogger(__name__)


class OrderService:
    """
    Service for order operations.
    Handles order creation, validation, and status management.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderService.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.order_repo = OrderRepository(db_session)
        self.product_repo = ProductRepository(db_session)
        self.user_repo = UserRepository(db_session)
        self.nft_repo = NFTRepository(db_session)
        self.wallet_repo = WalletRepository(db_session)
    
    def create_order(
        self,
        user_id: str,
        items: List[Dict[str, any]]
    ) -> Dict:
        """
        Create a new order with validation.
        Validates NFT requirements, stock availability, and reserves stock.
        
        Args:
            user_id: User's unique identifier
            items: List of order items with format:
                   [{'product_id': str, 'quantity': int}, ...]
            
        Returns:
            Dict: Created order information
            
        Raises:
            ValueError: If validation fails
            
        Requirements:
            - 5.1: Order creation
            - 5.2: NFT requirement validation
            - 5.3: Order record creation
        """
        try:
            # Verify user exists
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            
            # Validate items
            if not items or len(items) == 0:
                raise ValueError("Order must contain at least one item")
            
            # Validate each item and calculate total
            validated_items = []
            total_amount = 0
            
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity', 1)
                
                if not product_id:
                    raise ValueError("Product ID is required for each item")
                
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
                
                # Get product
                product = self.product_repo.find_by_id(product_id)
                if not product:
                    raise ValueError(f"Product not found: {product_id}")
                
                if not product.is_active:
                    raise ValueError(f"Product is not active: {product_id}")
                
                # Check NFT requirement
                if product.required_nft_id:
                    if not self._verify_user_nft_requirement(user_id, product.required_nft_id):
                        raise ValueError(
                            f"User does not meet NFT requirement for product: {product.name}"
                        )
                
                # Check stock availability
                if not self.product_repo.check_stock_availability(product_id, quantity):
                    raise ValueError(f"Insufficient stock for product: {product.name}")
                
                # Calculate subtotal
                subtotal = product.price * quantity
                total_amount += subtotal
                
                validated_items.append({
                    'product_id': product_id,
                    'product': product,
                    'quantity': quantity,
                    'unit_price': product.price,
                    'subtotal': subtotal
                })
            
            # Create order
            order = self.order_repo.create(
                user_id=user_id,
                total_amount=total_amount,
                status=OrderStatus.PENDING
            )
            
            # Create order items and reserve stock
            for item_data in validated_items:
                self.order_repo.create_order_item(
                    order_id=order.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
                
                # Reserve stock
                self.product_repo.update_stock(
                    item_data['product_id'],
                    -item_data['quantity']
                )
            
            self.db_session.commit()
            logger.info(f"Created order: {order.id} for user: {user_id}")
            
            return self._get_order_with_items(order.id)
            
        except ValueError as e:
            logger.error(f"Order creation failed: {str(e)}")
            self.db_session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating order: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Failed to create order: {str(e)}")
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Get order by ID with items.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Dict]: Order information with items or None if not found
            
        Requirements: 5.4 - Order retrieval
        """
        return self._get_order_with_items(order_id)
    
    def get_user_orders(
        self,
        user_id: str,
        status: Optional[OrderStatus] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get all orders for a user.
        
        Args:
            user_id: User's unique identifier
            status: Optional status filter
            limit: Maximum number of orders to return
            
        Returns:
            List[Dict]: List of orders with items
            
        Requirements: 5.4 - User order history
        """
        orders = self.order_repo.find_by_user(user_id, status=status, limit=limit)
        
        return [self._get_order_with_items(order.id) for order in orders]
    
    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus
    ) -> Optional[Dict]:
        """
        Update order status.
        
        Args:
            order_id: Order ID
            status: New order status
            
        Returns:
            Optional[Dict]: Updated order or None if not found
            
        Requirements: 5.6 - Order status update
        """
        try:
            order = self.order_repo.update_status(order_id, status)
            
            if not order:
                logger.warning(f"Order not found: {order_id}")
                return None
            
            self.db_session.commit()
            logger.info(f"Updated order {order_id} status to {status.value}")
            
            return self._get_order_with_items(order_id)
            
        except Exception as e:
            logger.error(f"Failed to update order status: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Order status update failed: {str(e)}")
    
    def complete_order(self, order_id: str) -> Optional[Dict]:
        """
        Mark order as completed.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Dict]: Updated order or None if not found
            
        Requirements: 5.6 - Order completion
        """
        return self.update_order_status(order_id, OrderStatus.COMPLETED)
    
    def fail_order(self, order_id: str) -> Optional[Dict]:
        """
        Mark order as failed and restore stock.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Dict]: Updated order or None if not found
            
        Requirements: 5.7 - Order failure handling with stock restoration
        """
        try:
            order = self.order_repo.find_by_id(order_id)
            if not order:
                logger.warning(f"Order not found: {order_id}")
                return None
            
            # Restore stock for all items
            for item in order.order_items:
                self.product_repo.update_stock(item.product_id, item.quantity)
                logger.info(
                    f"Restored {item.quantity} units of product {item.product_id}"
                )
            
            # Update order status
            order = self.order_repo.update_status(order_id, OrderStatus.FAILED)
            self.db_session.commit()
            
            logger.info(f"Failed order {order_id} and restored stock")
            
            return self._get_order_with_items(order_id)
            
        except Exception as e:
            logger.error(f"Failed to fail order: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Order failure handling failed: {str(e)}")
    
    def cancel_order(self, order_id: str) -> Optional[Dict]:
        """
        Cancel order and restore stock.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Dict]: Updated order or None if not found
            
        Requirements: 5.7 - Order cancellation with stock restoration
        """
        try:
            order = self.order_repo.find_by_id(order_id)
            if not order:
                logger.warning(f"Order not found: {order_id}")
                return None
            
            # Only allow cancellation of pending or processing orders
            if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
                raise ValueError(
                    f"Cannot cancel order with status: {order.status.value}"
                )
            
            # Restore stock for all items
            for item in order.order_items:
                self.product_repo.update_stock(item.product_id, item.quantity)
                logger.info(
                    f"Restored {item.quantity} units of product {item.product_id}"
                )
            
            # Update order status
            order = self.order_repo.update_status(order_id, OrderStatus.CANCELLED)
            self.db_session.commit()
            
            logger.info(f"Cancelled order {order_id} and restored stock")
            
            return self._get_order_with_items(order_id)
            
        except ValueError as e:
            logger.error(f"Order cancellation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Order cancellation failed: {str(e)}")
    
    def _verify_user_nft_requirement(self, user_id: str, required_nft_id: str) -> bool:
        """
        Verify if user meets NFT requirement.
        
        Args:
            user_id: User's unique identifier
            required_nft_id: Required NFT ID
            
        Returns:
            bool: True if user meets requirement, False otherwise
            
        Requirements: 5.2 - NFT requirement verification
        """
        try:
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                logger.warning(f"User {user_id} has no wallet")
                return False
            
            # Check if user has completed NFT
            has_nft = self.nft_repo.has_completed_nft(user_id, wallet.address)
            
            logger.info(
                f"NFT requirement verification for user {user_id}: {has_nft}"
            )
            
            return has_nft
            
        except Exception as e:
            logger.error(f"Error verifying NFT requirement: {str(e)}")
            return False
    
    def validate_nft_requirements(
        self,
        user_id: str,
        product_ids: List[str]
    ) -> Dict:
        """
        Validate NFT requirements for a list of products.
        
        Args:
            user_id: User's unique identifier
            product_ids: List of product IDs to validate
            
        Returns:
            Dict: Validation result with format:
                  {
                      'valid': bool,
                      'message': str,
                      'missing_nfts': List[str]
                  }
            
        Requirements: 5.2 - NFT requirement validation
        """
        try:
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                return {
                    'valid': False,
                    'message': 'ウォレットが見つかりません。ウォレットを作成してください。',
                    'missing_nfts': []
                }
            
            # Get all products
            products_with_nft_requirement = []
            for product_id in product_ids:
                product = self.product_repo.find_by_id(product_id)
                if product and product.required_nft_id:
                    products_with_nft_requirement.append(product)
            
            # If no products require NFTs, validation passes
            if not products_with_nft_requirement:
                return {
                    'valid': True,
                    'message': 'NFT要件はありません',
                    'missing_nfts': []
                }
            
            # Get user's completed NFTs
            user_nfts = self.nft_repo.find_by_wallet(wallet.address)
            completed_nft_ids = [
                nft.id for nft in user_nfts 
                if nft.status.value == 'completed'
            ]
            
            # Check each product's NFT requirement
            missing_nfts = []
            for product in products_with_nft_requirement:
                if product.required_nft_id not in completed_nft_ids:
                    missing_nfts.append({
                        'product_id': product.id,
                        'product_name': product.name,
                        'required_nft_id': product.required_nft_id
                    })
            
            if missing_nfts:
                product_names = ', '.join([nft['product_name'] for nft in missing_nfts])
                return {
                    'valid': False,
                    'message': f'以下の商品に必要なNFTを保有していません: {product_names}',
                    'missing_nfts': missing_nfts
                }
            
            return {
                'valid': True,
                'message': 'すべてのNFT要件を満たしています',
                'missing_nfts': []
            }
            
        except Exception as e:
            logger.error(f"Error validating NFT requirements: {str(e)}")
            return {
                'valid': False,
                'message': 'NFT要件の確認中にエラーが発生しました',
                'missing_nfts': []
            }
    
    def _get_order_with_items(self, order_id: str) -> Optional[Dict]:
        """
        Get order with items and product details.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Dict]: Order with items or None if not found
        """
        order = self.order_repo.find_by_id(order_id)
        if not order:
            return None
        
        order_dict = order.to_dict()
        
        # Add order items with product details
        items = []
        for item in order.order_items:
            item_dict = item.to_dict()
            
            # Add product details
            product = self.product_repo.find_by_id(item.product_id)
            if product:
                item_dict['product'] = product.to_dict()
            
            items.append(item_dict)
        
        order_dict['items'] = items
        
        return order_dict
