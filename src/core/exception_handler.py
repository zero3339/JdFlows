"""
Global Exception Handler

Provides global exception handling and error reporting.
"""
import sys
import traceback
from typing import Optional, Callable, Any
from pathlib import Path

from loguru import logger

from .exceptions import JDFlowsException


class ExceptionHandler:
    """Global exception handler for the application."""

    def __init__(self, log_file: Optional[Path] = None) -> None:
        """
        Initialize the exception handler.

        Args:
            log_file: Path to the error log file.
        """
        self.log_file = log_file or Path("logs/errors.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._original_excepthook: Optional[Callable[..., Any]] = None

    def install(self) -> None:
        """Install the global exception handler."""
        self._original_excepthook = sys.excepthook
        sys.excepthook = self.handle_exception

    def uninstall(self) -> None:
        """Uninstall the global exception handler."""
        if self._original_excepthook is not None:
            sys.excepthook = self._original_excepthook
            self._original_excepthook = None

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: Any,
    ) -> None:
        """
        Handle uncaught exceptions.

        Args:
            exc_type: Exception type.
            exc_value: Exception instance.
            exc_traceback: Traceback object.
        """
        # Ignore keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Format exception information
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # Log the exception
        if isinstance(exc_value, JDFlowsException):
            logger.error(f"Application error: {exc_value.message}\n{error_msg}")
        else:
            logger.critical(f"Uncaught exception:\n{error_msg}")

        # Write to error log file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"Exception: {exc_type.__name__}\n")
                f.write(f"Message: {exc_value}\n")
                f.write(f"{'='*80}\n")
                f.write(error_msg)
                f.write(f"\n{'='*80}\n\n")
        except Exception as e:
            logger.error(f"Failed to write to error log: {e}")

    def handle_thread_exception(self, args: Any) -> None:
        """
        Handle exceptions in threads.

        Args:
            args: Threading excepthook arguments.
        """
        exc_type = args.exc_type
        exc_value = args.exc_value
        exc_traceback = args.exc_traceback
        thread = args.thread

        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        logger.error(f"Exception in thread {thread.name}:\n{error_msg}")


# Global exception handler instance
_exception_handler: Optional[ExceptionHandler] = None


def install_exception_handler(log_file: Optional[Path] = None) -> ExceptionHandler:
    """
    Install the global exception handler.

    Args:
        log_file: Path to the error log file.

    Returns:
        ExceptionHandler: The installed exception handler.
    """
    global _exception_handler
    if _exception_handler is None:
        _exception_handler = ExceptionHandler(log_file)
        _exception_handler.install()
    return _exception_handler


def uninstall_exception_handler() -> None:
    """Uninstall the global exception handler."""
    global _exception_handler
    if _exception_handler is not None:
        _exception_handler.uninstall()
        _exception_handler = None


def get_exception_handler() -> Optional[ExceptionHandler]:
    """Get the global exception handler instance."""
    return _exception_handler
