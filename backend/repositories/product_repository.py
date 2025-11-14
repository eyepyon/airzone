"""
Product repository for managing product data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.product import Product
from repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product model operations.
    Provides custom queries for product filtering and stock management.
    
    Requirements: 3.4, 4.2, 4.3
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize ProductRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Product, db_session)
    
    def find_active_products(self) -> List[Product]:
        """
        Find all active products.
        
        Returns:
            List[Product]: List of active product instances
        """
        return self.db_session.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.created_at.desc()).all()
    
    def find_by_status(self, is_active: bool) -> List[Product]:
        """
        Find products by active status.
        
        Args:
            is_active: Whether to find active or inactive products
            
        Returns:
            List[Product]: List of product instances
        """
        return self.db_session.query(Product).filter(
            Product.is_active == is_active
        ).order_by(Product.created_at.desc()).all()
    
    def find_by_required_nft(self, required_nft_id: Optional[str]) -> List[Product]:
        """
        Find products by required NFT ID.
        
        Args:
            required_nft_id: NFT ID required for purchase, or None for no requirement
            
        Returns:
            List[Product]: List of product instances
        """
        if required_nft_id is None:
            return self.db_session.query(Product).filter(
                Product.required_nft_id.is_(None)
            ).all()
        else:
            return self.db_session.query(Product).filter(
                Product.required_nft_id == required_nft_id
            ).all()
    
    def find_available_products(self) -> List[Product]:
        """
        Find all products that are active and in stock.
        
        Returns:
            List[Product]: List of available product instances
        """
        return self.db_session.query(Product).filter(
            Product.is_active == True,
            Product.stock_quantity > 0
        ).order_by(Product.created_at.desc()).all()
    
    def find_by_price_range(self, min_price: int, max_price: int) -> List[Product]:
        """
        Find products within a price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            
        Returns:
            List[Product]: List of product instances
        """
        return self.db_session.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price,
            Product.is_active == True
        ).order_by(Product.price.asc()).all()
    
    def check_stock_availability(self, product_id: str, quantity: int) -> bool:
        """
        Check if sufficient stock is available for a product.
        
        Args:
            product_id: Product ID
            quantity: Quantity to check
            
        Returns:
            bool: True if sufficient stock available, False otherwise
        """
        product = self.find_by_id(product_id)
        if not product:
            return False
        return product.stock_quantity >= quantity
    
    def decrease_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """
        Decrease product stock quantity.
        
        Args:
            product_id: Product ID
            quantity: Quantity to decrease
            
        Returns:
            Optional[Product]: Updated product instance if successful, None otherwise
        """
        product = self.find_by_id(product_id)
        if not product or product.stock_quantity < quantity:
            return None
        
        new_stock = product.stock_quantity - quantity
        return self.update(product_id, stock_quantity=new_stock)
    
    def increase_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """
        Increase product stock quantity.
        
        Args:
            product_id: Product ID
            quantity: Quantity to increase
            
        Returns:
            Optional[Product]: Updated product instance if successful, None otherwise
        """
        product = self.find_by_id(product_id)
        if not product:
            return None
        
        new_stock = product.stock_quantity + quantity
        return self.update(product_id, stock_quantity=new_stock)
    
    def set_active_status(self, product_id: str, is_active: bool) -> Optional[Product]:
        """
        Set the active status of a product.
        
        Args:
            product_id: Product ID
            is_active: New active status
            
        Returns:
            Optional[Product]: Updated product instance if found, None otherwise
        """
        return self.update(product_id, is_active=is_active)
