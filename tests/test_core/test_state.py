"""Tests for state models"""
from datetime import datetime
from src.core.state import (
    TaskStatus,
    CollectionStatus,
    TaskState,
    CollectionState,
    UIState,
    GlobalState,
)


class TestTaskStatus:
    """Tests for TaskStatus enumeration"""

    def test_task_status_values(self):
        """Test task status enum values"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.PAUSED.value == "paused"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.CANCELLED.value == "cancelled"


class TestCollectionStatus:
    """Tests for CollectionStatus enumeration"""

    def test_collection_status_values(self):
        """Test collection status enum values"""
        assert CollectionStatus.IDLE.value == "idle"
        assert CollectionStatus.COLLECTING.value == "collecting"
        assert CollectionStatus.PAUSED.value == "paused"
        assert CollectionStatus.STOPPED.value == "stopped"


class TestTaskState:
    """Tests for TaskState model"""

    def test_task_state_creation(self):
        """Test task state creation"""
        task = TaskState(task_id="test-1", name="Test Task")
        assert task.task_id == "test-1"
        assert task.name == "Test Task"
        assert task.status == TaskStatus.PENDING
        assert task.progress == 0.0
        assert isinstance(task.created_at, datetime)
        assert task.started_at is None
        assert task.completed_at is None
        assert task.error_message is None
        assert task.metadata == {}

    def test_task_state_with_values(self):
        """Test task state with custom values"""
        now = datetime.now()
        task = TaskState(
            task_id="test-2",
            name="Task 2",
            status="running",
            progress=50.0,
            started_at=now,
            metadata={"key": "value"},
        )
        assert task.status == TaskStatus.RUNNING
        assert task.progress == 50.0
        assert task.started_at == now
        assert task.metadata == {"key": "value"}


class TestCollectionState:
    """Tests for CollectionState model"""

    def test_collection_state_defaults(self):
        """Test collection state default values"""
        state = CollectionState()
        # Either enum or string depending on Config
        assert state.status == CollectionStatus.IDLE or state.status == "idle"
        assert state.total_tasks == 0
        assert state.completed_tasks == 0
        assert state.failed_tasks == 0
        assert state.total_products == 0
        assert state.started_at is None
        assert state.current_task_id is None

    def test_collection_progress_calculation(self):
        """Test collection progress calculation"""
        state = CollectionState(total_tasks=10, completed_tasks=5)
        assert state.progress == 50.0

        state = CollectionState(total_tasks=0, completed_tasks=0)
        assert state.progress == 0.0

        state = CollectionState(total_tasks=100, completed_tasks=75)
        assert state.progress == 75.0


class TestUIState:
    """Tests for UIState model"""

    def test_ui_state_defaults(self):
        """Test UI state default values"""
        state = UIState()
        assert state.current_page == "home"
        assert state.sidebar_visible is True
        assert state.theme == "light"
        assert state.window_width == 1280
        assert state.window_height == 800
        assert isinstance(state.last_updated, datetime)


class TestGlobalState:
    """Tests for GlobalState model"""

    def test_global_state_initialization(self):
        """Test global state initialization"""
        state = GlobalState()
        assert isinstance(state.collection, CollectionState)
        assert isinstance(state.ui, UIState)
        assert state.tasks == {}
        assert state.session_id is None
        assert isinstance(state.last_updated, datetime)

    def test_add_task(self):
        """Test adding a task"""
        state = GlobalState()
        task = TaskState(task_id="task-1", name="Task 1")
        state.add_task(task)
        assert "task-1" in state.tasks
        assert state.tasks["task-1"].name == "Task 1"

    def test_get_task(self):
        """Test getting a task"""
        state = GlobalState()
        task = TaskState(task_id="task-1", name="Task 1")
        state.add_task(task)

        retrieved = state.get_task("task-1")
        assert retrieved is not None
        assert retrieved.task_id == "task-1"

        not_found = state.get_task("not-exists")
        assert not_found is None

    def test_remove_task(self):
        """Test removing a task"""
        state = GlobalState()
        task = TaskState(task_id="task-1", name="Task 1")
        state.add_task(task)

        removed = state.remove_task("task-1")
        assert removed is True
        assert "task-1" not in state.tasks

        not_removed = state.remove_task("not-exists")
        assert not_removed is False

    def test_get_active_tasks(self):
        """Test getting active tasks"""
        state = GlobalState()
        state.add_task(TaskState(task_id="t1", name="T1", status="running"))
        state.add_task(TaskState(task_id="t2", name="T2", status="pending"))
        state.add_task(TaskState(task_id="t3", name="T3", status="running"))

        active = state.get_active_tasks()
        assert len(active) == 2
        assert all(t.status == "running" for t in active)

    def test_get_completed_tasks(self):
        """Test getting completed tasks"""
        state = GlobalState()
        state.add_task(TaskState(task_id="t1", name="T1", status="completed"))
        state.add_task(TaskState(task_id="t2", name="T2", status="running"))
        state.add_task(TaskState(task_id="t3", name="T3", status="completed"))

        completed = state.get_completed_tasks()
        assert len(completed) == 2
        assert all(t.status == "completed" for t in completed)

    def test_get_failed_tasks(self):
        """Test getting failed tasks"""
        state = GlobalState()
        state.add_task(TaskState(task_id="t1", name="T1", status="failed"))
        state.add_task(TaskState(task_id="t2", name="T2", status="running"))
        state.add_task(TaskState(task_id="t3", name="T3", status="failed"))

        failed = state.get_failed_tasks()
        assert len(failed) == 2
        assert all(t.status == "failed" for t in failed)
