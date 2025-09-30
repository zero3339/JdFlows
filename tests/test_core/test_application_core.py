"""Tests for application core"""
from src.core.application_core import ApplicationCore, ApplicationState


class TestApplicationCore:
    """Tests for ApplicationCore"""

    def test_initialization(self, tmp_path):
        """Test core initialization"""
        core = ApplicationCore(app_name="TestApp", config_dir=tmp_path / "config")
        assert core.app_name == "TestApp"
        assert core.state == ApplicationState.INITIALIZING

    def test_initialize_success(self, tmp_path):
        """Test successful initialization"""
        core = ApplicationCore(config_dir=tmp_path / "config")
        core.initialize()

        assert core.state == ApplicationState.READY
        assert core.config_manager is not None
        assert core.exception_handler is not None

    def test_start_when_ready(self, tmp_path):
        """Test starting application when ready"""
        core = ApplicationCore(config_dir=tmp_path / "config")
        core.initialize()
        core.start()

        assert core.state == ApplicationState.RUNNING
        assert core.is_running() is True

    def test_stop(self, tmp_path):
        """Test stopping application"""
        core = ApplicationCore(config_dir=tmp_path / "config")
        core.initialize()
        core.start()
        core.stop()

        assert core.state == ApplicationState.STOPPED
        assert core.is_running() is False

    def test_register_startup_callback(self, tmp_path):
        """Test registering startup callback"""
        core = ApplicationCore(config_dir=tmp_path / "config")

        callback_executed = []

        def test_callback():
            callback_executed.append(True)

        core.register_startup_callback(test_callback)
        core.initialize()
        core.start()

        assert len(callback_executed) == 1

    def test_register_shutdown_callback(self, tmp_path):
        """Test registering shutdown callback"""
        core = ApplicationCore(config_dir=tmp_path / "config")

        callback_executed = []

        def test_callback():
            callback_executed.append(True)

        core.register_shutdown_callback(test_callback)
        core.initialize()
        core.start()
        core.stop()

        assert len(callback_executed) == 1

    def test_get_state(self, tmp_path):
        """Test getting application state"""
        core = ApplicationCore(config_dir=tmp_path / "config")

        assert core.get_state() == ApplicationState.INITIALIZING
        core.initialize()
        assert core.get_state() == ApplicationState.READY
        core.start()
        assert core.get_state() == ApplicationState.RUNNING
        core.stop()
        assert core.get_state() == ApplicationState.STOPPED
