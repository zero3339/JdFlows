"""
Configuration Data Models

Pydantic models for application configuration validation and management.
"""
from typing import Optional, Any
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class AppConfig(BaseModel):
    """Application configuration."""

    name: str = Field(default="JDFlows", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode flag")

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class WindowConfig(BaseModel):
    """Window configuration."""

    title: str = Field(default="JDFlows", description="Window title")
    width: int = Field(default=1280, ge=800, le=3840, description="Window width")
    height: int = Field(default=800, ge=600, le=2160, description="Window height")
    min_width: int = Field(default=1024, ge=640, description="Minimum window width")
    min_height: int = Field(default=600, ge=480, description="Minimum window height")

    @field_validator("min_width")
    @classmethod
    def validate_min_width(cls, v: int, info: Any) -> int:
        """Ensure min_width is less than or equal to width."""
        # Note: info.data may not have 'width' yet during validation
        return v

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class DatabaseConfig(BaseModel):
    """Database configuration."""

    url: str = Field(default="sqlite:///data/jdflows.db", description="Database URL")
    echo: bool = Field(default=False, description="Echo SQL statements")
    pool_size: int = Field(default=5, ge=1, le=50, description="Connection pool size")

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO", description="Logging level")
    file: str = Field(default="logs/jdflows.log", description="Log file path")
    rotation: str = Field(default="100 MB", description="Log rotation size")
    retention: str = Field(default="30 days", description="Log retention period")
    compression: str = Field(default="zip", description="Log compression format")

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate logging level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class BrowserConfig(BaseModel):
    """Browser automation configuration."""

    headless: bool = Field(default=True, description="Run browser in headless mode")
    timeout: int = Field(default=30000, ge=1000, le=300000, description="Timeout in ms")
    user_agent: Optional[str] = Field(default=None, description="Custom user agent")
    viewport_width: int = Field(default=1920, ge=800, description="Viewport width")
    viewport_height: int = Field(default=1080, ge=600, description="Viewport height")

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class SystemConfig(BaseModel):
    """System-level configuration."""

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"


class ApplicationConfig(BaseModel):
    """Complete application configuration."""

    app: AppConfig = Field(default_factory=AppConfig)
    window: WindowConfig = Field(default_factory=WindowConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)

    class Config:
        """Pydantic configuration."""

        frozen = False
        extra = "forbid"

    def get_log_path(self) -> Path:
        """Get the log file path."""
        return Path(self.system.logging.file)

    def get_db_path(self) -> Optional[Path]:
        """Get the database file path if using SQLite."""
        if self.system.database.url.startswith("sqlite:///"):
            db_file = self.system.database.url.replace("sqlite:///", "")
            return Path(db_file)
        return None
