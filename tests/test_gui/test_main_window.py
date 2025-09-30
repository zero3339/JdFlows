"""Tests for main window"""
import pytest
from src.gui.style_manager import Theme
from src.core.config import WindowConfig


@pytest.mark.gui
class TestMainWindow:
    """Tests for MainWindow"""

    def test_config_default_values(self):
        """Test default window configuration"""
        config = WindowConfig()
        assert config.title == "JDFlows"
        assert config.width == 1280
        assert config.height == 800
        assert config.min_width == 1024
        assert config.min_height == 600

    def test_config_custom_values(self):
        """Test custom window configuration"""
        config = WindowConfig(title="Test Window", width=800, height=600)
        assert config.title == "Test Window"
        assert config.width == 800
        assert config.height == 600

    def test_theme_enum(self):
        """Test theme enumeration"""
        assert Theme.LIGHT.value == "light"
        assert Theme.DARK.value == "dark"
