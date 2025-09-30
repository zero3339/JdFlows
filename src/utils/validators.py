"""
Data Validators

Provides validation functions for various data types.
"""
import re
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse


def is_valid_email(email: str) -> bool:
    """
    Validate an email address.

    Args:
        email: Email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """
    Validate a URL.

    Args:
        url: URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_phone(phone: str, region: str = "CN") -> bool:
    """
    Validate a phone number.

    Args:
        phone: Phone number to validate.
        region: Region code (default: CN for China).

    Returns:
        bool: True if valid, False otherwise.
    """
    # Simple Chinese phone number validation
    if region == "CN":
        pattern = r"^1[3-9]\d{9}$"
        return bool(re.match(pattern, phone))
    return False


def is_valid_path(path: str) -> bool:
    """
    Validate a file system path.

    Args:
        path: Path to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        Path(path)
        return True
    except Exception:
        return False


def is_valid_port(port: int) -> bool:
    """
    Validate a network port number.

    Args:
        port: Port number to validate.

    Returns:
        bool: True if valid (1-65535), False otherwise.
    """
    return 1 <= port <= 65535


def is_non_empty_string(value: Any) -> bool:
    """
    Check if a value is a non-empty string.

    Args:
        value: Value to check.

    Returns:
        bool: True if non-empty string, False otherwise.
    """
    return isinstance(value, str) and len(value.strip()) > 0


def is_positive_integer(value: Any) -> bool:
    """
    Check if a value is a positive integer.

    Args:
        value: Value to check.

    Returns:
        bool: True if positive integer, False otherwise.
    """
    return isinstance(value, int) and value > 0


def is_non_negative_integer(value: Any) -> bool:
    """
    Check if a value is a non-negative integer.

    Args:
        value: Value to check.

    Returns:
        bool: True if non-negative integer, False otherwise.
    """
    return isinstance(value, int) and value >= 0


def is_in_range(value: float, min_val: float, max_val: float) -> bool:
    """
    Check if a value is within a specified range.

    Args:
        value: Value to check.
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).

    Returns:
        bool: True if in range, False otherwise.
    """
    return min_val <= value <= max_val


def validate_string_length(
    value: str, min_length: Optional[int] = None, max_length: Optional[int] = None
) -> bool:
    """
    Validate string length.

    Args:
        value: String to validate.
        min_length: Minimum length (inclusive), or None for no minimum.
        max_length: Maximum length (inclusive), or None for no maximum.

    Returns:
        bool: True if valid, False otherwise.
    """
    length = len(value)

    if min_length is not None and length < min_length:
        return False

    if max_length is not None and length > max_length:
        return False

    return True


def is_valid_jd_product_id(product_id: str) -> bool:
    """
    Validate a JD.com product ID.

    Args:
        product_id: Product ID to validate.

    Returns:
        bool: True if valid, False otherwise.

    Note:
        JD product IDs are typically numeric strings.
    """
    return bool(re.match(r"^\d+$", product_id))


def is_valid_price(price: Any) -> bool:
    """
    Validate a price value.

    Args:
        price: Price value to validate.

    Returns:
        bool: True if valid (positive number), False otherwise.
    """
    try:
        price_float = float(price)
        return price_float > 0
    except (ValueError, TypeError):
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Filename to sanitize.

    Returns:
        str: Sanitized filename.
    """
    # Remove invalid characters for Windows/Unix filesystems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, "_", filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip().strip(".")

    # Ensure filename is not empty
    if not sanitized:
        sanitized = "unnamed"

    return sanitized


def validate_dict_keys(data: dict[str, Any], required_keys: list[str]) -> bool:
    """
    Validate that a dictionary contains all required keys.

    Args:
        data: Dictionary to validate.
        required_keys: List of required keys.

    Returns:
        bool: True if all keys present, False otherwise.
    """
    return all(key in data for key in required_keys)
