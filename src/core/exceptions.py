"""
Custom Exceptions

Defines custom exception classes for the application.
"""


class JDFlowsException(Exception):
    """Base exception for all JDFlows errors."""

    def __init__(self, message: str, *args: object) -> None:
        """
        Initialize the exception.

        Args:
            message: Error message.
            *args: Additional arguments.
        """
        self.message = message
        super().__init__(message, *args)


class ConfigurationError(JDFlowsException):
    """Raised when there is a configuration error."""

    pass


class LoggingError(JDFlowsException):
    """Raised when there is a logging system error."""

    pass


class DatabaseError(JDFlowsException):
    """Raised when there is a database error."""

    pass


class BrowserError(JDFlowsException):
    """Raised when there is a browser automation error."""

    pass


class DataExtractionError(JDFlowsException):
    """Raised when data extraction fails."""

    pass


class ValidationError(JDFlowsException):
    """Raised when data validation fails."""

    pass


class GUIError(JDFlowsException):
    """Raised when there is a GUI error."""

    pass


class NetworkError(JDFlowsException):
    """Raised when there is a network error."""

    pass


class AuthenticationError(JDFlowsException):
    """Raised when authentication fails."""

    pass


class ResourceNotFoundError(JDFlowsException):
    """Raised when a required resource is not found."""

    pass


class OperationTimeoutError(JDFlowsException):
    """Raised when an operation times out."""

    pass


class DataError(JDFlowsException):
    """Data processing error."""

    pass


class StateError(JDFlowsException):
    """State management error."""

    pass
