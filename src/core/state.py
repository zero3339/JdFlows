"""
Application State Models

Global state models and enumerations.
"""
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CollectionStatus(Enum):
    """Collection status enumeration."""

    IDLE = "idle"
    COLLECTING = "collecting"
    PAUSED = "paused"
    STOPPED = "stopped"


class TaskState(BaseModel):
    """Individual task state model."""

    task_id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Task name")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Task progress (0-100)")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    started_at: Optional[datetime] = Field(default=None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Task metadata")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True


class CollectionState(BaseModel):
    """Collection state model."""

    status: CollectionStatus = Field(default=CollectionStatus.IDLE, description="Collection status")
    total_tasks: int = Field(default=0, ge=0, description="Total number of tasks")
    completed_tasks: int = Field(default=0, ge=0, description="Completed tasks count")
    failed_tasks: int = Field(default=0, ge=0, description="Failed tasks count")
    total_products: int = Field(default=0, ge=0, description="Total products collected")
    started_at: Optional[datetime] = Field(default=None, description="Collection start time")
    current_task_id: Optional[str] = Field(default=None, description="Current active task ID")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True

    @property
    def progress(self) -> float:
        """
        Calculate overall collection progress.

        Returns:
            float: Progress percentage (0-100).
        """
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100.0


class UIState(BaseModel):
    """UI state model."""

    current_page: str = Field(default="home", description="Current page/view")
    sidebar_visible: bool = Field(default=True, description="Sidebar visibility")
    theme: str = Field(default="light", description="Current theme")
    window_width: int = Field(default=1280, ge=800, description="Window width")
    window_height: int = Field(default=800, ge=600, description="Window height")
    last_updated: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )


class GlobalState(BaseModel):
    """Global application state model."""

    collection: CollectionState = Field(
        default_factory=CollectionState, description="Collection state"
    )
    ui: UIState = Field(default_factory=UIState, description="UI state")
    tasks: Dict[str, TaskState] = Field(default_factory=dict, description="Task states")
    session_id: Optional[str] = Field(default=None, description="Current session ID")
    last_updated: datetime = Field(
        default_factory=datetime.now, description="Last state update timestamp"
    )

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True

    def get_task(self, task_id: str) -> Optional[TaskState]:
        """
        Get task state by ID.

        Args:
            task_id: Task identifier.

        Returns:
            Optional[TaskState]: Task state if found, None otherwise.
        """
        return self.tasks.get(task_id)

    def add_task(self, task: TaskState) -> None:
        """
        Add or update a task.

        Args:
            task: Task state to add.
        """
        self.tasks[task.task_id] = task
        self.last_updated = datetime.now()

    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task.

        Args:
            task_id: Task identifier.

        Returns:
            bool: True if task was removed, False if not found.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.last_updated = datetime.now()
            return True
        return False

    def get_active_tasks(self) -> list[TaskState]:
        """
        Get all active (running) tasks.

        Returns:
            list[TaskState]: List of active tasks.
        """
        return [task for task in self.tasks.values() if task.status == "running"]

    def get_completed_tasks(self) -> list[TaskState]:
        """
        Get all completed tasks.

        Returns:
            list[TaskState]: List of completed tasks.
        """
        return [task for task in self.tasks.values() if task.status == TaskStatus.COMPLETED]

    def get_failed_tasks(self) -> list[TaskState]:
        """
        Get all failed tasks.

        Returns:
            list[TaskState]: List of failed tasks.
        """
        return [task for task in self.tasks.values() if task.status == "failed"]
