"""
Order repository for managing order and order item data access.
Provides custom queries for order management and status updates.

Requirements: 5.3, 5.4, 5.6
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from models.order import Order, OrderItem, OrderStatus
from repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model with custom query methods.
    Handles order creation, retrieval, and status management operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Order, db_session)
    
    def find_by_user(self, user_id: str, limit: Optional[int] = None, 
                     offset: Optional[int] = None) -> List[Order]:
        """
        Find all orders for a specific user.
        Used to retrieve user's order history.
        
        Args:
            user_id: User's ID
            limit: Maximum number of orders to return
            offset: Number of orders to skip
            
        Returns:
            List[Order]: List of user's orders
            
        Requirements: 5.4 - Order retrieval and management
        """
        query = self.db_session.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc())
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_id_with_items(self, order_id: str) -> Optional[Order]:
        """
        Find an order by ID with its order items eagerly loaded.
        Optimizes query by loading related items in a single query.
        
        Args:
            order_id: Order's ID
            
        Returns:
            Optional[Order]: Order instance with items if found, None otherwise
            
        Requirements: 5.4 - Order detail retrieval
        """
        return self.db_session.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.id == order_id).first()
    
    def find_by_status(self, status: OrderStatus, limit: Optional[int] = None) -> List[Order]:
        """
        Find all orders with a specific status.
        Used for order processing and management.
        
        Args:
            status: Order status to filter by
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of orders with the specified status
            
        Requirements: 5.6 - Order status management
        """
        query = self.db_session.query(Order).filter(
            Order.status == status
        ).order_by(Order.created_at.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        """
        Update the status of an order.
        Used during order processing and payment completion.
        
        Args:
            order_id: Order's ID
            status: New order status
            
        Returns:
            Optional[Order]: Updated order instance if found, None otherwise
            
        Requirements: 5.6 - Order status updates during payment processing
        """
        return self.update(order_id, status=status)
    
    def create_order_with_items(self, user_id: str, total_amount: int, 
                                items: List[dict]) -> Order:
        """
        Create a new order with order items in a single transaction.
        
        Args:
            user_id: User's ID
            total_amount: Total order amount
            items: List of order item dictionaries with keys:
                   product_id, quantity, unit_price, subtotal
            
        Returns:
            Order: Created order instance with items
            
        Requirements: 5.3 - Order creation with items
        """
        try:
            # Create order
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                status=OrderStatus.PENDING
            )
            self.db_session.add(order)
            self.db_session.flush()  # Get order ID without committing
            
            # Create order items
            for item_data in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
                self.db_session.add(order_item)
            
            self.db_session.commit()
            self.db_session.refresh(order)
            return order
        except Exception as e:
            self.db_session.rollback()
            raise e
    
    def count_by_user(self, user_id: str) -> int:
        """
        Count total orders for a specific user.
        
        Args:
            user_id: User's ID
            
        Returns:
            int: Number of orders
        """
        return self.db_session.query(Order).filter(
            Order.user_id == user_id
        ).count()
    
    def count_by_status(self, status: OrderStatus) -> int:
        """
        Count orders with a specific status.
        
        Args:
            status: Order status to count
            
        Returns:
            int: Number of orders with the status
        """
        return self.db_session.query(Order).filter(
            Order.status == status
        ).count()


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model.
    Handles order item specific operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderItemRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(OrderItem, db_session)
    
    def find_by_order(self, order_id: str) -> List[OrderItem]:
        """
        Find all items for a specific order.
        
        Args:
            order_id: Order's ID
            
        Returns:
            List[OrderItem]: List of order items
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
    
    def find_by_product(self, product_id: str) -> List[OrderItem]:
        """
        Find all order items for a specific product.
        Useful for product sales analytics.
        
        Args:
            product_id: Product's ID
            
        Returns:
            List[OrderItem]: List of order items
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.product_id == product_id
        ).all()
