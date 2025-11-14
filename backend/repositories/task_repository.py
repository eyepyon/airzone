"""
Task repository for managing background task data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.task_queue import TaskQueue, TaskStatus
from repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskQueue]):
    """
    Repository for TaskQueue model operations.
    Provides custom queries for task management and status tracking.
    
    Requirements: 5.3, 5.4, 5.5, 5.6, 10.4
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize TaskRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(TaskQueue, db_session)
    
    def find_by_task_type(self, task_type: str) -> List[TaskQueue]:
        """
        Find all tasks of a specific type.
        
        Args:
            task_type: Task type to filter by
            
        Returns:
            List[TaskQueue]: List of task instances
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.task_type == task_type
        ).order_by(TaskQueue.created_at.desc()).all()
    
    def find_by_status(self, status: TaskStatus) -> List[TaskQueue]:
        """
        Find all tasks with a specific status.
        
        Args:
            status: Task status to filter by
            
        Returns:
            List[TaskQueue]: List of task instances
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.status == status
        ).order_by(TaskQueue.created_at.asc()).all()
    
    def find_pending_tasks(self) -> List[TaskQueue]:
        """
        Find all pending tasks.
        
        Returns:
            List[TaskQueue]: List of pending task instances
        """
        return self.find_by_status(TaskStatus.PENDING)
    
    def find_running_tasks(self) -> List[TaskQueue]:
        """
        Find all running tasks.
        
        Returns:
            List[TaskQueue]: List of running task instances
        """
        return self.find_by_status(TaskStatus.RUNNING)
    
    def find_failed_tasks(self) -> List[TaskQueue]:
        """
        Find all failed tasks.
        
        Returns:
            List[TaskQueue]: List of failed task instances
        """
        return self.find_by_status(TaskStatus.FAILED)
    
    def find_retryable_tasks(self) -> List[TaskQueue]:
        """
        Find all failed tasks that can be retried.
        
        Returns:
            List[TaskQueue]: List of retryable task instances
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.status == TaskStatus.FAILED,
            TaskQueue.retry_count < TaskQueue.max_retries
        ).order_by(TaskQueue.created_at.asc()).all()
    
    def update_status(self, task_id: str, status: TaskStatus, 
                     **kwargs) -> Optional[TaskQueue]:
        """
        Update the status of a task.
        
        Args:
            task_id: Task ID
            status: New task status
            **kwargs: Additional fields to update (result, error_message, etc.)
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        kwargs['status'] = status
        return self.update(task_id, **kwargs)
    
    def increment_retry_count(self, task_id: str) -> Optional[TaskQueue]:
        """
        Increment the retry count for a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        try:
            task = self.find_by_id(task_id)
            if not task:
                return None
            
            new_retry_count = task.retry_count + 1
            return self.update(task_id, retry_count=new_retry_count)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
    
    def mark_as_running(self, task_id: str) -> Optional[TaskQueue]:
        """
        Mark a task as running.
        
        Args:
            task_id: Task ID
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.RUNNING)
    
    def mark_as_completed(self, task_id: str, result: dict = None) -> Optional[TaskQueue]:
        """
        Mark a task as completed with optional result.
        
        Args:
            task_id: Task ID
            result: Task result data
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.COMPLETED, result=result)
    
    def mark_as_failed(self, task_id: str, error_message: str) -> Optional[TaskQueue]:
        """
        Mark a task as failed with error message.
        
        Args:
            task_id: Task ID
            error_message: Error message describing the failure
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.FAILED, error_message=error_message)
    
    def count_by_status(self, status: TaskStatus) -> int:
        """
        Count tasks with a specific status.
        
        Args:
            status: Task status to count
            
        Returns:
            int: Number of tasks with the given status
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.status == status
        ).count()
    
    def count_by_type_and_status(self, task_type: str, status: TaskStatus) -> int:
        """
        Count tasks by type and status.
        
        Args:
            task_type: Task type to filter by
            status: Task status to count
            
        Returns:
            int: Number of tasks matching the criteria
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.task_type == task_type,
            TaskQueue.status == status
        ).count()
