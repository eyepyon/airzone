"""
WiFi Session model for tracking captive portal connections.
"""
from sqlalchemy import Column, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel


class WiFiSession(BaseModel):
    """
    WiFi Session model representing a user's WiFi connection session.
    Tracks when users connect to the captive portal and their session details.
    """
    __tablename__ = 'wifi_sessions'
    
    # WiFi Session fields
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    mac_address = Column(String(17), nullable=True)  # Format: XX:XX:XX:XX:XX:XX
    ip_address = Column(String(45), nullable=True)  # Supports both IPv4 and IPv6
    connected_at = Column(DateTime, nullable=False)
    disconnected_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='wifi_sessions')
    
    # Indexes
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_mac_address', 'mac_address'),
    )
    
    def __repr__(self):
        return f"<WiFiSession(id={self.id}, user_id={self.user_id}, mac_address={self.mac_address})>"
