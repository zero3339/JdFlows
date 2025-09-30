"""Tests for configuration manager"""
import pytest

from src.core.config import ApplicationConfig
from src.core.config_manager import ConfigManager
from src.core.exceptions import ConfigurationError


class TestConfigManager:
    """Tests for ConfigManager"""

    def test_initialization(self, tmp_path):
        """Test config manager initialization"""
        manager = ConfigManager(config_dir=tmp_path)
        assert manager.config_dir == tmp_path
        assert manager.config_dir.exists()

    def test_get_or_create_default(self, tmp_path):
        """Test getting or creating default configuration"""
        manager = ConfigManager(config_dir=tmp_path)
        config = manager.get_or_create_default()

        assert config.app.name == "JDFlows"
        assert (tmp_path / "app.json").exists()
        assert (tmp_path / "system.json").exists()

    def test_save_and_load(self, tmp_path):
        """Test saving and loading configuration"""
        manager = ConfigManager(config_dir=tmp_path)

        # Create and save config
        config = ApplicationConfig()
        config.app.debug = True
        manager.save(config)

        # Load config
        loaded_config = manager.load()
        assert loaded_config.app.debug is True

    def test_get_config_without_loading(self, tmp_path):
        """Test getting config without loading first"""
        manager = ConfigManager(config_dir=tmp_path)

        with pytest.raises(ConfigurationError):
            manager.get_config()

    def test_update_app_config(self, tmp_path):
        """Test updating app configuration"""
        manager = ConfigManager(config_dir=tmp_path)
        manager.get_or_create_default()

        manager.update_app_config(debug=True, version="1.0.0")
        config = manager.get_config()

        assert config.app.debug is True
        assert config.app.version == "1.0.0"

    def test_get_app_name(self, tmp_path):
        """Test getting app name"""
        manager = ConfigManager(config_dir=tmp_path)
        manager.get_or_create_default()

        assert manager.get_app_name() == "JDFlows"

    def test_is_debug_mode(self, tmp_path):
        """Test checking debug mode"""
        manager = ConfigManager(config_dir=tmp_path)
        manager.get_or_create_default()

        assert manager.is_debug_mode() is False

        manager.update_app_config(debug=True)
        assert manager.is_debug_mode() is True
