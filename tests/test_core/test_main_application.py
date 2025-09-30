"""Tests for main application"""
from src.main_application import JDFlowsApplication, create_application
from src.core.application_core import ApplicationState


class TestJDFlowsApplication:
    """Tests for JDFlowsApplication"""

    def test_initialization(self, tmp_path, monkeypatch):
        """Test application initialization"""
        # Skip Qt initialization in tests
        monkeypatch.setattr("src.main_application.QApplication", lambda x: None)

        app = JDFlowsApplication(argv=[])
        assert app.core is not None
        assert app.qt_app is None

    def test_create_application_factory(self, tmp_path, monkeypatch):
        """Test application factory function"""

        # Mock Qt to avoid display requirements
        class MockQApp:
            def __init__(self, argv):
                pass

            def setApplicationName(self, name):
                pass

            def setApplicationVersion(self, version):
                pass

            def setOrganizationName(self, org):
                pass

            def exec(self):
                return 0

            def quit(self):
                pass

        monkeypatch.setattr("src.main_application.QApplication", MockQApp)

        # Create temp config dir
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Patch core to use temp config
        original_init = JDFlowsApplication.__init__

        def patched_init(self, argv=None):
            original_init(self, argv)
            self.core.config_dir = config_dir

        monkeypatch.setattr(JDFlowsApplication, "__init__", patched_init)

        app = create_application(argv=[])
        assert app.get_state() == ApplicationState.READY

    def test_get_config_manager(self, tmp_path, monkeypatch):
        """Test getting config manager"""
        monkeypatch.setattr("src.main_application.QApplication", lambda x: None)

        app = JDFlowsApplication(argv=[])
        app.core.config_dir = tmp_path / "config"
        app.core.initialize()

        config_manager = app.get_config_manager()
        assert config_manager is not None

    def test_get_state(self, tmp_path, monkeypatch):
        """Test getting application state"""
        monkeypatch.setattr("src.main_application.QApplication", lambda x: None)

        app = JDFlowsApplication(argv=[])
        assert app.get_state() == ApplicationState.INITIALIZING
