"""
Order and OrderItem models for e-commerce transactions.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum


class OrderStatus(enum.Enum):
    """Enum for order status"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    """
    Order model representing a customer order.
    Contains order-level information and references to order items.
    """
    __tablename__ = 'orders'
    
    # Order fields
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_amount = Column(Integer, nullable=False)  # Total in smallest currency unit
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )
    
    # Relationships
    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payments = relationship('Payment', back_populates='order', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert order to dictionary.
        
        Args:
            exclude_fields (list): Fields to exclude
            
        Returns:
            dict: Order data dictionary
        """
        result = super().to_dict(exclude_fields=exclude_fields)
        
        # Convert enum to string value
        if 'status' in result and isinstance(result['status'], OrderStatus):
            result['status'] = result['status'].value
        
        return result
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount}, status={self.status.value})>"


class OrderItem(BaseModel):
    """
    OrderItem model representing individual items within an order.
    Links products to orders with quantity and pricing information.
    """
    __tablename__ = 'order_items'
    
    # OrderItem fields
    order_id = Column(String(36), ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)  # Price per unit at time of order
    subtotal = Column(Integer, nullable=False)  # quantity * unit_price
    
    # Relationships
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product')
    
    # Indexes
    __table_args__ = (
        Index('idx_order_id', 'order_id'),
    )
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
