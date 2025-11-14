"""
Task Manager for handling background tasks using ThreadPoolExecutor.
Provides asynchronous task execution with status tracking.
"""
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any, Optional, Dict
import uuid
import logging
from functools import wraps
from sqlalchemy.orm import Session
from repositories.task_repository import TaskRepository
from models.task_queue import TaskStatus


logger = logging.getLogger(__name__)


class TaskManager:
    """
    Task Manager for executing background tasks asynchronously.
    Uses ThreadPoolExecutor for concurrent task execution and tracks
    task status in the database.
    
    Requirements: 10.1, 10.2, 10.3, 10.4
    """
    
    def __init__(self, db_session: Session, max_workers: int = 5):
        """
        Initialize TaskManager with database session and thread pool.
        
        Args:
            db_session: SQLAlchemy database session
            max_workers: Maximum number of worker threads (default: 5)
        """
        self.db_session = db_session
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_repo = TaskRepository(db_session)
        self._futures: Dict[str, Future] = {}
        logger.info(f"TaskManager initialized with {max_workers} workers")
    
    def submit_task(
        self,
        task_type: str,
        func: Callable,
        *args,
        payload: Optional[dict] = None,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Submit a task for asynchronous execution.
        
        Args:
            task_type: Type of task (e.g., 'nft_mint', 'payment_process')
            func: Function to execute
            *args: Positional arguments for the function
            payload: Optional payload data to store with the task
            max_retries: Maximum number of retry attempts (default: 3)
            **kwargs: Keyword arguments for the function
            
        Returns:
            str: Task ID for tracking
        """
        # Create task record in database
        task_id = str(uuid.uuid4())
        task = self.task_repo.create(
            id=task_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            payload=payload,
            max_retries=max_retries
        )
        
        logger.info(f"Task {task_id} ({task_type}) submitted to queue")
        
        # Submit task to thread pool
        future = self.executor.submit(
            self._execute_task,
            task_id,
            func,
            *args,
            **kwargs
        )
        
        # Store future for tracking
        self._futures[task_id] = future
        
        return task_id
    
    def _execute_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute a task and update its status in the database.
        
        Args:
            task_id: Task ID
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Any: Result of the function execution
            
        Raises:
            Exception: If task execution fails
        """
        try:
            # Mark task as running
            self.task_repo.mark_as_running(task_id)
            logger.info(f"Task {task_id} started execution")
            
            # Execute the function
            result = func(*args, **kwargs)
            
            # Mark task as completed
            result_data = result if isinstance(result, dict) else {'result': str(result)}
            self.task_repo.mark_as_completed(task_id, result=result_data)
            logger.info(f"Task {task_id} completed successfully")
            
            # Clean up future
            if task_id in self._futures:
                del self._futures[task_id]
            
            return result
            
        except Exception as e:
            # Mark task as failed
            error_message = str(e)
            self.task_repo.mark_as_failed(task_id, error_message=error_message)
            logger.error(f"Task {task_id} failed: {error_message}", exc_info=True)
            
            # Clean up future
            if task_id in self._futures:
                del self._futures[task_id]
            
            raise
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current status of a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Optional[Dict[str, Any]]: Task status information or None if not found
        """
        task = self.task_repo.find_by_id(task_id)
        if not task:
            return None
        
        return task.to_dict()
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Attempt to cancel a pending or running task.
        
        Args:
            task_id: Task ID
            
        Returns:
            bool: True if task was cancelled, False otherwise
        """
        if task_id in self._futures:
            future = self._futures[task_id]
            if future.cancel():
                self.task_repo.mark_as_failed(
                    task_id,
                    error_message="Task cancelled by user"
                )
                del self._futures[task_id]
                logger.info(f"Task {task_id} cancelled")
                return True
        
        return False
    
    def get_pending_tasks(self) -> list:
        """
        Get all pending tasks.
        
        Returns:
            list: List of pending task dictionaries
        """
        tasks = self.task_repo.find_pending_tasks()
        return [task.to_dict() for task in tasks]
    
    def get_running_tasks(self) -> list:
        """
        Get all running tasks.
        
        Returns:
            list: List of running task dictionaries
        """
        tasks = self.task_repo.find_running_tasks()
        return [task.to_dict() for task in tasks]
    
    def get_failed_tasks(self) -> list:
        """
        Get all failed tasks.
        
        Returns:
            list: List of failed task dictionaries
        """
        tasks = self.task_repo.find_failed_tasks()
        return [task.to_dict() for task in tasks]
    
    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the task manager and wait for tasks to complete.
        
        Args:
            wait: If True, wait for all tasks to complete before shutting down
        """
        logger.info("Shutting down TaskManager")
        self.executor.shutdown(wait=wait)
        self._futures.clear()
        logger.info("TaskManager shutdown complete")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown(wait=True)
