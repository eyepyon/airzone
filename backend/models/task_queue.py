"""
Task Queue model for managing background tasks.
"""
from sqlalchemy import Column, String, Integer, Text, Enum, Index, JSON
from models.base import BaseModel
import enum


class TaskStatus(enum.Enum):
    """Enum for task status"""
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TaskQueue(BaseModel):
    """
    Task Queue model representing a background task.
    Tracks asynchronous tasks such as NFT minting operations.
    """
    __tablename__ = 'task_queue'
    
    # Task Queue fields
    task_type = Column(String(50), nullable=False)
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )
    payload = Column(JSON, nullable=True)  # Task input data
    result = Column(JSON, nullable=True)  # Task output data
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_task_type', 'task_type'),
    )
    
    def to_dict(self, exclude_fields=None):
        """
        Convert task to dictionary.
        
        Args:
            exclude_fields (list): Fields to exclude
            
        Returns:
            dict: Task data dictionary
        """
        result = super().to_dict(exclude_fields=exclude_fields)
        
        # Convert enum to string value
        if 'status' in result and isinstance(result['status'], TaskStatus):
            result['status'] = result['status'].value
        
        return result
    
    def __repr__(self):
        return f"<TaskQueue(id={self.id}, task_type={self.task_type}, status={self.status.value})>"
