"""
WiFiSession model for tracking WiFi captive portal sessions.
"""
from sqlalchemy import Column, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from models.base import BaseModel


class WiFiSession(BaseModel):
    """
    WiFiSession model representing a WiFi connection session.
    Tracks user connections through the OpenNDS captive portal.
    """
    __tablename__ = 'wifi_sessions'
    
    # WiFiSession fields
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    mac_address = Column(String(17), nullable=True)  # MAC address format: XX:XX:XX:XX:XX:XX
    ip_address = Column(String(45), nullable=True)  # IPv4 (15 chars) or IPv6 (45 chars)
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
        return f"<WiFiSession(id={self.id}, user_id={self.user_id}, mac_address={self.mac_address}, connected_at={self.connected_at})>"
