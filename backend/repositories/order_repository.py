"""
Order repository for managing order data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from models.order import Order, OrderItem, OrderStatus
from repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model operations.
    Provides custom queries for order lookup and status management.
    
    Requirements: 5.3, 5.4, 5.5, 5.6
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Order, db_session)
    
    def find_by_user_id(self, user_id: str) -> List[Order]:
        """
        Find all orders for a specific user.
        
        Args:
            user_id: User's ID
            
        Returns:
            List[Order]: List of order instances
        """
        return self.db_session.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc()).all()
    
    def find_by_status(self, status: OrderStatus) -> List[Order]:
        """
        Find all orders with a specific status.
        
        Args:
            status: Order status to filter by
            
        Returns:
            List[Order]: List of order instances
        """
        return self.db_session.query(Order).filter(
            Order.status == status
        ).order_by(Order.created_at.desc()).all()
    
    def find_by_user_and_status(self, user_id: str, 
                                status: OrderStatus) -> List[Order]:
        """
        Find orders by user ID and status.
        
        Args:
            user_id: User's ID
            status: Order status to filter by
            
        Returns:
            List[Order]: List of order instances
        """
        return self.db_session.query(Order).filter(
            Order.user_id == user_id,
            Order.status == status
        ).order_by(Order.created_at.desc()).all()
    
    def find_with_items(self, order_id: str) -> Optional[Order]:
        """
        Find an order with its items eagerly loaded.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Order]: Order instance with items if found, None otherwise
        """
        return self.db_session.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.id == order_id).first()
    
    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        """
        Update the status of an order.
        
        Args:
            order_id: Order ID
            status: New order status
            
        Returns:
            Optional[Order]: Updated order instance if found, None otherwise
        """
        return self.update(order_id, status=status)
    
    def count_by_status(self, status: OrderStatus) -> int:
        """
        Count orders with a specific status.
        
        Args:
            status: Order status to count
            
        Returns:
            int: Number of orders with the given status
        """
        return self.db_session.query(Order).filter(
            Order.status == status
        ).count()
    
    def find_pending_orders(self) -> List[Order]:
        """
        Find all pending orders.
        
        Returns:
            List[Order]: List of pending order instances
        """
        return self.find_by_status(OrderStatus.PENDING)
    
    def find_completed_orders_by_user(self, user_id: str) -> List[Order]:
        """
        Find all completed orders for a user.
        
        Args:
            user_id: User's ID
            
        Returns:
            List[Order]: List of completed order instances
        """
        return self.find_by_user_and_status(user_id, OrderStatus.COMPLETED)


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model operations.
    Provides queries for order item management.
    
    Requirements: 5.3, 5.4
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderItemRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(OrderItem, db_session)
    
    def find_by_order_id(self, order_id: str) -> List[OrderItem]:
        """
        Find all items for a specific order.
        
        Args:
            order_id: Order ID
            
        Returns:
            List[OrderItem]: List of order item instances
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
    
    def find_by_product_id(self, product_id: str) -> List[OrderItem]:
        """
        Find all order items for a specific product.
        
        Args:
            product_id: Product ID
            
        Returns:
            List[OrderItem]: List of order item instances
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.product_id == product_id
        ).all()
