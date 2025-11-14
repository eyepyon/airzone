"""
Base model class for SQLAlchemy models.
Provides common functionality and utilities for all models.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


# Create declarative base
Base = declarative_base()


class BaseModel(Base):
    """
    Abstract base model class that provides common fields and methods.
    All models should inherit from this class.
    """
    __abstract__ = True
    
    # Common fields for all models
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self, exclude_fields=None):
        """
        Convert model instance to dictionary.
        
        Args:
            exclude_fields (list): List of field names to exclude from the dictionary
            
        Returns:
            dict: Dictionary representation of the model
        """
        if exclude_fields is None:
            exclude_fields = []
        
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(self, column.name)
                # Convert datetime objects to ISO format strings
                if isinstance(value, datetime):
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value
        
        return result
    
    def __repr__(self):
        """String representation of the model"""
        return f"<{self.__class__.__name__}(id={self.id})>"


def generate_uuid():
    """
    Generate a new UUID string.
    
    Returns:
        str: UUID string in format 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    """
    return str(uuid.uuid4())
