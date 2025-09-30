"""
State Manager

Global application state management with observer pattern.
"""
from typing import Callable, Optional, Any, Dict
from threading import RLock
from loguru import logger

from src.core.state import GlobalState, TaskState, CollectionState, UIState
from src.core.exceptions import StateError


StateChangeCallback = Callable[[str, Any, Any], None]


class StateManager:
    """
    Global state manager with observer pattern.

    Provides thread-safe state management with change notifications.
    """

    def __init__(self) -> None:
        """Initialize the state manager."""
        self._state = GlobalState()
        self._lock = RLock()
        self._observers: Dict[str, list[StateChangeCallback]] = {}

        logger.info("State manager initialized")

    def get_state(self) -> GlobalState:
        """
        Get the current global state.

        Returns:
            GlobalState: Current state (read-only copy).
        """
        with self._lock:
            return self._state.model_copy(deep=True)

    def get_collection_state(self) -> CollectionState:
        """
        Get collection state.

        Returns:
            CollectionState: Collection state copy.
        """
        with self._lock:
            return self._state.collection.model_copy(deep=True)

    def update_collection_state(self, **kwargs) -> None:
        """
        Update collection state fields.

        Args:
            **kwargs: Fields to update.
        """
        with self._lock:
            old_state = self._state.collection.model_copy(deep=True)

            for key, value in kwargs.items():
                if hasattr(self._state.collection, key):
                    setattr(self._state.collection, key, value)
                else:
                    raise StateError(f"Invalid collection state field: {key}")

            new_state = self._state.collection.model_copy(deep=True)
            self._notify_observers("collection", old_state, new_state)

        logger.debug(f"Collection state updated: {kwargs}")

    def get_ui_state(self) -> UIState:
        """
        Get UI state.

        Returns:
            UIState: UI state copy.
        """
        with self._lock:
            return self._state.ui.model_copy(deep=True)

    def update_ui_state(self, **kwargs) -> None:
        """
        Update UI state fields.

        Args:
            **kwargs: Fields to update.
        """
        with self._lock:
            old_state = self._state.ui.model_copy(deep=True)

            for key, value in kwargs.items():
                if hasattr(self._state.ui, key):
                    setattr(self._state.ui, key, value)
                else:
                    raise StateError(f"Invalid UI state field: {key}")

            new_state = self._state.ui.model_copy(deep=True)
            self._notify_observers("ui", old_state, new_state)

        logger.debug(f"UI state updated: {kwargs}")

    def get_task(self, task_id: str) -> Optional[TaskState]:
        """
        Get task state by ID.

        Args:
            task_id: Task identifier.

        Returns:
            Optional[TaskState]: Task state if found.
        """
        with self._lock:
            task = self._state.get_task(task_id)
            return task.model_copy(deep=True) if task else None

    def add_task(self, task: TaskState) -> None:
        """
        Add or update a task.

        Args:
            task: Task state.
        """
        with self._lock:
            old_task = self._state.get_task(task.task_id)
            self._state.add_task(task)
            new_task = self._state.get_task(task.task_id)

            if old_task:
                self._notify_observers(f"task.{task.task_id}", old_task, new_task)
            else:
                self._notify_observers("tasks", None, new_task)

        logger.debug(f"Task added/updated: {task.task_id}")

    def update_task(self, task_id: str, **kwargs) -> None:
        """
        Update task fields.

        Args:
            task_id: Task identifier.
            **kwargs: Fields to update.

        Raises:
            StateError: If task not found.
        """
        with self._lock:
            task = self._state.get_task(task_id)
            if not task:
                raise StateError(f"Task not found: {task_id}")

            old_task = task.model_copy(deep=True)

            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
                else:
                    raise StateError(f"Invalid task field: {key}")

            new_task = task.model_copy(deep=True)
            self._notify_observers(f"task.{task_id}", old_task, new_task)

        logger.debug(f"Task updated: {task_id}, {kwargs}")

    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task.

        Args:
            task_id: Task identifier.

        Returns:
            bool: True if removed, False if not found.
        """
        with self._lock:
            task = self._state.get_task(task_id)
            removed = self._state.remove_task(task_id)

            if removed and task:
                self._notify_observers("tasks", task, None)

        if removed:
            logger.debug(f"Task removed: {task_id}")

        return removed

    def get_all_tasks(self) -> list[TaskState]:
        """
        Get all tasks.

        Returns:
            list[TaskState]: List of all task states.
        """
        with self._lock:
            return [task.model_copy(deep=True) for task in self._state.tasks.values()]

    def clear_tasks(self) -> None:
        """Clear all tasks."""
        with self._lock:
            old_tasks = list(self._state.tasks.values())
            self._state.tasks.clear()

            for task in old_tasks:
                self._notify_observers("tasks", task, None)

        logger.info("All tasks cleared")

    def register_observer(self, key: str, callback: StateChangeCallback) -> None:
        """
        Register a state change observer.

        Args:
            key: State key to observe (e.g., "collection", "ui", "task.{task_id}").
            callback: Callback function (key, old_value, new_value) -> None.
        """
        with self._lock:
            if key not in self._observers:
                self._observers[key] = []
            self._observers[key].append(callback)

        logger.debug(f"Observer registered for: {key}")

    def unregister_observer(self, key: str, callback: StateChangeCallback) -> bool:
        """
        Unregister a state change observer.

        Args:
            key: State key.
            callback: Callback function to remove.

        Returns:
            bool: True if removed, False if not found.
        """
        with self._lock:
            if key in self._observers and callback in self._observers[key]:
                self._observers[key].remove(callback)
                if not self._observers[key]:
                    del self._observers[key]
                logger.debug(f"Observer unregistered for: {key}")
                return True

        return False

    def clear_observers(self, key: Optional[str] = None) -> None:
        """
        Clear observers.

        Args:
            key: Specific key to clear, or None to clear all.
        """
        with self._lock:
            if key:
                if key in self._observers:
                    del self._observers[key]
                    logger.debug(f"Observers cleared for: {key}")
            else:
                self._observers.clear()
                logger.info("All observers cleared")

    def _notify_observers(self, key: str, old_value: Any, new_value: Any) -> None:
        """
        Notify observers of state changes.

        Args:
            key: State key that changed.
            old_value: Previous value.
            new_value: New value.
        """
        observers = self._observers.get(key, [])

        for callback in observers:
            try:
                callback(key, old_value, new_value)
            except Exception as e:
                logger.error(f"Observer callback error for {key}: {e}")

    def reset(self) -> None:
        """Reset state to initial values."""
        with self._lock:
            self._state = GlobalState()
            self._observers.clear()

        logger.info("State manager reset")

    def export_state(self) -> dict:
        """
        Export state as dictionary.

        Returns:
            dict: State data.
        """
        with self._lock:
            return self._state.model_dump()

    def import_state(self, state_data: dict) -> None:
        """
        Import state from dictionary.

        Args:
            state_data: State data to import.

        Raises:
            StateError: If import fails.
        """
        try:
            with self._lock:
                new_state = GlobalState(**state_data)
                self._state = new_state
                logger.info("State imported successfully")
        except Exception as e:
            raise StateError(f"Failed to import state: {e}") from e
