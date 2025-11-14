"""
OrderRepository for managing order and order item data access.
Provides methods for order CRUD operations and status management.

Requirements: 5.3, 5.4, 5.6
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from repositories.base import BaseRepository
from models.order import Order, OrderItem, OrderStatus


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model.
    Handles order creation, retrieval, and status updates.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderRepository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Order, db_session)
    
    def find_by_user(self, user_id: str, limit: Optional[int] = None, 
                     offset: Optional[int] = None) -> List[Order]:
        """
        Find all orders for a specific user.
        
        Args:
            user_id: The user ID to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List[Order]: List of orders for the user
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
        
        Args:
            order_id: The order ID to find
            
        Returns:
            Optional[Order]: Order with items if found, None otherwise
        """
        return self.db_session.query(Order).options(
            joinedload(Order.order_items)
        ).filter(Order.id == order_id).first()
    
    def find_by_status(self, status: OrderStatus, limit: Optional[int] = None) -> List[Order]:
        """
        Find orders by status.
        
        Args:
            status: The order status to filter by
            limit: Maximum number of records to return
            
        Returns:
            List[Order]: List of orders with the specified status
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
        
        Args:
            order_id: The order ID to update
            status: The new status
            
        Returns:
            Optional[Order]: Updated order if found, None otherwise
        """
        return self.update(order_id, status=status)
    
    def create_with_items(self, user_id: str, total_amount: int, 
                         items: List[dict]) -> Order:
        """
        Create an order with its order items in a single transaction.
        
        Args:
            user_id: The user ID creating the order
            total_amount: Total order amount
            items: List of order item dictionaries with keys:
                   product_id, quantity, unit_price, subtotal
            
        Returns:
            Order: Created order with items
            
        Raises:
            SQLAlchemyError: If database operation fails
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


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model.
    Handles order item CRUD operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize OrderItemRepository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(OrderItem, db_session)
    
    def find_by_order(self, order_id: str) -> List[OrderItem]:
        """
        Find all items for a specific order.
        
        Args:
            order_id: The order ID to filter by
            
        Returns:
            List[OrderItem]: List of order items
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
    
    def find_by_product(self, product_id: str) -> List[OrderItem]:
        """
        Find all order items for a specific product.
        
        Args:
            product_id: The product ID to filter by
            
        Returns:
            List[OrderItem]: List of order items
        """
        return self.db_session.query(OrderItem).filter(
            OrderItem.product_id == product_id
        ).all()
