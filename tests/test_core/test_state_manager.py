"""Tests for state manager"""
import pytest
from src.core.state import TaskState, TaskStatus, CollectionStatus
from src.core.state_manager import StateManager
from src.core.exceptions import StateError


class TestStateManager:
    """Tests for StateManager"""

    def test_initialization(self):
        """Test state manager initialization"""
        manager = StateManager()
        state = manager.get_state()
        # Enum not converted via model_copy
        assert state.collection.status == CollectionStatus.IDLE or state.collection.status == "idle"
        assert state.ui.theme == "light"
        assert state.tasks == {}

    def test_get_collection_state(self):
        """Test getting collection state"""
        manager = StateManager()
        collection = manager.get_collection_state()
        # Enum not converted when getting via model_copy
        assert collection.status == CollectionStatus.IDLE or collection.status == "idle"
        assert collection.total_tasks == 0

    def test_update_collection_state(self):
        """Test updating collection state"""
        manager = StateManager()
        manager.update_collection_state(total_tasks=10, completed_tasks=5)

        collection = manager.get_collection_state()
        assert collection.total_tasks == 10
        assert collection.completed_tasks == 5
        assert collection.progress == 50.0

    def test_get_ui_state(self):
        """Test getting UI state"""
        manager = StateManager()
        ui = manager.get_ui_state()
        assert ui.current_page == "home"
        assert ui.theme == "light"

    def test_update_ui_state(self):
        """Test updating UI state"""
        manager = StateManager()
        manager.update_ui_state(current_page="settings", theme="dark")

        ui = manager.get_ui_state()
        assert ui.current_page == "settings"
        assert ui.theme == "dark"

    def test_add_task(self):
        """Test adding a task"""
        manager = StateManager()
        task = TaskState(task_id="task-1", name="Task 1")
        manager.add_task(task)

        retrieved = manager.get_task("task-1")
        assert retrieved is not None
        assert retrieved.task_id == "task-1"
        assert retrieved.name == "Task 1"

    def test_get_task_not_found(self):
        """Test getting non-existent task"""
        manager = StateManager()
        task = manager.get_task("not-exists")
        assert task is None

    def test_update_task(self):
        """Test updating a task"""
        manager = StateManager()
        task = TaskState(task_id="task-1", name="Task 1")
        manager.add_task(task)

        manager.update_task("task-1", status="running", progress=50.0)

        updated = manager.get_task("task-1")
        assert updated.status == "running"
        assert updated.progress == 50.0

    def test_update_task_not_found(self):
        """Test updating non-existent task"""
        manager = StateManager()
        with pytest.raises(StateError):
            manager.update_task("not-exists", status=TaskStatus.RUNNING)

    def test_remove_task(self):
        """Test removing a task"""
        manager = StateManager()
        task = TaskState(task_id="task-1", name="Task 1")
        manager.add_task(task)

        removed = manager.remove_task("task-1")
        assert removed is True

        retrieved = manager.get_task("task-1")
        assert retrieved is None

    def test_remove_task_not_found(self):
        """Test removing non-existent task"""
        manager = StateManager()
        removed = manager.remove_task("not-exists")
        assert removed is False

    def test_get_all_tasks(self):
        """Test getting all tasks"""
        manager = StateManager()
        manager.add_task(TaskState(task_id="t1", name="T1"))
        manager.add_task(TaskState(task_id="t2", name="T2"))
        manager.add_task(TaskState(task_id="t3", name="T3"))

        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 3

    def test_clear_tasks(self):
        """Test clearing all tasks"""
        manager = StateManager()
        manager.add_task(TaskState(task_id="t1", name="T1"))
        manager.add_task(TaskState(task_id="t2", name="T2"))

        manager.clear_tasks()

        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 0

    def test_observer_registration(self):
        """Test observer registration and notification"""
        manager = StateManager()
        callback_data = []

        def callback(key, old_value, new_value):
            callback_data.append((key, old_value, new_value))

        manager.register_observer("collection", callback)
        manager.update_collection_state(total_tasks=5)

        assert len(callback_data) == 1
        assert callback_data[0][0] == "collection"

    def test_observer_unregistration(self):
        """Test observer unregistration"""
        manager = StateManager()
        callback_data = []

        def callback(key, old_value, new_value):
            callback_data.append((key, old_value, new_value))

        manager.register_observer("collection", callback)
        manager.unregister_observer("collection", callback)

        manager.update_collection_state(total_tasks=5)
        assert len(callback_data) == 0

    def test_reset(self):
        """Test state manager reset"""
        manager = StateManager()
        manager.add_task(TaskState(task_id="t1", name="T1"))
        manager.update_collection_state(total_tasks=10)

        manager.reset()

        state = manager.get_state()
        assert state.tasks == {}
        assert state.collection.total_tasks == 0

    def test_export_import_state(self):
        """Test state export and import"""
        manager = StateManager()
        manager.add_task(TaskState(task_id="t1", name="T1"))
        manager.update_collection_state(total_tasks=5)

        exported = manager.export_state()
        assert "tasks" in exported
        assert "collection" in exported

        new_manager = StateManager()
        new_manager.import_state(exported)

        imported_state = new_manager.get_state()
        assert imported_state.collection.total_tasks == 5
        assert "t1" in imported_state.tasks
