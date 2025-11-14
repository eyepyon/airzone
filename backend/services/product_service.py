"""
Product Service for managing e-commerce products.
Handles product CRUD operations, stock management, and NFT requirement verification.

Requirements: 4.2, 4.3, 4.4, 4.5
"""
from typing import List, Dict, Optional
import logging
from sqlalchemy.orm import Session
from repositories.product_repository import ProductRepository
from repositories.nft_repository import NFTRepository
from repositories.wallet_repository import WalletRepository


logger = logging.getLogger(__name__)


class ProductService:
    """
    Service for product operations.
    Handles product management, stock control, and NFT requirement verification.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize ProductService.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.product_repo = ProductRepository(db_session)
        self.nft_repo = NFTRepository(db_session)
        self.wallet_repo = WalletRepository(db_session)
    
    def create_product(
        self,
        name: str,
        price: int,
        description: Optional[str] = None,
        stock_quantity: int = 0,
        image_url: Optional[str] = None,
        required_nft_id: Optional[str] = None,
        is_active: bool = True
    ) -> Dict:
        """
        Create a new product.
        
        Args:
            name: Product name
            price: Price in smallest currency unit (e.g., yen)
            description: Product description
            stock_quantity: Initial stock quantity
            image_url: Product image URL
            required_nft_id: Optional NFT ID required to purchase
            is_active: Whether product is active
            
        Returns:
            Dict: Created product information
            
        Requirements: 4.2 - Product creation
        """
        try:
            product = self.product_repo.create(
                name=name,
                price=price,
                description=description,
                stock_quantity=stock_quantity,
                image_url=image_url,
                required_nft_id=required_nft_id,
                is_active=is_active
            )
            
            self.db_session.commit()
            logger.info(f"Created product: {product.id} - {name}")
            
            return product.to_dict()
            
        except Exception as e:
            logger.error(f"Failed to create product: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Product creation failed: {str(e)}")
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Optional[Dict]: Product information or None if not found
            
        Requirements: 4.3 - Product retrieval
        """
        product = self.product_repo.find_by_id(product_id)
        if not product:
            return None
        
        return product.to_dict()
    
    def get_all_products(
        self,
        only_active: bool = True,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict]:
        """
        Get all products.
        
        Args:
            only_active: Whether to only return active products
            limit: Maximum number of products to return
            offset: Number of products to skip
            
        Returns:
            List[Dict]: List of products
            
        Requirements: 4.1 - Product listing
        """
        if only_active:
            products = self.product_repo.find_active_products(limit=limit, offset=offset)
        else:
            products = self.product_repo.find_all()
            if offset:
                products = products[offset:]
            if limit:
                products = products[:limit]
        
        return [product.to_dict() for product in products]
    
    def update_product(
        self,
        product_id: str,
        **kwargs
    ) -> Optional[Dict]:
        """
        Update product information.
        
        Args:
            product_id: Product ID
            **kwargs: Fields to update
            
        Returns:
            Optional[Dict]: Updated product or None if not found
            
        Requirements: 4.4 - Product update
        """
        try:
            product = self.product_repo.update(product_id, **kwargs)
            
            if not product:
                logger.warning(f"Product not found: {product_id}")
                return None
            
            self.db_session.commit()
            logger.info(f"Updated product: {product_id}")
            
            return product.to_dict()
            
        except Exception as e:
            logger.error(f"Failed to update product: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Product update failed: {str(e)}")
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete (deactivate) a product.
        
        Args:
            product_id: Product ID
            
        Returns:
            bool: True if deleted, False if not found
            
        Requirements: 4.5 - Product deletion
        """
        try:
            product = self.product_repo.deactivate_product(product_id)
            
            if not product:
                logger.warning(f"Product not found: {product_id}")
                return False
            
            self.db_session.commit()
            logger.info(f"Deactivated product: {product_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete product: {str(e)}")
            self.db_session.rollback()
            raise Exception(f"Product deletion failed: {str(e)}")
    
    def check_stock_availability(self, product_id: str, quantity: int) -> bool:
        """
        Check if product has sufficient stock.
        
        Args:
            product_id: Product ID
            quantity: Required quantity
            
        Returns:
            bool: True if sufficient stock available, False otherwise
            
        Requirements: 4.3 - Stock availability check
        """
        return self.product_repo.check_stock_availability(product_id, quantity)
    
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """
        Reserve stock for a product (decrease stock quantity).
        
        Args:
            product_id: Product ID
            quantity: Quantity to reserve
            
        Returns:
            bool: True if stock reserved successfully, False otherwise
            
        Requirements: 4.3 - Stock management
        """
        try:
            # Check availability first
            if not self.check_stock_availability(product_id, quantity):
                logger.warning(f"Insufficient stock for product {product_id}")
                return False
            
            # Decrease stock
            product = self.product_repo.update_stock(product_id, -quantity)
            
            if not product:
                logger.error(f"Failed to reserve stock for product {product_id}")
                return False
            
            self.db_session.commit()
            logger.info(f"Reserved {quantity} units of product {product_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to reserve stock: {str(e)}")
            self.db_session.rollback()
            return False
    
    def restore_stock(self, product_id: str, quantity: int) -> bool:
        """
        Restore stock for a product (increase stock quantity).
        Used when order is cancelled or payment fails.
        
        Args:
            product_id: Product ID
            quantity: Quantity to restore
            
        Returns:
            bool: True if stock restored successfully, False otherwise
            
        Requirements: 4.3 - Stock management
        """
        try:
            product = self.product_repo.update_stock(product_id, quantity)
            
            if not product:
                logger.error(f"Failed to restore stock for product {product_id}")
                return False
            
            self.db_session.commit()
            logger.info(f"Restored {quantity} units of product {product_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore stock: {str(e)}")
            self.db_session.rollback()
            return False
    
    def verify_nft_requirement(self, user_id: str, product_id: str) -> bool:
        """
        Verify if user meets NFT requirement for a product.
        
        Args:
            user_id: User's unique identifier
            product_id: Product ID
            
        Returns:
            bool: True if user meets requirement (or no requirement), False otherwise
            
        Requirements: 4.2 - NFT requirement verification
        """
        try:
            # Get product
            product = self.product_repo.find_by_id(product_id)
            if not product:
                logger.warning(f"Product not found: {product_id}")
                return False
            
            # If no NFT required, allow purchase
            if not product.required_nft_id:
                return True
            
            # Get user's wallet
            wallet = self.wallet_repo.find_by_user_id(user_id)
            if not wallet:
                logger.warning(f"User {user_id} has no wallet")
                return False
            
            # Check if user has completed NFT
            has_nft = self.nft_repo.has_completed_nft(user_id, wallet.address)
            
            logger.info(
                f"NFT requirement verification for user {user_id}, "
                f"product {product_id}: {has_nft}"
            )
            
            return has_nft
            
        except Exception as e:
            logger.error(f"Error verifying NFT requirement: {str(e)}")
            return False
    
    def get_products_by_nft_requirement(
        self,
        required_nft_id: Optional[str] = None,
        only_active: bool = True
    ) -> List[Dict]:
        """
        Get products by NFT requirement.
        
        Args:
            required_nft_id: NFT ID required (None for products without requirement)
            only_active: Whether to only return active products
            
        Returns:
            List[Dict]: List of products
        """
        products = self.product_repo.find_by_nft_requirement(
            required_nft_id=required_nft_id,
            only_active=only_active
        )
        
        return [product.to_dict() for product in products]
    
    def search_products(
        self,
        search_term: str,
        only_active: bool = True,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Search products by name or description.
        
        Args:
            search_term: Search term
            only_active: Whether to only return active products
            limit: Maximum number of products to return
            
        Returns:
            List[Dict]: List of matching products
        """
        products = self.product_repo.search_products(
            search_term=search_term,
            only_active=only_active,
            limit=limit
        )
        
        return [product.to_dict() for product in products]
    
    def get_available_products(
        self,
        min_stock: int = 1,
        only_active: bool = True,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get products with available stock.
        
        Args:
            min_stock: Minimum stock quantity required
            only_active: Whether to only return active products
            limit: Maximum number of products to return
            
        Returns:
            List[Dict]: List of available products
        """
        products = self.product_repo.find_available_products(
            min_stock=min_stock,
            only_active=only_active,
            limit=limit
        )
        
        return [product.to_dict() for product in products]
