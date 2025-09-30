"""Tests for settings dialog"""
import pytest
from src.core.config import ApplicationConfig, AppConfig, WindowConfig
from src.core.config_manager import ConfigManager


class TestSettingsDialog:
    """Tests for SettingsDialog"""

    def test_config_initialization(self):
        """Test configuration initialization"""
        config = ApplicationConfig()
        assert config.app.name == "JDFlows"
        assert config.app.version == "0.1.0"
        assert config.app.debug is False

    def test_app_config_defaults(self):
        """Test app configuration defaults"""
        app_config = AppConfig()
        assert app_config.name == "JDFlows"
        assert app_config.version == "0.1.0"
        assert app_config.debug is False

    def test_window_config_defaults(self):
        """Test window configuration defaults"""
        window_config = WindowConfig()
        assert window_config.title == "JDFlows"
        assert window_config.width == 1280
        assert window_config.height == 800
        assert window_config.min_width == 1024
        assert window_config.min_height == 600

    def test_config_update(self):
        """Test configuration update"""
        config = ApplicationConfig()
        config.app.name = "Test App"
        config.app.debug = True
        assert config.app.name == "Test App"
        assert config.app.debug is True

    def test_window_config_update(self):
        """Test window configuration update"""
        config = WindowConfig()
        config.width = 1920
        config.height = 1080
        assert config.width == 1920
        assert config.height == 1080

    def test_config_manager_initialization(self, tmp_path):
        """Test config manager initialization"""
        manager = ConfigManager(config_dir=tmp_path / "config")
        assert manager.config_dir == tmp_path / "config"

    def test_config_validation(self):
        """Test configuration validation"""
        # Valid config
        config = WindowConfig(width=1280, height=800)
        assert config.width == 1280
        assert config.height == 800

        # Test constraints
        with pytest.raises(Exception):
            WindowConfig(width=500, height=400)  # Below minimum
