"""
Main Application

JDFlows main application class with PyQt6 integration.
"""
from typing import Optional, Any

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from loguru import logger

from src.core.application_core import ApplicationCore, ApplicationState
from src.core.config_manager import ConfigManager
from src.core.exceptions import JDFlowsException, GUIError


class JDFlowsApplication:
    """Main JDFlows application class."""

    def __init__(self, argv: Optional[list[str]] = None) -> None:
        """
        Initialize the JDFlows application.

        Args:
            argv: Command line arguments.
        """
        self.argv = argv or []

        # Core components
        self.core = ApplicationCore(app_name="JDFlows")
        self.qt_app: Optional[QApplication] = None
        self.main_window: Optional[Any] = None  # Will be set when GUI is implemented

        # Timers
        self._shutdown_timer: Optional[QTimer] = None

    def initialize(self) -> None:
        """
        Initialize the application.

        Raises:
            JDFlowsException: If initialization fails.
        """
        try:
            # Initialize core
            self.core.initialize()
            logger.info("Application core initialized")

            # Register lifecycle callbacks
            self.core.register_startup_callback(self._on_startup)
            self.core.register_shutdown_callback(self._on_shutdown)

            # Initialize Qt application
            self._initialize_qt()
            logger.info("Qt application initialized")

        except Exception as e:
            logger.critical(f"Application initialization failed: {e}")
            raise JDFlowsException(f"Initialization failed: {e}") from e

    def run(self) -> int:
        """
        Run the application.

        Returns:
            int: Exit code.
        """
        try:
            if self.core.get_state() != ApplicationState.READY:
                raise JDFlowsException("Application must be initialized before running")

            # Start the application
            self.core.start()

            # Run Qt event loop
            if self.qt_app is not None:
                logger.info("Starting Qt event loop...")
                return self.qt_app.exec()
            else:
                logger.warning("Qt application not initialized, running in headless mode")
                return 0

        except Exception as e:
            logger.critical(f"Application run failed: {e}")
            return 1
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Shutdown the application gracefully."""
        if self.core.get_state() != ApplicationState.STOPPED:
            logger.info("Shutting down application...")
            self.core.stop()

    def get_config_manager(self) -> Optional[ConfigManager]:
        """Get the configuration manager."""
        return self.core.config_manager

    def get_state(self) -> ApplicationState:
        """Get the current application state."""
        return self.core.get_state()

    def _initialize_qt(self) -> None:
        """Initialize Qt application."""
        try:
            # Create Qt application
            self.qt_app = QApplication(self.argv)

            # Set application properties
            if self.core.config_manager:
                config = self.core.config_manager.get_config()
                self.qt_app.setApplicationName(config.app.name)
                self.qt_app.setApplicationVersion(config.app.version)
                self.qt_app.setOrganizationName("JDFlows")

            logger.info("Qt application created successfully")

        except Exception as e:
            raise GUIError(f"Failed to initialize Qt application: {e}") from e

    def _on_startup(self) -> None:
        """Callback executed on application startup."""
        logger.info("Application startup callback executed")

        # Future: Initialize main window and other GUI components
        # self.main_window = MainWindow(self)
        # self.main_window.show()

    def _on_shutdown(self) -> None:
        """Callback executed on application shutdown."""
        logger.info("Application shutdown callback executed")

        # Cleanup Qt application
        if self.qt_app is not None:
            logger.info("Cleaning up Qt application...")
            # Future: Close main window
            # if self.main_window:
            #     self.main_window.close()

            # Quit Qt application
            self.qt_app.quit()


def create_application(argv: Optional[list[str]] = None) -> JDFlowsApplication:
    """
    Factory function to create and initialize the application.

    Args:
        argv: Command line arguments.

    Returns:
        JDFlowsApplication: Initialized application instance.
    """
    app = JDFlowsApplication(argv=argv)
    app.initialize()
    return app
