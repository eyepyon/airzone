"""
Product model for e-commerce shop items.
"""
from sqlalchemy import Column, String, Text, Integer, Boolean, Index, JSON
from models.base import BaseModel


class Product(BaseModel):
    """
    Product model representing items available for purchase in the EC shop.
    Products can optionally require NFT ownership for purchase.
    """
    __tablename__ = 'products'
    
    # Product fields
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(20), nullable=True, default='goods')  # goods, nft, ticket
    delivery_method = Column(String(20), nullable=True, default='venue_pickup')  # 後方互換性のため保持
    delivery_options = Column(JSON, nullable=True)  # 利用可能な受け取り方法の配列 ['venue_pickup', 'home_delivery', 'airzone_pickup']
    price = Column(Integer, nullable=False)  # Price in smallest currency unit (e.g., cents, yen)
    stock_quantity = Column(Integer, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)
    required_nft_id = Column(String(36), nullable=True)  # Optional NFT requirement
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_is_active', 'is_active'),
        Index('idx_required_nft', 'required_nft_id'),
    )
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
