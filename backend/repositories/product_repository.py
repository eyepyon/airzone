"""
Product Repository for managing e-commerce products.
Provides specialized queries for product operations.

Requirements: 3.4, 4.2, 4.3
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.product import Product
from repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository for product operations.
    Provides methods to query products by various criteria including active status,
    NFT requirements, and stock availability.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize Product repository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(Product, db_session)
    
    def find_active_products(self, limit: Optional[int] = None, 
                            offset: Optional[int] = None) -> List[Product]:
        """
        Find all active products.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List[Product]: List of active products
        """
        query = self.db_session.query(Product).filter(
            Product.is_active == True
        ).order_by(Product.created_at.desc())
        
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_status(self, is_active: bool, 
                       limit: Optional[int] = None) -> List[Product]:
        """
        Find products by active status.
        
        Args:
            is_active: Whether to find active or inactive products
            limit: Maximum number of records to return
            
        Returns:
            List[Product]: List of products matching the status
        """
        query = self.db_session.query(Product).filter(
            Product.is_active == is_active
        ).order_by(Product.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_nft_requirement(self, required_nft_id: Optional[str] = None,
                                only_active: bool = True) -> List[Product]:
        """
        Find products by NFT requirement.
        
        Args:
            required_nft_id: The required NFT ID (None for products without NFT requirement)
            only_active: Whether to only return active products
            
        Returns:
            List[Product]: List of products matching the NFT requirement
        """
        query = self.db_session.query(Product)
        
        if required_nft_id is None:
            query = query.filter(Product.required_nft_id.is_(None))
        else:
            query = query.filter(Product.required_nft_id == required_nft_id)
        
        if only_active:
            query = query.filter(Product.is_active == True)
        
        return query.order_by(Product.created_at.desc()).all()
    
    def find_available_products(self, min_stock: int = 1,
                               only_active: bool = True,
                               limit: Optional[int] = None) -> List[Product]:
        """
        Find products with available stock.
        
        Args:
            min_stock: Minimum stock quantity required
            only_active: Whether to only return active products
            limit: Maximum number of records to return
            
        Returns:
            List[Product]: List of products with available stock
        """
        query = self.db_session.query(Product).filter(
            Product.stock_quantity >= min_stock
        )
        
        if only_active:
            query = query.filter(Product.is_active == True)
        
        query = query.order_by(Product.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def search_products(self, search_term: str, 
                       only_active: bool = True,
                       limit: Optional[int] = None) -> List[Product]:
        """
        Search products by name or description.
        
        Args:
            search_term: The term to search for
            only_active: Whether to only return active products
            limit: Maximum number of records to return
            
        Returns:
            List[Product]: List of products matching the search term
        """
        search_pattern = f"%{search_term}%"
        query = self.db_session.query(Product).filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )
        
        if only_active:
            query = query.filter(Product.is_active == True)
        
        query = query.order_by(Product.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_price_range(self, min_price: Optional[int] = None,
                           max_price: Optional[int] = None,
                           only_active: bool = True) -> List[Product]:
        """
        Find products within a price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            only_active: Whether to only return active products
            
        Returns:
            List[Product]: List of products within the price range
        """
        query = self.db_session.query(Product)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if only_active:
            query = query.filter(Product.is_active == True)
        
        return query.order_by(Product.price.asc()).all()
    
    def update_stock(self, product_id: str, quantity_change: int) -> Optional[Product]:
        """
        Update product stock quantity by adding or subtracting.
        
        Args:
            product_id: The product ID
            quantity_change: The amount to add (positive) or subtract (negative)
            
        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        product = self.find_by_id(product_id)
        if not product:
            return None
        
        new_quantity = product.stock_quantity + quantity_change
        # Prevent negative stock
        if new_quantity < 0:
            new_quantity = 0
        
        return self.update(product_id, stock_quantity=new_quantity)
    
    def check_stock_availability(self, product_id: str, 
                                 required_quantity: int) -> bool:
        """
        Check if a product has sufficient stock.
        
        Args:
            product_id: The product ID
            required_quantity: The quantity needed
            
        Returns:
            bool: True if sufficient stock available, False otherwise
        """
        product = self.find_by_id(product_id)
        if not product:
            return False
        
        return product.stock_quantity >= required_quantity
    
    def deactivate_product(self, product_id: str) -> Optional[Product]:
        """
        Deactivate a product (soft delete).
        
        Args:
            product_id: The product ID
            
        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        return self.update(product_id, is_active=False)
    
    def activate_product(self, product_id: str) -> Optional[Product]:
        """
        Activate a product.
        
        Args:
            product_id: The product ID
            
        Returns:
            Optional[Product]: Updated product if found, None otherwise
        """
        return self.update(product_id, is_active=True)
    
    def count_active_products(self) -> int:
        """
        Count all active products.
        
        Returns:
            int: Number of active products
        """
        return self.db_session.query(Product).filter(
            Product.is_active == True
        ).count()
    
    def count_out_of_stock(self, only_active: bool = True) -> int:
        """
        Count products that are out of stock.
        
        Args:
            only_active: Whether to only count active products
            
        Returns:
            int: Number of out-of-stock products
        """
        query = self.db_session.query(Product).filter(
            Product.stock_quantity == 0
        )
        
        if only_active:
            query = query.filter(Product.is_active == True)
        
        return query.count()
