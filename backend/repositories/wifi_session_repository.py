"""
WiFiSession repository for managing WiFi session data access.
Provides custom queries for finding sessions by user, MAC address, and status.

Requirements: 2.1, 2.2, 2.3, 2.4
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.wifi_session import WiFiSession
from repositories.base import BaseRepository


class WiFiSessionRepository(BaseRepository[WiFiSession]):
    """
    Repository for WiFiSession model with custom query methods.
    Handles WiFi captive portal session tracking and management.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize WiFiSessionRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(WiFiSession, db_session)
    
    def create_session(
        self,
        user_id: Optional[str],
        mac_address: Optional[str],
        ip_address: Optional[str],
        connected_at: Optional[datetime] = None
    ) -> WiFiSession:
        """
        Create a new WiFi session record.
        
        Args:
            user_id: User ID (optional, can be None for unauthenticated sessions)
            mac_address: Device MAC address
            ip_address: Device IP address
            connected_at: Connection timestamp (defaults to current time)
            
        Returns:
            WiFiSession: Created session instance
            
        Requirements: 2.2 - Create WiFi session record
        """
        if connected_at is None:
            connected_at = datetime.utcnow()
        
        return self.create(
            user_id=user_id,
            mac_address=mac_address,
            ip_address=ip_address,
            connected_at=connected_at
        )
    
    def find_by_user(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[WiFiSession]:
        """
        Find all WiFi sessions for a specific user.
        Returns sessions ordered by connection time (most recent first).
        
        Args:
            user_id: User ID to search for
            limit: Maximum number of sessions to return
            
        Returns:
            List[WiFiSession]: List of session instances
            
        Requirements: 2.4 - Track WiFi session history
        """
        query = self.db_session.query(WiFiSession).filter(
            WiFiSession.user_id == user_id
        ).order_by(desc(WiFiSession.connected_at))
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_mac_address(
        self,
        mac_address: str,
        limit: Optional[int] = None
    ) -> List[WiFiSession]:
        """
        Find all WiFi sessions for a specific MAC address.
        Useful for tracking device connection history.
        
        Args:
            mac_address: MAC address to search for
            limit: Maximum number of sessions to return
            
        Returns:
            List[WiFiSession]: List of session instances
        """
        query = self.db_session.query(WiFiSession).filter(
            WiFiSession.mac_address == mac_address
        ).order_by(desc(WiFiSession.connected_at))
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def find_active_sessions(
        self,
        user_id: Optional[str] = None
    ) -> List[WiFiSession]:
        """
        Find all active WiFi sessions (not disconnected).
        Optionally filter by user ID.
        
        Args:
            user_id: Optional user ID to filter by
            
        Returns:
            List[WiFiSession]: List of active session instances
        """
        query = self.db_session.query(WiFiSession).filter(
            WiFiSession.disconnected_at.is_(None)
        )
        
        if user_id:
            query = query.filter(WiFiSession.user_id == user_id)
        
        return query.order_by(desc(WiFiSession.connected_at)).all()
    
    def disconnect_session(
        self,
        session_id: str,
        disconnected_at: Optional[datetime] = None
    ) -> Optional[WiFiSession]:
        """
        Mark a WiFi session as disconnected.
        
        Args:
            session_id: Session ID to disconnect
            disconnected_at: Disconnection timestamp (defaults to current time)
            
        Returns:
            Optional[WiFiSession]: Updated session instance if found, None otherwise
        """
        if disconnected_at is None:
            disconnected_at = datetime.utcnow()
        
        return self.update(session_id, disconnected_at=disconnected_at)
    
    def get_session_count_by_user(self, user_id: str) -> int:
        """
        Get the total number of WiFi sessions for a user.
        
        Args:
            user_id: User ID to count sessions for
            
        Returns:
            int: Number of sessions
        """
        return self.count({'user_id': user_id})
    
    def get_recent_session_by_mac(
        self,
        mac_address: str
    ) -> Optional[WiFiSession]:
        """
        Get the most recent WiFi session for a MAC address.
        
        Args:
            mac_address: MAC address to search for
            
        Returns:
            Optional[WiFiSession]: Most recent session if found, None otherwise
        """
        return self.db_session.query(WiFiSession).filter(
            WiFiSession.mac_address == mac_address
        ).order_by(desc(WiFiSession.connected_at)).first()
