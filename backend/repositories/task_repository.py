"""
Task Queue repository for managing background task data access.
Provides custom queries for task management and status updates.

Requirements: 10.4
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.task_queue import TaskQueue, TaskStatus
from repositories.base import BaseRepository


class TaskRepository(BaseRepository[TaskQueue]):
    """
    Repository for TaskQueue model with custom query methods.
    Handles background task tracking, status updates, and retry management.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize TaskRepository with database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(TaskQueue, db_session)
    
    def create_task(self, task_type: str, payload: Optional[Dict[str, Any]] = None,
                   max_retries: int = 3) -> TaskQueue:
        """
        Create a new task in the queue.
        
        Args:
            task_type: Type of task (e.g., 'nft_mint', 'email_send')
            payload: Task input data as dictionary
            max_retries: Maximum number of retry attempts
            
        Returns:
            TaskQueue: Created task instance
            
        Requirements: 10.4 - Task queue management
        """
        return self.create(
            task_type=task_type,
            payload=payload,
            status=TaskStatus.PENDING,
            retry_count=0,
            max_retries=max_retries
        )
    
    def find_by_status(self, status: TaskStatus, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find all tasks with a specific status.
        Used for task processing and monitoring.
        
        Args:
            status: Task status to filter by
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of tasks with the specified status
            
        Requirements: 10.4 - Task status tracking
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.status == status
        ).order_by(TaskQueue.created_at.asc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_task_type(self, task_type: str, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find all tasks of a specific type.
        Used for task type specific processing.
        
        Args:
            task_type: Task type to filter by
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of tasks with the specified type
            
        Requirements: 10.4 - Task type filtering
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.task_type == task_type
        ).order_by(TaskQueue.created_at.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def update_status(self, task_id: str, status: TaskStatus, 
                     result: Optional[Dict[str, Any]] = None,
                     error_message: Optional[str] = None) -> Optional[TaskQueue]:
        """
        Update the status of a task with optional result or error.
        Used during task execution to track progress and outcomes.
        
        Args:
            task_id: Task's ID
            status: New task status
            result: Task result data (for completed tasks)
            error_message: Error message (for failed tasks)
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
            
        Requirements: 10.4 - Task status updates during execution
        """
        update_data = {'status': status}
        
        if result is not None:
            update_data['result'] = result
        
        if error_message is not None:
            update_data['error_message'] = error_message
        
        return self.update(task_id, **update_data)
    
    def increment_retry_count(self, task_id: str) -> Optional[TaskQueue]:
        """
        Increment the retry count for a task.
        Used when a task fails and needs to be retried.
        
        Args:
            task_id: Task's ID
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
            
        Requirements: 10.4 - Task retry management
        """
        task = self.find_by_id(task_id)
        if task:
            return self.update(task_id, retry_count=task.retry_count + 1)
        return None
    
    def can_retry(self, task_id: str) -> bool:
        """
        Check if a task can be retried based on retry count.
        
        Args:
            task_id: Task's ID
            
        Returns:
            bool: True if task can be retried, False otherwise
            
        Requirements: 10.4 - Retry limit enforcement
        """
        task = self.find_by_id(task_id)
        if task:
            return task.retry_count < task.max_retries
        return False
    
    def get_pending_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Get all pending tasks ready for processing.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of pending tasks
            
        Requirements: 10.4 - Pending task retrieval
        """
        return self.find_by_status(TaskStatus.PENDING, limit=limit)
    
    def find_pending_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Alias for get_pending_tasks for backward compatibility.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of pending tasks
        """
        return self.get_pending_tasks(limit=limit)
    
    def find_running_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Get all running tasks.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of running tasks
        """
        return self.find_by_status(TaskStatus.RUNNING, limit=limit)
    
    def find_failed_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Get all failed tasks.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of failed tasks
        """
        return self.find_by_status(TaskStatus.FAILED, limit=limit)
    
    def get_failed_retryable_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Get all failed tasks that can still be retried.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            List[TaskQueue]: List of retryable failed tasks
            
        Requirements: 10.4 - Failed task retry management
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.status == TaskStatus.FAILED,
            TaskQueue.retry_count < TaskQueue.max_retries
        ).order_by(TaskQueue.created_at.asc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def count_by_status(self, status: TaskStatus) -> int:
        """
        Count tasks with a specific status.
        
        Args:
            status: Task status to count
            
        Returns:
            int: Number of tasks with the status
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.status == status
        ).count()
    
    def count_by_task_type(self, task_type: str) -> int:
        """
        Count tasks of a specific type.
        
        Args:
            task_type: Task type to count
            
        Returns:
            int: Number of tasks of the type
        """
        return self.db_session.query(TaskQueue).filter(
            TaskQueue.task_type == task_type
        ).count()
    
    def mark_as_running(self, task_id: str) -> Optional[TaskQueue]:
        """
        Mark a task as running.
        
        Args:
            task_id: Task's ID
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.RUNNING)
    
    def mark_as_completed(self, task_id: str, result: Optional[Dict[str, Any]] = None) -> Optional[TaskQueue]:
        """
        Mark a task as completed with optional result.
        
        Args:
            task_id: Task's ID
            result: Task result data
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.COMPLETED, result=result)
    
    def mark_as_failed(self, task_id: str, error_message: str) -> Optional[TaskQueue]:
        """
        Mark a task as failed with error message.
        
        Args:
            task_id: Task's ID
            error_message: Error message describing the failure
            
        Returns:
            Optional[TaskQueue]: Updated task instance if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.FAILED, error_message=error_message)
