"""
User repository for managing user data access.
Provides custom queries for finding users by Google ID and email.

Requirements: 1.2, 1.3
"""
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model with custom query methods.
    Handles user authentication and account management operations.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize UserRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(User, db_session)
    
    def find_by_google_id(self, google_id: str) -> Optional[User]:
        """
        Find a user by their Google OAuth ID.
        Used during Google authentication to check if user exists.
        
        Args:
            google_id: Google OAuth user ID
            
        Returns:
            Optional[User]: User instance if found, None otherwise
            
        Requirements: 1.2 - User authentication via Google OAuth
        """
        return self.db_session.query(User).filter(
            User.google_id == google_id
        ).first()
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by their email address.
        Used for user lookup and duplicate email prevention.
        
        Args:
            email: User's email address
            
        Returns:
            Optional[User]: User instance if found, None otherwise
            
        Requirements: 1.2 - User account management
        """
        return self.db_session.query(User).filter(
            User.email == email
        ).first()
    
    def create_user(self, email: str, google_id: str, name: str) -> User:
        """
        Create a new user with Google OAuth credentials.
        
        Args:
            email: User's email address
            google_id: Google OAuth user ID
            name: User's display name
            
        Returns:
            User: Created user instance
            
        Requirements: 1.2 - Create new user record on first login
        """
        return self.create(
            email=email,
            google_id=google_id,
            name=name
        )
    
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
            google_id: Google OAuth user ID to check
            
        Returns:
            bool: True if Google ID exists, False otherwise
        """
        return self.db_session.query(
            self.db_session.query(User).filter(
                User.google_id == google_id
            ).exists()
        ).scalar()
