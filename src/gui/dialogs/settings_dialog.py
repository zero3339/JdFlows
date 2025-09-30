"""
Settings Dialog

Application settings configuration dialog.
"""
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt6.QtCore import pyqtSignal
from loguru import logger

from src.core.config import ApplicationConfig
from src.core.config_manager import ConfigManager


class SettingsDialog(QDialog):
    """Settings configuration dialog."""

    # Signal emitted when settings are saved
    settings_saved = pyqtSignal()

    def __init__(self, config_manager: Optional[ConfigManager] = None, parent=None) -> None:
        """
        Initialize the settings dialog.

        Args:
            config_manager: Configuration manager instance.
            parent: Parent widget.
        """
        super().__init__(parent)

        self.config_manager = config_manager
        self.config: Optional[ApplicationConfig] = None

        if self.config_manager:
            self.config = self.config_manager.get_config()

        self._setup_ui()
        self._load_config()

        logger.info("Settings dialog initialized")

    def _setup_ui(self) -> None:
        """Setup the dialog UI."""
        self.setWindowTitle("设置")
        self.setMinimumSize(600, 500)

        # Main layout
        layout = QVBoxLayout(self)

        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add tabs
        self._create_app_tab()
        self._create_window_tab()
        self._create_browser_tab()
        self._create_logging_tab()

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save_settings)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _create_app_tab(self) -> None:
        """Create application settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # App group
        app_group = QGroupBox("应用程序设置")
        app_layout = QFormLayout()

        self.app_name_edit = QLineEdit()
        app_layout.addRow("应用名称:", self.app_name_edit)

        self.app_version_edit = QLineEdit()
        self.app_version_edit.setReadOnly(True)
        app_layout.addRow("版本:", self.app_version_edit)

        self.app_debug_checkbox = QCheckBox()
        app_layout.addRow("调试模式:", self.app_debug_checkbox)

        app_group.setLayout(app_layout)
        layout.addWidget(app_group)

        layout.addStretch()
        self.tab_widget.addTab(tab, "应用程序")

    def _create_window_tab(self) -> None:
        """Create window settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Window group
        window_group = QGroupBox("窗口设置")
        window_layout = QFormLayout()

        self.window_title_edit = QLineEdit()
        window_layout.addRow("窗口标题:", self.window_title_edit)

        self.window_width_spin = QSpinBox()
        self.window_width_spin.setRange(800, 3840)
        self.window_width_spin.setSingleStep(10)
        window_layout.addRow("窗口宽度:", self.window_width_spin)

        self.window_height_spin = QSpinBox()
        self.window_height_spin.setRange(600, 2160)
        self.window_height_spin.setSingleStep(10)
        window_layout.addRow("窗口高度:", self.window_height_spin)

        self.window_min_width_spin = QSpinBox()
        self.window_min_width_spin.setRange(640, 2048)
        self.window_min_width_spin.setSingleStep(10)
        window_layout.addRow("最小宽度:", self.window_min_width_spin)

        self.window_min_height_spin = QSpinBox()
        self.window_min_height_spin.setRange(480, 1440)
        self.window_min_height_spin.setSingleStep(10)
        window_layout.addRow("最小高度:", self.window_min_height_spin)

        window_group.setLayout(window_layout)
        layout.addWidget(window_group)

        layout.addStretch()
        self.tab_widget.addTab(tab, "窗口")

    def _create_browser_tab(self) -> None:
        """Create browser settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Browser group
        browser_group = QGroupBox("浏览器设置")
        browser_layout = QFormLayout()

        self.browser_headless_checkbox = QCheckBox()
        browser_layout.addRow("无头模式:", self.browser_headless_checkbox)

        self.browser_timeout_spin = QSpinBox()
        self.browser_timeout_spin.setRange(1000, 300000)
        self.browser_timeout_spin.setSingleStep(1000)
        self.browser_timeout_spin.setSuffix(" ms")
        browser_layout.addRow("超时时间:", self.browser_timeout_spin)

        self.browser_user_agent_edit = QLineEdit()
        self.browser_user_agent_edit.setPlaceholderText("留空使用默认User-Agent")
        browser_layout.addRow("User-Agent:", self.browser_user_agent_edit)

        self.browser_viewport_width_spin = QSpinBox()
        self.browser_viewport_width_spin.setRange(800, 3840)
        browser_layout.addRow("视口宽度:", self.browser_viewport_width_spin)

        self.browser_viewport_height_spin = QSpinBox()
        self.browser_viewport_height_spin.setRange(600, 2160)
        browser_layout.addRow("视口高度:", self.browser_viewport_height_spin)

        browser_group.setLayout(browser_layout)
        layout.addWidget(browser_group)

        layout.addStretch()
        self.tab_widget.addTab(tab, "浏览器")

    def _create_logging_tab(self) -> None:
        """Create logging settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Logging group
        logging_group = QGroupBox("日志设置")
        logging_layout = QFormLayout()

        self.logging_level_combo = QComboBox()
        self.logging_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        logging_layout.addRow("日志级别:", self.logging_level_combo)

        self.logging_file_edit = QLineEdit()
        logging_layout.addRow("日志文件:", self.logging_file_edit)

        self.logging_rotation_edit = QLineEdit()
        logging_layout.addRow("日志轮转:", self.logging_rotation_edit)

        self.logging_retention_edit = QLineEdit()
        logging_layout.addRow("日志保留:", self.logging_retention_edit)

        self.logging_compression_edit = QLineEdit()
        logging_layout.addRow("压缩格式:", self.logging_compression_edit)

        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)

        layout.addStretch()
        self.tab_widget.addTab(tab, "日志")

    def _load_config(self) -> None:
        """Load configuration into UI widgets."""
        if not self.config:
            return

        try:
            # App settings
            self.app_name_edit.setText(self.config.app.name)
            self.app_version_edit.setText(self.config.app.version)
            self.app_debug_checkbox.setChecked(self.config.app.debug)

            # Window settings
            self.window_title_edit.setText(self.config.window.title)
            self.window_width_spin.setValue(self.config.window.width)
            self.window_height_spin.setValue(self.config.window.height)
            self.window_min_width_spin.setValue(self.config.window.min_width)
            self.window_min_height_spin.setValue(self.config.window.min_height)

            # Browser settings
            self.browser_headless_checkbox.setChecked(self.config.system.browser.headless)
            self.browser_timeout_spin.setValue(self.config.system.browser.timeout)
            if self.config.system.browser.user_agent:
                self.browser_user_agent_edit.setText(self.config.system.browser.user_agent)
            self.browser_viewport_width_spin.setValue(self.config.system.browser.viewport_width)
            self.browser_viewport_height_spin.setValue(self.config.system.browser.viewport_height)

            # Logging settings
            self.logging_level_combo.setCurrentText(self.config.system.logging.level)
            self.logging_file_edit.setText(self.config.system.logging.file)
            self.logging_rotation_edit.setText(self.config.system.logging.rotation)
            self.logging_retention_edit.setText(self.config.system.logging.retention)
            self.logging_compression_edit.setText(self.config.system.logging.compression)

            logger.debug("Configuration loaded into settings dialog")

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")

    def _save_settings(self) -> None:
        """Save settings from UI to configuration."""
        if not self.config or not self.config_manager:
            logger.warning("No config or config manager available")
            self.reject()
            return

        try:
            # Update config object
            self.config.app.name = self.app_name_edit.text()
            self.config.app.debug = self.app_debug_checkbox.isChecked()

            self.config.window.title = self.window_title_edit.text()
            self.config.window.width = self.window_width_spin.value()
            self.config.window.height = self.window_height_spin.value()
            self.config.window.min_width = self.window_min_width_spin.value()
            self.config.window.min_height = self.window_min_height_spin.value()

            self.config.system.browser.headless = self.browser_headless_checkbox.isChecked()
            self.config.system.browser.timeout = self.browser_timeout_spin.value()
            user_agent = self.browser_user_agent_edit.text().strip()
            self.config.system.browser.user_agent = user_agent if user_agent else None
            self.config.system.browser.viewport_width = self.browser_viewport_width_spin.value()
            self.config.system.browser.viewport_height = self.browser_viewport_height_spin.value()

            self.config.system.logging.level = self.logging_level_combo.currentText()
            self.config.system.logging.file = self.logging_file_edit.text()
            self.config.system.logging.rotation = self.logging_rotation_edit.text()
            self.config.system.logging.retention = self.logging_retention_edit.text()
            self.config.system.logging.compression = self.logging_compression_edit.text()

            # Save to file
            self.config_manager.save_config(self.config)

            logger.info("Settings saved successfully")
            self.settings_saved.emit()
            self.accept()

        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            self.reject()
