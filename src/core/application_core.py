"""
Application Core

Provides the core application management functionality.
"""
import signal
import sys
from enum import Enum
from typing import Optional, Callable, Any
from pathlib import Path

from loguru import logger

from .config_manager import ConfigManager
from .logger import setup_logger
from .exception_handler import install_exception_handler, ExceptionHandler
from .exceptions import JDFlowsException


class ApplicationState(Enum):
    """Application state enumeration."""

    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class ApplicationCore:
    """Core application management class."""

    def __init__(self, app_name: str = "JDFlows", config_dir: Optional[Path] = None) -> None:
        """
        Initialize the application core.

        Args:
            app_name: Application name.
            config_dir: Configuration directory path.
        """
        self.app_name = app_name
        self.config_dir = config_dir or Path("config")
        self.state = ApplicationState.INITIALIZING

        # Core components
        self.config_manager: Optional[ConfigManager] = None
        self.exception_handler: Optional[ExceptionHandler] = None

        # Lifecycle callbacks
        self._on_startup_callbacks: list[Callable[[], None]] = []
        self._on_shutdown_callbacks: list[Callable[[], None]] = []

        # Signal handlers
        self._original_sigint_handler: Optional[Any] = None
        self._original_sigterm_handler: Optional[Any] = None

    def initialize(self) -> None:
        """
        Initialize the application core components.

        Raises:
            JDFlowsException: If initialization fails.
        """
        try:
            logger.info(f"Initializing {self.app_name}...")

            # Initialize configuration manager
            self.config_manager = ConfigManager(config_dir=self.config_dir)
            config = self.config_manager.get_or_create_default()

            # Setup logging
            setup_logger(config=config.system.logging)
            logger.info(f"Logging system initialized: {config.system.logging.file}")

            # Install exception handler
            log_file = Path("logs/errors.log")
            self.exception_handler = install_exception_handler(log_file=log_file)
            logger.info("Exception handler installed")

            # Install signal handlers
            self._install_signal_handlers()
            logger.info("Signal handlers installed")

            self.state = ApplicationState.READY
            logger.info(f"{self.app_name} core initialized successfully")

        except Exception as e:
            self.state = ApplicationState.ERROR
            logger.critical(f"Failed to initialize application core: {e}")
            raise JDFlowsException(f"Initialization failed: {e}") from e

    def start(self) -> None:
        """
        Start the application.

        Raises:
            JDFlowsException: If application is not ready or start fails.
        """
        if self.state != ApplicationState.READY:
            raise JDFlowsException(f"Cannot start: application is in {self.state.value} state")

        try:
            logger.info(f"Starting {self.app_name}...")
            self.state = ApplicationState.RUNNING

            # Execute startup callbacks
            for callback in self._on_startup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Startup callback failed: {e}")

            logger.info(f"{self.app_name} started successfully")

        except Exception as e:
            self.state = ApplicationState.ERROR
            logger.critical(f"Failed to start application: {e}")
            raise JDFlowsException(f"Start failed: {e}") from e

    def stop(self) -> None:
        """Stop the application gracefully."""
        if self.state == ApplicationState.STOPPED:
            logger.warning("Application is already stopped")
            return

        try:
            logger.info(f"Stopping {self.app_name}...")
            self.state = ApplicationState.STOPPING

            # Execute shutdown callbacks
            for callback in self._on_shutdown_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Shutdown callback failed: {e}")

            # Restore signal handlers
            self._restore_signal_handlers()

            self.state = ApplicationState.STOPPED
            logger.info(f"{self.app_name} stopped successfully")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            self.state = ApplicationState.ERROR

    def register_startup_callback(self, callback: Callable[[], None]) -> None:
        """
        Register a callback to be executed on startup.

        Args:
            callback: Callback function.
        """
        self._on_startup_callbacks.append(callback)
        logger.debug(f"Registered startup callback: {callback.__name__}")

    def register_shutdown_callback(self, callback: Callable[[], None]) -> None:
        """
        Register a callback to be executed on shutdown.

        Args:
            callback: Callback function.
        """
        self._on_shutdown_callbacks.append(callback)
        logger.debug(f"Registered shutdown callback: {callback.__name__}")

    def get_state(self) -> ApplicationState:
        """Get the current application state."""
        return self.state

    def is_running(self) -> bool:
        """Check if the application is running."""
        return self.state == ApplicationState.RUNNING

    def _install_signal_handlers(self) -> None:
        """Install signal handlers for graceful shutdown."""
        self._original_sigint_handler = signal.signal(signal.SIGINT, self._signal_handler)
        self._original_sigterm_handler = signal.signal(signal.SIGTERM, self._signal_handler)

    def _restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler is not None:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
        if self._original_sigterm_handler is not None:
            signal.signal(signal.SIGTERM, self._original_sigterm_handler)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        """
        Handle termination signals.

        Args:
            signum: Signal number.
            frame: Current stack frame.
        """
        sig_name = signal.Signals(signum).name
        logger.warning(f"Received signal {sig_name}, initiating graceful shutdown...")
        self.stop()
        sys.exit(0)
