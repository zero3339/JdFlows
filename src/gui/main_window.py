"""
Main Window

JDFlows main application window.
"""
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStatusBar,
    QLabel,
    QPushButton,
    QToolBar,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction
from loguru import logger

from src.gui.style_manager import StyleManager, Theme
from src.core.config import WindowConfig


class MainWindow(QMainWindow):
    """Main application window."""

    # Signals
    theme_changed = pyqtSignal(Theme)
    window_closed = pyqtSignal()

    def __init__(
        self,
        config: Optional[WindowConfig] = None,
        style_manager: Optional[StyleManager] = None,
    ) -> None:
        """
        Initialize the main window.

        Args:
            config: Window configuration.
            style_manager: Style manager instance.
        """
        super().__init__()

        self.config = config or WindowConfig()
        self.style_manager = style_manager or StyleManager()

        # Setup window
        self._setup_window()

        # Setup UI components
        self._setup_menubar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_statusbar()

        logger.info("Main window initialized")

    def _setup_window(self) -> None:
        """Setup main window properties."""
        # Set window title
        self.setWindowTitle(self.config.title)

        # Set window size
        self.resize(self.config.width, self.config.height)
        self.setMinimumSize(self.config.min_width, self.config.min_height)

        # Center window on screen
        screen = self.screen()
        if screen:
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.config.width) // 2
            y = (screen_geometry.height() - self.config.height) // 2
            self.move(x, y)

    def _setup_menubar(self) -> None:
        """Setup menu bar."""
        menubar = self.menuBar()
        if not menubar:
            return

        # File menu
        file_menu = menubar.addMenu("文件(&F)")

        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("视图(&V)")

        self.toggle_theme_action = QAction("切换主题", self)
        self.toggle_theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(self.toggle_theme_action)

        # Help menu
        help_menu = menubar.addMenu("帮助(&H)")

        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self) -> None:
        """Setup toolbar."""
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add toolbar actions (placeholders for now)
        # Future: Add real actions when features are implemented

    def _setup_central_widget(self) -> None:
        """Setup central widget."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Welcome label (placeholder)
        welcome_label = QLabel("欢迎使用 JDFlows")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24pt; font-weight: bold;")
        main_layout.addWidget(welcome_label)

        # Description
        desc_label = QLabel("京东商品采集系统 v0.1.0")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("font-size: 12pt; color: #757575;")
        main_layout.addWidget(desc_label)

        main_layout.addStretch()

        # Action buttons (placeholder)
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        start_button = QPushButton("开始采集")
        start_button.setMinimumWidth(120)
        start_button.clicked.connect(self._on_start_collection)
        button_layout.addWidget(start_button)

        settings_button = QPushButton("设置")
        settings_button.setMinimumWidth(120)
        settings_button.clicked.connect(self._on_open_settings)
        button_layout.addWidget(settings_button)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def _setup_statusbar(self) -> None:
        """Setup status bar."""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Status label
        self.status_label = QLabel("就绪")
        statusbar.addWidget(self.status_label)

        # Version label
        version_label = QLabel("v0.1.0")
        statusbar.addPermanentWidget(version_label)

    def set_theme(self, theme: Theme) -> None:
        """
        Set window theme.

        Args:
            theme: Theme to apply.
        """
        self.style_manager.set_theme(theme)
        self.theme_changed.emit(theme)
        logger.info(f"Window theme changed to: {theme.value}")

    def update_status(self, message: str) -> None:
        """
        Update status bar message.

        Args:
            message: Status message.
        """
        self.status_label.setText(message)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        logger.info("Main window closing")
        self.window_closed.emit()
        event.accept()

    def _toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        current = self.style_manager.get_theme()
        new_theme = Theme.DARK if current == Theme.LIGHT else Theme.LIGHT
        self.set_theme(new_theme)

    def _show_about(self) -> None:
        """Show about dialog."""
        # Placeholder - will be implemented in later tasks
        self.update_status("关于对话框 - 待实现")
        logger.info("About dialog requested")

    def _on_start_collection(self) -> None:
        """Handle start collection button."""
        # Placeholder - will be implemented in later tasks
        self.update_status("采集功能 - 待实现")
        logger.info("Start collection requested")

    def _on_open_settings(self) -> None:
        """Handle settings button."""
        # Placeholder - will be implemented in later tasks
        self.update_status("设置对话框 - 待实现")
        logger.info("Settings dialog requested")
