"""
TaskRepository for managing background task queue data access.
Provides methods for task CRUD operations and status management.

Requirements: 10.4
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from models.task_queue import TaskQueue, TaskStatus


class TaskRepository(BaseRepository[TaskQueue]):
    """
    Repository for TaskQueue model.
    Handles task creation, retrieval, and status updates for background processing.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize TaskRepository.
        
        Args:
            db_session: SQLAlchemy database session
        """
        super().__init__(TaskQueue, db_session)
    
    def find_by_status(self, status: TaskStatus, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find tasks by status.
        
        Args:
            status: The task status to filter by
            limit: Maximum number of records to return
            
        Returns:
            List[TaskQueue]: List of tasks with the specified status
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.status == status
        ).order_by(TaskQueue.created_at.asc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def find_by_task_type(self, task_type: str, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find tasks by task type.
        
        Args:
            task_type: The task type to filter by
            limit: Maximum number of records to return
            
        Returns:
            List[TaskQueue]: List of tasks with the specified type
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.task_type == task_type
        ).order_by(TaskQueue.created_at.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def find_pending_tasks(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find all pending tasks that are ready to be processed.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List[TaskQueue]: List of pending tasks
        """
        return self.find_by_status(TaskStatus.PENDING, limit=limit)
    
    def find_failed_tasks_for_retry(self, limit: Optional[int] = None) -> List[TaskQueue]:
        """
        Find failed tasks that can be retried (retry_count < max_retries).
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List[TaskQueue]: List of failed tasks eligible for retry
        """
        query = self.db_session.query(TaskQueue).filter(
            TaskQueue.status == TaskStatus.FAILED,
            TaskQueue.retry_count < TaskQueue.max_retries
        ).order_by(TaskQueue.created_at.asc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
    
    def update_status(self, task_id: str, status: TaskStatus, 
                     result: Optional[Dict[str, Any]] = None,
                     error_message: Optional[str] = None) -> Optional[TaskQueue]:
        """
        Update the status of a task with optional result or error.
        
        Args:
            task_id: The task ID to update
            status: The new status
            result: Optional result data for completed tasks
            error_message: Optional error message for failed tasks
            
        Returns:
            Optional[TaskQueue]: Updated task if found, None otherwise
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
        
        Args:
            task_id: The task ID to update
            
        Returns:
            Optional[TaskQueue]: Updated task if found, None otherwise
        """
        task = self.find_by_id(task_id)
        if task:
            return self.update(task_id, retry_count=task.retry_count + 1)
        return None
    
    def create_task(self, task_type: str, payload: Optional[Dict[str, Any]] = None,
                   max_retries: int = 3) -> TaskQueue:
        """
        Create a new task in the queue.
        
        Args:
            task_type: Type of task to create
            payload: Task input data
            max_retries: Maximum number of retry attempts (default: 3)
            
        Returns:
            TaskQueue: Created task record
        """
        return self.create(
            task_type=task_type,
            payload=payload,
            status=TaskStatus.PENDING,
            retry_count=0,
            max_retries=max_retries
        )
    
    def mark_as_running(self, task_id: str) -> Optional[TaskQueue]:
        """
        Mark a task as running.
        
        Args:
            task_id: The task ID to update
            
        Returns:
            Optional[TaskQueue]: Updated task if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.RUNNING)
    
    def mark_as_completed(self, task_id: str, result: Optional[Dict[str, Any]] = None) -> Optional[TaskQueue]:
        """
        Mark a task as completed with optional result data.
        
        Args:
            task_id: The task ID to update
            result: Optional result data
            
        Returns:
            Optional[TaskQueue]: Updated task if found, None otherwise
        """
        return self.update_status(task_id, TaskStatus.COMPLETED, result=result)
    
    def mark_as_failed(self, task_id: str, error_message: str) -> Optional[TaskQueue]:
        """
        Mark a task as failed with error message.
        
        Args:
            task_id: The task ID to update
            error_message: Error message describing the failure
            
        Returns:
            Optional[TaskQueue]: Updated task if found, None otherwise
        """
        task = self.increment_retry_count(task_id)
        if task:
            return self.update_status(task_id, TaskStatus.FAILED, error_message=error_message)
        return None
