"""
Configuration Manager

Manages loading, saving, and accessing application configuration.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any

from pydantic import ValidationError

from .config import ApplicationConfig, AppConfig, WindowConfig
from .exceptions import ConfigurationError


class ConfigManager:
    """Configuration manager for loading and saving application settings."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """
        Initialize the configuration manager.

        Args:
            config_dir: Directory containing configuration files.
                       Defaults to 'config' in the current directory.
        """
        self.config_dir = config_dir or Path("config")
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self._config: Optional[ApplicationConfig] = None
        self._app_config_file = self.config_dir / "app.json"
        self._system_config_file = self.config_dir / "system.json"

    def load(self) -> ApplicationConfig:
        """
        Load configuration from JSON files.

        Returns:
            ApplicationConfig: The loaded configuration.

        Raises:
            ConfigurationError: If configuration loading or validation fails.
        """
        try:
            config_data: Dict[str, Any] = {}

            # Load app configuration
            if self._app_config_file.exists():
                with open(self._app_config_file, "r", encoding="utf-8") as f:
                    app_data = json.load(f)
                    config_data.update(app_data)

            # Load system configuration
            if self._system_config_file.exists():
                with open(self._system_config_file, "r", encoding="utf-8") as f:
                    system_data = json.load(f)
                    config_data["system"] = system_data

            # Create and validate configuration
            self._config = ApplicationConfig(**config_data)
            return self._config

        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}") from e
        except ValidationError as e:
            raise ConfigurationError(f"Configuration validation failed: {e}") from e
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e

    def save(self, config: Optional[ApplicationConfig] = None) -> None:
        """
        Save configuration to JSON files.

        Args:
            config: Configuration to save. If None, saves the current config.

        Raises:
            ConfigurationError: If no configuration is available or save fails.
        """
        if config is None:
            if self._config is None:
                raise ConfigurationError("No configuration to save")
            config = self._config

        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Save app configuration
            app_data = {
                "app": config.app.model_dump(),
                "window": config.window.model_dump(),
            }
            with open(self._app_config_file, "w", encoding="utf-8") as f:
                json.dump(app_data, f, indent=2, ensure_ascii=False)

            # Save system configuration
            system_data = config.system.model_dump()
            with open(self._system_config_file, "w", encoding="utf-8") as f:
                json.dump(system_data, f, indent=2, ensure_ascii=False)

            self._config = config

        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}") from e

    def get_config(self) -> ApplicationConfig:
        """
        Get the current configuration.

        Returns:
            ApplicationConfig: The current configuration.

        Raises:
            ConfigurationError: If configuration is not loaded.
        """
        if self._config is None:
            raise ConfigurationError("Configuration not loaded. Call load() first.")
        return self._config

    def reload(self) -> ApplicationConfig:
        """
        Reload configuration from files.

        Returns:
            ApplicationConfig: The reloaded configuration.
        """
        return self.load()

    def get_or_create_default(self) -> ApplicationConfig:
        """
        Load existing configuration or create default if none exists.

        Returns:
            ApplicationConfig: The loaded or default configuration.
        """
        if self._app_config_file.exists() or self._system_config_file.exists():
            return self.load()
        else:
            # Create default configuration
            self._config = ApplicationConfig()
            self.save(self._config)
            return self._config

    def update_app_config(self, **kwargs: Any) -> None:
        """
        Update application configuration fields.

        Args:
            **kwargs: Fields to update in AppConfig.

        Raises:
            ConfigurationError: If configuration is not loaded or update fails.
        """
        if self._config is None:
            raise ConfigurationError("Configuration not loaded")

        try:
            updated_data = self._config.app.model_dump()
            updated_data.update(kwargs)
            self._config.app = AppConfig(**updated_data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid app configuration update: {e}") from e

    def update_window_config(self, **kwargs: Any) -> None:
        """
        Update window configuration fields.

        Args:
            **kwargs: Fields to update in WindowConfig.

        Raises:
            ConfigurationError: If configuration is not loaded or update fails.
        """
        if self._config is None:
            raise ConfigurationError("Configuration not loaded")

        try:
            updated_data = self._config.window.model_dump()
            updated_data.update(kwargs)
            self._config.window = WindowConfig(**updated_data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid window configuration update: {e}") from e

    def get_app_name(self) -> str:
        """Get the application name."""
        return self.get_config().app.name

    def get_app_version(self) -> str:
        """Get the application version."""
        return self.get_config().app.version

    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get_config().app.debug
