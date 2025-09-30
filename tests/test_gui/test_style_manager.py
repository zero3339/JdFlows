"""Tests for style manager"""
from src.gui.style_manager import StyleManager, Theme


class TestStyleManager:
    """Tests for StyleManager"""

    def test_initialization(self):
        """Test style manager initialization"""
        manager = StyleManager()
        assert manager.current_theme == Theme.LIGHT
        assert manager.app is None

    def test_get_theme(self):
        """Test getting current theme"""
        manager = StyleManager()
        assert manager.get_theme() == Theme.LIGHT

    def test_get_color(self):
        """Test getting color from theme"""
        manager = StyleManager()
        color = manager.get_color("primary")
        assert color == "#1976D2"  # Light theme primary color

    def test_get_color_dark_theme(self):
        """Test getting color from dark theme"""
        manager = StyleManager()
        manager.current_theme = Theme.DARK
        color = manager.get_color("primary")
        assert color == "#90CAF9"  # Dark theme primary color

    def test_get_color_not_found(self):
        """Test getting non-existent color"""
        manager = StyleManager()
        color = manager.get_color("nonexistent")
        assert color == "#000000"  # Default color

    def test_add_custom_style(self):
        """Test adding custom style"""
        manager = StyleManager()
        manager.add_custom_style("QPushButton", "background: red;")
        assert "QPushButton" in manager._custom_styles
        assert manager._custom_styles["QPushButton"] == "background: red;"

    def test_build_stylesheet_light(self):
        """Test building light theme stylesheet"""
        manager = StyleManager()
        stylesheet = manager._build_stylesheet(Theme.LIGHT)
        assert "#FFFFFF" in stylesheet  # Background color
        assert "#1976D2" in stylesheet  # Primary color

    def test_build_stylesheet_dark(self):
        """Test building dark theme stylesheet"""
        manager = StyleManager()
        stylesheet = manager._build_stylesheet(Theme.DARK)
        assert "#1E1E1E" in stylesheet  # Background color
        assert "#90CAF9" in stylesheet  # Primary color

    def test_build_stylesheet_with_custom_styles(self):
        """Test building stylesheet with custom styles"""
        manager = StyleManager()
        manager.add_custom_style("QCustomWidget", "margin: 10px;")
        stylesheet = manager._build_stylesheet(Theme.LIGHT)
        assert "QCustomWidget" in stylesheet
        assert "margin: 10px;" in stylesheet
