"""
User repository for managing user data access.
"""
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    Provides custom queries for user lookup by email and Google ID.
    
    Requirements: 1.2, 1.3
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize UserRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(User, db_session)
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        return self.db_session.query(User).filter(
            User.email == email
        ).first()
    
    def find_by_google_id(self, google_id: str) -> Optional[User]:
        """
        Find a user by Google OAuth ID.
        
        Args:
            google_id: User's Google OAuth ID
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        return self.db_session.query(User).filter(
            User.google_id == google_id
        ).first()
    
    def email_exists(self, email: str) -> bool:
        """
        Check if an email address is already registered.
        
        Args:
            email: Email address to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(User).filter(
                User.email == email
            ).exists()
        ).scalar()
    
    def google_id_exists(self, google_id: str) -> bool:
        """
        Check if a Google ID is already registered.
        
        Args:
            google_id: Google OAuth ID to check
            
        Returns:
            bool: True if Google ID exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(User).filter(
                User.google_id == google_id
            ).exists()
        ).scalar()
