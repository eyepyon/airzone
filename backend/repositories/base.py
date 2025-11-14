"""
Base repository class providing common CRUD operations.
All repositories should inherit from this class.
"""
from typing import TypeVar, Generic, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.base import BaseModel


T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Base repository class that provides common CRUD operations.
    Uses parameterized queries to prevent SQL injection attacks.
    
    Requirements: 6.4, 8.4, 9.2
    """
    
    def __init__(self, model_class: type[T], db_session: Session):
        """
        Initialize repository with model class and database session.
        
        Args:
            model_class: The SQLAlchemy model class
            db_session: SQLAlchemy database session
        """
        self.model_class = model_class
        self.db_session = db_session
    
    def create(self, **kwargs) -> T:
        """
        Create a new record in the database.
        
        Args:
            **kwargs: Field values for the new record
            
        Returns:
            T: Created model instance
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            instance = self.model_class(**kwargs)
            self.db_session.add(instance)
            self.db_session.commit()
            self.db_session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
    
    def find_by_id(self, record_id: str) -> Optional[T]:
        """
        Find a record by its ID.
        
        Args:
            record_id: The ID of the record to find
            
        Returns:
            Optional[T]: Model instance if found, None otherwise
        """
        return self.db_session.query(self.model_class).filter(
            self.model_class.id == record_id
        ).first()
    
    def find_all(self, filters: Optional[Dict[str, Any]] = None, 
                 limit: Optional[int] = None, 
                 offset: Optional[int] = None) -> List[T]:
        """
        Find all records matching the given filters.
        
        Args:
            filters: Dictionary of field names and values to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List[T]: List of model instances
        """
        query = self.db_session.query(self.model_class)
        
        # Apply filters using parameterized queries
        if filters:
            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    query = query.filter(getattr(self.model_class, field) == value)
        
        # Apply pagination
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def update(self, record_id: str, **kwargs) -> Optional[T]:
        """
        Update a record by its ID.
        
        Args:
            record_id: The ID of the record to update
            **kwargs: Field values to update
            
        Returns:
            Optional[T]: Updated model instance if found, None otherwise
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            instance = self.find_by_id(record_id)
            if not instance:
                return None
            
            # Update fields using parameterized approach
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.db_session.commit()
            self.db_session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
    
    def delete(self, record_id: str) -> bool:
        """
        Delete a record by its ID.
        
        Args:
            record_id: The ID of the record to delete
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            instance = self.find_by_id(record_id)
            if not instance:
                return False
            
            self.db_session.delete(instance)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records matching the given filters.
        
        Args:
            filters: Dictionary of field names and values to filter by
            
        Returns:
            int: Number of matching records
        """
        query = self.db_session.query(self.model_class)
        
        # Apply filters using parameterized queries
        if filters:
            for field, value in filters.items():
                if hasattr(self.model_class, field):
                    query = query.filter(getattr(self.model_class, field) == value)
        
        return query.count()
    
    def exists(self, record_id: str) -> bool:
        """
        Check if a record exists by its ID.
        
        Args:
            record_id: The ID of the record to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(self.model_class).filter(
                self.model_class.id == record_id
            ).exists()
        ).scalar()
