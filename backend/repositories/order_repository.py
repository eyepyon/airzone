"""
Order repository for managing order and order item data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from models.order import Order, OrderItem, OrderStatus
from repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model operations.
    Provides custom queries for order filtering and status management.
    
    Requirements: 5.3, 5.4, 5.6
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Order, db_session)
    
    def find_by_user(self, user_id: str, limit: Optional[int] = None) -> List[Order]:
        """
        Find all orders for a specific user.
        
        Args:
            user_id: User ID
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of order instances
        """
        query = self.db_session.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
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
    
    def find_by_user_and_status(self, user_id: str, status: OrderStatus) -> List[Order]:
        """
        Find orders for a specific user with a specific status.
        
        Args:
            user_id: User ID
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
        Find an order by ID with its order items eagerly loaded.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Order]: Order instance with items if found, None otherwise
        """
        return self.db_session.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.id == order_id).first()
    
    def find_with_items_and_payments(self, order_id: str) -> Optional[Order]:
        """
        Find an order by ID with its order items and payments eagerly loaded.
        
        Args:
            order_id: Order ID
            
        Returns:
            Optional[Order]: Order instance with items and payments if found, None otherwise
        """
        return self.db_session.query(Order).options(
            joinedload(Order.order_items),
            joinedload(Order.payments)
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
    
    def get_total_amount_by_user(self, user_id: str, status: Optional[OrderStatus] = None) -> int:
        """
        Calculate total amount of orders for a user.
        
        Args:
            user_id: User ID
            status: Optional status filter
            
        Returns:
            int: Total amount in smallest currency unit
        """
        query = self.db_session.query(Order).filter(
            Order.user_id == user_id
        )
        
        if status:
            query = query.filter(Order.status == status)
        
        orders = query.all()
        return sum(order.total_amount for order in orders)
    
    def count_by_user(self, user_id: str, status: Optional[OrderStatus] = None) -> int:
        """
        Count orders for a specific user.
        
        Args:
            user_id: User ID
            status: Optional status filter
            
        Returns:
            int: Number of orders
        """
        query = self.db_session.query(Order).filter(
            Order.user_id == user_id
        )
        
        if status:
            query = query.filter(Order.status == status)
        
        return query.count()


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model operations.
    Provides custom queries for order item management.
    
    Requirements: 5.3, 5.4
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
            order_id: Order ID
            
        Returns:
            List[OrderItem]: List of order item instances
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
    
    def find_by_product(self, product_id: str) -> List[OrderItem]:
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
    
    def get_total_quantity_by_product(self, product_id: str) -> int:
        """
        Calculate total quantity ordered for a specific product.
        
        Args:
            product_id: Product ID
            
        Returns:
            int: Total quantity ordered
        """
        items = self.find_by_product(product_id)
        return sum(item.quantity for item in items)
    
    def create_bulk(self, order_items_data: List[dict]) -> List[OrderItem]:
        """
        Create multiple order items in bulk.
        
        Args:
            order_items_data: List of dictionaries containing order item data
            
        Returns:
            List[OrderItem]: List of created order item instances
        """
        try:
            items = [OrderItem(**data) for data in order_items_data]
            self.db_session.add_all(items)
            self.db_session.commit()
            
            for item in items:
                self.db_session.refresh(item)
            
            return items
        except Exception as e:
            self.db_session.rollback()
            raise e
