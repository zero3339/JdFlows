"""Tests for configuration models"""
import pytest
from pydantic import ValidationError

from src.core.config import (
    AppConfig,
    WindowConfig,
    LoggingConfig,
    ApplicationConfig,
)


class TestAppConfig:
    """Tests for AppConfig"""

    def test_default_values(self):
        """Test default configuration values"""
        config = AppConfig()
        assert config.name == "JDFlows"
        assert config.version == "0.1.0"
        assert config.debug is False

    def test_custom_values(self):
        """Test custom configuration values"""
        config = AppConfig(name="TestApp", version="1.0.0", debug=True)
        assert config.name == "TestApp"
        assert config.version == "1.0.0"
        assert config.debug is True


class TestWindowConfig:
    """Tests for WindowConfig"""

    def test_default_values(self):
        """Test default window configuration"""
        config = WindowConfig()
        assert config.width == 1280
        assert config.height == 800
        assert config.min_width == 1024
        assert config.min_height == 600

    def test_valid_dimensions(self):
        """Test valid window dimensions"""
        config = WindowConfig(width=1920, height=1080)
        assert config.width == 1920
        assert config.height == 1080

    def test_invalid_dimensions(self):
        """Test invalid window dimensions"""
        with pytest.raises(ValidationError):
            WindowConfig(width=500)  # Too small


class TestLoggingConfig:
    """Tests for LoggingConfig"""

    def test_default_values(self):
        """Test default logging configuration"""
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.file == "logs/jdflows.log"

    def test_level_validation(self):
        """Test log level validation"""
        config = LoggingConfig(level="debug")
        assert config.level == "DEBUG"

        with pytest.raises(ValidationError):
            LoggingConfig(level="INVALID")


class TestApplicationConfig:
    """Tests for ApplicationConfig"""

    def test_default_configuration(self):
        """Test default application configuration"""
        config = ApplicationConfig()
        assert config.app.name == "JDFlows"
        assert config.window.width == 1280
        assert config.system.database.url == "sqlite:///data/jdflows.db"

    def test_get_log_path(self):
        """Test getting log file path"""
        config = ApplicationConfig()
        log_path = config.get_log_path()
        assert str(log_path) == "logs/jdflows.log"

    def test_get_db_path(self):
        """Test getting database path"""
        config = ApplicationConfig()
        db_path = config.get_db_path()
        assert db_path is not None
        assert str(db_path) == "data/jdflows.db"
