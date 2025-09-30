"""
Logger Initialization

Initializes and configures the Loguru-based logging system.
"""
import sys
from pathlib import Path
from typing import Optional, Any

from loguru import logger

from .config import LoggingConfig
from .exceptions import LoggingError


def setup_logger(
    config: Optional[LoggingConfig] = None,
    log_file: Optional[Path] = None,
    level: Optional[str] = None,
) -> None:
    """
    Configure the application logger.

    Args:
        config: Logging configuration object.
        log_file: Path to the log file (overrides config).
        level: Log level (overrides config).

    Raises:
        LoggingError: If logger setup fails.
    """
    try:
        # Remove default handler
        logger.remove()

        # Determine log level
        if level is None:
            level = config.level if config else "INFO"

        # Determine log file
        if log_file is None:
            log_file = Path(config.file) if config else Path("logs/jdflows.log")

        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Add console handler (stderr)
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=level,
            colorize=True,
        )

        # Add file handler
        rotation = config.rotation if config else "100 MB"
        retention = config.retention if config else "30 days"
        compression = config.compression if config else "zip"

        logger.add(
            str(log_file),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            encoding="utf-8",
        )

        logger.info(f"Logger initialized: level={level}, file={log_file}")

    except Exception as e:
        raise LoggingError(f"Failed to setup logger: {e}") from e


def get_logger(name: str) -> Any:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Logger instance bound to the specified name.
    """
    return logger.bind(name=name)


def disable_logger() -> None:
    """Disable all logging."""
    logger.disable("")


def enable_logger() -> None:
    """Enable all logging."""
    logger.enable("")
