"""Tests for custom exceptions"""
import pytest

from src.core.exceptions import (
    JDFlowsException,
    ConfigurationError,
    LoggingError,
)


class TestExceptions:
    """Tests for custom exception classes"""

    def test_base_exception(self):
        """Test base JDFlowsException"""
        exc = JDFlowsException("Test error")
        assert exc.message == "Test error"
        assert str(exc) == "Test error"

    def test_configuration_error(self):
        """Test ConfigurationError"""
        exc = ConfigurationError("Config error")
        assert isinstance(exc, JDFlowsException)
        assert exc.message == "Config error"

    def test_logging_error(self):
        """Test LoggingError"""
        exc = LoggingError("Log error")
        assert isinstance(exc, JDFlowsException)
        assert exc.message == "Log error"

    def test_exception_raise(self):
        """Test raising exceptions"""
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError("Test config error")

        assert "Test config error" in str(exc_info.value)
