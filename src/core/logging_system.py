"""
Advanced Logging System

Provides advanced logging features including context managers and decorators.
"""
import time
import functools
from typing import Callable, Any, Optional
from contextlib import contextmanager

from loguru import logger


@contextmanager
def log_context(message: str, level: str = "INFO") -> Any:
    """
    Context manager for logging entry and exit of a code block.

    Args:
        message: Description of the context.
        level: Log level.

    Yields:
        None

    Example:
        with log_context("Processing data"):
            # Your code here
            pass
    """
    start_time = time.time()
    logger.log(level, f"[START] {message}")
    try:
        yield
    except Exception as e:
        logger.error(f"[ERROR] {message}: {e}")
        raise
    finally:
        elapsed = time.time() - start_time
        logger.log(level, f"[END] {message} (took {elapsed:.2f}s)")


def log_execution(
    level: str = "DEBUG", log_args: bool = True, log_result: bool = True
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to log function execution.

    Args:
        level: Log level.
        log_args: Whether to log function arguments.
        log_result: Whether to log function return value.

    Returns:
        Decorated function.

    Example:
        @log_execution(level="INFO")
        def my_function(x, y):
            return x + y
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            # Log function call
            if log_args:
                args_repr = ", ".join([repr(a) for a in args])
                kwargs_repr = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
                all_args = ", ".join(filter(None, [args_repr, kwargs_repr]))
                logger.log(level, f"Calling {func_name}({all_args})")
            else:
                logger.log(level, f"Calling {func_name}")

            # Execute function
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                # Log result
                if log_result:
                    logger.log(
                        level,
                        f"{func_name} returned {result!r} (took {elapsed:.3f}s)",
                    )
                else:
                    logger.log(level, f"{func_name} completed (took {elapsed:.3f}s)")

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{func_name} raised {type(e).__name__}: {e} (took {elapsed:.3f}s)")
                raise

        return wrapper

    return decorator


def log_async_execution(
    level: str = "DEBUG", log_args: bool = True, log_result: bool = True
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to log async function execution.

    Args:
        level: Log level.
        log_args: Whether to log function arguments.
        log_result: Whether to log function return value.

    Returns:
        Decorated async function.

    Example:
        @log_async_execution(level="INFO")
        async def my_async_function(x, y):
            return x + y
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            # Log function call
            if log_args:
                args_repr = ", ".join([repr(a) for a in args])
                kwargs_repr = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
                all_args = ", ".join(filter(None, [args_repr, kwargs_repr]))
                logger.log(level, f"Calling async {func_name}({all_args})")
            else:
                logger.log(level, f"Calling async {func_name}")

            # Execute function
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start_time

                # Log result
                if log_result:
                    logger.log(
                        level,
                        f"{func_name} returned {result!r} (took {elapsed:.3f}s)",
                    )
                else:
                    logger.log(level, f"{func_name} completed (took {elapsed:.3f}s)")

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{func_name} raised {type(e).__name__}: {e} (took {elapsed:.3f}s)")
                raise

        return wrapper

    return decorator


class PerformanceLogger:
    """Logger for performance monitoring."""

    def __init__(self, name: str, threshold: float = 1.0) -> None:
        """
        Initialize the performance logger.

        Args:
            name: Name of the operation being monitored.
            threshold: Time threshold in seconds to trigger warning.
        """
        self.name = name
        self.threshold = threshold
        self.start_time: Optional[float] = None

    def __enter__(self) -> "PerformanceLogger":
        """Start timing."""
        self.start_time = time.time()
        logger.debug(f"[PERF] Starting: {self.name}")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop timing and log."""
        if self.start_time is not None:
            elapsed = time.time() - self.start_time

            if elapsed >= self.threshold:
                logger.warning(
                    f"[PERF] {self.name} took {elapsed:.3f}s (threshold: {self.threshold}s)"
                )
            else:
                logger.debug(f"[PERF] {self.name} took {elapsed:.3f}s")
