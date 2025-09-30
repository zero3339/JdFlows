"""
Style Manager

Manages application styles and themes.
"""
from enum import Enum
from typing import Dict, Optional
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from loguru import logger


class Theme(Enum):
    """Theme enumeration."""

    LIGHT = "light"
    DARK = "dark"


class StyleManager:
    """Manages application styles and themes."""

    # Theme color palettes
    THEMES: Dict[Theme, Dict[str, str]] = {
        Theme.LIGHT: {
            "background": "#FFFFFF",
            "surface": "#F5F5F5",
            "primary": "#1976D2",
            "secondary": "#424242",
            "accent": "#FF4081",
            "text": "#212121",
            "text_secondary": "#757575",
            "border": "#E0E0E0",
            "hover": "#E3F2FD",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336",
            "info": "#2196F3",
        },
        Theme.DARK: {
            "background": "#1E1E1E",
            "surface": "#2D2D2D",
            "primary": "#90CAF9",
            "secondary": "#B0B0B0",
            "accent": "#F48FB1",
            "text": "#FFFFFF",
            "text_secondary": "#B0B0B0",
            "border": "#404040",
            "hover": "#424242",
            "success": "#66BB6A",
            "warning": "#FFA726",
            "error": "#EF5350",
            "info": "#42A5F5",
        },
    }

    def __init__(self, app: Optional[QApplication] = None) -> None:
        """
        Initialize the style manager.

        Args:
            app: QApplication instance.
        """
        self.app = app
        self.current_theme = Theme.LIGHT
        self._custom_styles: Dict[str, str] = {}

    def set_theme(self, theme: Theme) -> None:
        """
        Set the application theme.

        Args:
            theme: Theme to apply.
        """
        self.current_theme = theme
        stylesheet = self._build_stylesheet(theme)

        if self.app:
            self.app.setStyleSheet(stylesheet)
            logger.info(f"Applied theme: {theme.value}")
        else:
            logger.warning("No QApplication instance available for styling")

    def get_theme(self) -> Theme:
        """Get the current theme."""
        return self.current_theme

    def get_color(self, color_name: str) -> str:
        """
        Get a color from the current theme.

        Args:
            color_name: Name of the color.

        Returns:
            Color hex code.
        """
        colors = self.THEMES.get(self.current_theme, {})
        return colors.get(color_name, "#000000")

    def add_custom_style(self, widget_type: str, style: str) -> None:
        """
        Add custom style for a widget type.

        Args:
            widget_type: Qt widget type (e.g., 'QPushButton').
            style: CSS-like style string.
        """
        self._custom_styles[widget_type] = style
        logger.debug(f"Added custom style for {widget_type}")

    def apply_styles(self) -> None:
        """Apply the current theme with custom styles."""
        self.set_theme(self.current_theme)

    def _build_stylesheet(self, theme: Theme) -> str:
        """
        Build the complete stylesheet for a theme.

        Args:
            theme: Theme to build stylesheet for.

        Returns:
            Complete stylesheet string.
        """
        colors = self.THEMES[theme]

        # Base stylesheet
        stylesheet = f"""
            QWidget {{
                background-color: {colors['background']};
                color: {colors['text']};
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 10pt;
            }}

            QMainWindow {{
                background-color: {colors['background']};
            }}

            QPushButton {{
                background-color: {colors['primary']};
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
            }}

            QPushButton:hover {{
                background-color: {colors['hover']};
                color: {colors['text']};
            }}

            QPushButton:pressed {{
                background-color: {colors['accent']};
            }}

            QPushButton:disabled {{
                background-color: {colors['surface']};
                color: {colors['text_secondary']};
            }}

            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 6px;
            }}

            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 2px solid {colors['primary']};
            }}

            QLabel {{
                color: {colors['text']};
                background: transparent;
            }}

            QGroupBox {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                margin-top: 12px;
                padding: 12px;
                font-weight: bold;
            }}

            QGroupBox::title {{
                color: {colors['primary']};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}

            QTableWidget {{
                background-color: {colors['surface']};
                alternate-background-color: {colors['background']};
                gridline-color: {colors['border']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
            }}

            QTableWidget::item {{
                padding: 5px;
            }}

            QTableWidget::item:selected {{
                background-color: {colors['primary']};
                color: #FFFFFF;
            }}

            QHeaderView::section {{
                background-color: {colors['surface']};
                color: {colors['text']};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {colors['primary']};
                font-weight: bold;
            }}

            QMenuBar {{
                background-color: {colors['surface']};
                color: {colors['text']};
            }}

            QMenuBar::item:selected {{
                background-color: {colors['hover']};
            }}

            QMenu {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
            }}

            QMenu::item:selected {{
                background-color: {colors['hover']};
            }}

            QStatusBar {{
                background-color: {colors['surface']};
                color: {colors['text_secondary']};
            }}

            QToolBar {{
                background-color: {colors['surface']};
                border: none;
                spacing: 4px;
            }}

            QScrollBar:vertical {{
                background: {colors['surface']};
                width: 12px;
                margin: 0px;
            }}

            QScrollBar::handle:vertical {{
                background: {colors['border']};
                min-height: 20px;
                border-radius: 6px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: {colors['text_secondary']};
            }}

            QScrollBar:horizontal {{
                background: {colors['surface']};
                height: 12px;
                margin: 0px;
            }}

            QScrollBar::handle:horizontal {{
                background: {colors['border']};
                min-width: 20px;
                border-radius: 6px;
            }}

            QScrollBar::handle:horizontal:hover {{
                background: {colors['text_secondary']};
            }}

            QProgressBar {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                text-align: center;
            }}

            QProgressBar::chunk {{
                background-color: {colors['primary']};
                border-radius: 3px;
            }}
        """

        # Add custom styles
        for widget_type, custom_style in self._custom_styles.items():
            stylesheet += f"\n{widget_type} {{\n{custom_style}\n}}\n"

        return stylesheet

    def load_custom_stylesheet(self, file_path: Path) -> bool:
        """
        Load custom stylesheet from file.

        Args:
            file_path: Path to stylesheet file.

        Returns:
            True if loaded successfully.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                custom_stylesheet = f.read()

            if self.app:
                current_stylesheet = self._build_stylesheet(self.current_theme)
                self.app.setStyleSheet(current_stylesheet + "\n" + custom_stylesheet)
                logger.info(f"Loaded custom stylesheet: {file_path}")
                return True
            else:
                logger.warning("No QApplication instance available")
                return False

        except Exception as e:
            logger.error(f"Failed to load custom stylesheet: {e}")
            return False
