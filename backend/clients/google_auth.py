"""
Google OAuth client for authentication.
Handles Google ID token verification and user information retrieval.

Requirements: 1.1
"""
from typing import Dict, Optional
from google.oauth2 import id_token
from google.auth.transport import requests
import logging


logger = logging.getLogger(__name__)


class GoogleAuthClient:
    """
    Client for Google OAuth authentication.
    Verifies Google ID tokens and retrieves user information.
    """
    
    def __init__(self, client_id: str):
        """
        Initialize GoogleAuthClient with Google OAuth client ID.
        
        Args:
            client_id: Google OAuth client ID
        """
        self.client_id = client_id
        self.request = requests.Request()
    
    def verify_id_token(self, token: str) -> Optional[Dict]:
        """
        Verify a Google ID token and extract user information.
        
        Args:
            token: Google ID token to verify
            
        Returns:
            Optional[Dict]: User information if token is valid, None otherwise
            
        Raises:
            ValueError: If token is invalid or verification fails
            
        Requirements: 1.1 - Google OAuth authentication
        """
        try:
            # Verify the token using Google's library
            idinfo = id_token.verify_oauth2_token(
                token, 
                self.request, 
                self.client_id
            )
            
            # Verify the issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid token issuer')
            
            # Extract user information
            user_info = {
                'google_id': idinfo['sub'],
                'email': idinfo.get('email'),
                'email_verified': idinfo.get('email_verified', False),
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture'),
                'given_name': idinfo.get('given_name'),
                'family_name': idinfo.get('family_name'),
                'locale': idinfo.get('locale')
            }
            
            logger.info(f"Successfully verified Google ID token for user: {user_info['email']}")
            return user_info
            
        except ValueError as e:
            logger.error(f"Failed to verify Google ID token: {str(e)}")
            raise ValueError(f"Invalid Google ID token: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {str(e)}")
            raise ValueError(f"Token verification failed: {str(e)}")
    
    def get_user_info(self, token: str) -> Dict:
        """
        Get user information from a verified Google ID token.
        Convenience method that wraps verify_id_token.
        
        Args:
            token: Google ID token
            
        Returns:
            Dict: User information dictionary
            
        Raises:
            ValueError: If token is invalid
        """
        user_info = self.verify_id_token(token)
        if not user_info:
            raise ValueError("Failed to retrieve user information")
        return user_info
    
    def validate_email_verified(self, token: str) -> bool:
        """
        Check if the email associated with the token is verified.
        
        Args:
            token: Google ID token
            
        Returns:
            bool: True if email is verified, False otherwise
        """
        try:
            user_info = self.verify_id_token(token)
            return user_info.get('email_verified', False) if user_info else False
        except ValueError:
            return False
