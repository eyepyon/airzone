"""
Authentication Service for handling user authentication and JWT token management.
Provides Google OAuth authentication flow and JWT token generation/verification.

Requirements: 1.1, 1.4, 1.5, 6.1
"""
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta
import jwt
import logging
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from repositories.wallet_repository import WalletRepository
from clients.google_auth import GoogleAuthClient


logger = logging.getLogger(__name__)


class AuthService:
    """
    Service for authentication operations.
    Handles Google OAuth authentication, JWT token generation and verification.
    """
    
    def __init__(
        self,
        db_session: Session,
        google_client: GoogleAuthClient,
        jwt_secret: str,
        jwt_access_expires: int = 3600,
        jwt_refresh_expires: int = 2592000
    ):
        """
        Initialize AuthService.
        
        Args:
            db_session: SQLAlchemy database session
            google_client: Google OAuth client
            jwt_secret: Secret key for JWT signing
            jwt_access_expires: Access token expiration in seconds (default: 1 hour)
            jwt_refresh_expires: Refresh token expiration in seconds (default: 30 days)
        """
        self.db_session = db_session
        self.user_repo = UserRepository(db_session)
        self.wallet_repo = WalletRepository(db_session)
        self.google_client = google_client
        self.jwt_secret = jwt_secret
        self.jwt_access_expires = jwt_access_expires
        self.jwt_refresh_expires = jwt_refresh_expires
    
    def authenticate_google(self, id_token: str) -> Tuple[Dict, str, str]:
        """
        Authenticate user with Google OAuth ID token.
        Creates new user if first login, returns existing user otherwise.
        
        Args:
            id_token: Google OAuth ID token
            
        Returns:
            Tuple[Dict, str, str]: (user_dict, access_token, refresh_token)
            
        Raises:
            ValueError: If token is invalid or authentication fails
            
        Requirements:
            - 1.1: Google OAuth authentication
            - 1.4: JWT access token generation (1 hour expiration)
            - 1.5: JWT refresh token generation (30 days expiration)
        """
        try:
            # Verify Google ID token and get user info
            user_info = self.google_client.verify_id_token(id_token)
            
            if not user_info:
                raise ValueError("Failed to verify Google ID token")
            
            # Check if email is verified
            if not user_info.get('email_verified', False):
                raise ValueError("Email not verified")
            
            google_id = user_info['google_id']
            email = user_info['email']
            name = user_info.get('name', email.split('@')[0])
            
            # Find or create user
            user = self.user_repo.find_by_google_id(google_id)
            
            if not user:
                # Create new user
                logger.info(f"Creating new user for Google ID: {google_id}")
                user = self.user_repo.create_user(
                    email=email,
                    google_id=google_id,
                    name=name
                )
                self.db_session.commit()
                logger.info(f"Created new user: {user.id}")
            else:
                logger.info(f"Existing user authenticated: {user.id}")
            
            # Generate JWT tokens
            access_token = self.create_access_token(user.id)
            refresh_token = self.create_refresh_token(user.id)
            
            return (user.to_dict(), access_token, refresh_token)
            
        except ValueError as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            self.db_session.rollback()
            raise ValueError(f"Authentication failed: {str(e)}")
    
    def create_access_token(self, user_id: str) -> str:
        """
        Create JWT access token for user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            str: JWT access token
            
        Requirements: 1.4 - JWT access token with 1 hour expiration
        """
        payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_access_expires),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        logger.info(f"Created access token for user: {user_id}")
        
        return token
    
    def create_refresh_token(self, user_id: str) -> str:
        """
        Create JWT refresh token for user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            str: JWT refresh token
            
        Requirements: 1.5 - JWT refresh token with 30 days expiration
        """
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_refresh_expires),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        logger.info(f"Created refresh token for user: {user_id}")
        
        return token
    
    def verify_access_token(self, token: str) -> Dict:
        """
        Verify JWT access token and extract payload.
        
        Args:
            token: JWT access token
            
        Returns:
            Dict: Token payload with user_id
            
        Raises:
            ValueError: If token is invalid or expired
            
        Requirements: 6.1 - JWT token verification
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Verify token type
            if payload.get('type') != 'access':
                raise ValueError("Invalid token type")
            
            logger.info(f"Verified access token for user: {payload['user_id']}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Access token expired")
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid access token: {str(e)}")
            raise ValueError("Invalid token")
    
    def verify_refresh_token(self, token: str) -> Dict:
        """
        Verify JWT refresh token and extract payload.
        
        Args:
            token: JWT refresh token
            
        Returns:
            Dict: Token payload with user_id
            
        Raises:
            ValueError: If token is invalid or expired
            
        Requirements: 1.5 - Refresh token verification
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Verify token type
            if payload.get('type') != 'refresh':
                raise ValueError("Invalid token type")
            
            logger.info(f"Verified refresh token for user: {payload['user_id']}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Refresh token expired")
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid refresh token: {str(e)}")
            raise ValueError("Invalid token")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Generate new access token using refresh token.
        
        Args:
            refresh_token: JWT refresh token
            
        Returns:
            str: New JWT access token
            
        Raises:
            ValueError: If refresh token is invalid
            
        Requirements: 1.5 - Token refresh functionality
        """
        try:
            # Verify refresh token
            payload = self.verify_refresh_token(refresh_token)
            user_id = payload['user_id']
            
            # Verify user still exists
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Generate new access token
            access_token = self.create_access_token(user_id)
            logger.info(f"Refreshed access token for user: {user_id}")
            
            return access_token
            
        except ValueError as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise
    
    def get_current_user(self, access_token: str) -> Optional[Dict]:
        """
        Get current user information from access token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            Optional[Dict]: User information or None if invalid
            
        Requirements: 6.1 - User authentication verification
        """
        try:
            # Verify token
            payload = self.verify_access_token(access_token)
            user_id = payload['user_id']
            
            # Get user from database
            user = self.user_repo.find_by_id(user_id)
            if not user:
                logger.warning(f"User not found for token: {user_id}")
                return None
            
            return user.to_dict()
            
        except ValueError as e:
            logger.warning(f"Failed to get current user: {str(e)}")
            return None
    
    def validate_token(self, token: str) -> bool:
        """
        Validate if a token is valid (not expired and properly signed).
        
        Args:
            token: JWT token to validate
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            self.verify_access_token(token)
            return True
        except ValueError:
            return False
