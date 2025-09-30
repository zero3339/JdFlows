"""
Data Formatters

Provides formatting functions for various data types.
"""
from datetime import datetime
from typing import Any, Optional, Union
from decimal import Decimal


def format_price(
    price: Union[int, float, Decimal, str], currency: str = "¥", decimals: int = 2
) -> str:
    """
    Format a price value.

    Args:
        price: Price value.
        currency: Currency symbol.
        decimals: Number of decimal places.

    Returns:
        str: Formatted price string.
    """
    try:
        price_float = float(price)
        return f"{currency}{price_float:.{decimals}f}"
    except (ValueError, TypeError):
        return f"{currency}0.00"


def format_number(number: Union[int, float], separator: str = ",") -> str:
    """
    Format a number with thousand separators.

    Args:
        number: Number to format.
        separator: Thousand separator.

    Returns:
        str: Formatted number string.
    """
    return f"{number:,}".replace(",", separator)


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a value as a percentage.

    Args:
        value: Value to format (0.0 to 1.0).
        decimals: Number of decimal places.

    Returns:
        str: Formatted percentage string.
    """
    return f"{value * 100:.{decimals}f}%"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Format a duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds.

    Returns:
        str: Formatted duration (e.g., "1h 23m 45s").
    """
    if seconds < 60:
        return f"{seconds:.0f}s"

    minutes = seconds // 60
    remaining_seconds = seconds % 60

    if minutes < 60:
        return f"{minutes:.0f}m {remaining_seconds:.0f}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours:.0f}h {remaining_minutes:.0f}m"


def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object.

    Args:
        dt: Datetime object.
        format_string: Format string.

    Returns:
        str: Formatted datetime string.
    """
    return dt.strftime(format_string)


def format_relative_time(dt: datetime) -> str:
    """
    Format a datetime as relative time (e.g., "2 hours ago").

    Args:
        dt: Datetime object.

    Returns:
        str: Relative time string.
    """
    now = datetime.now()
    delta = now - dt

    if delta.days > 365:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"

    if delta.days > 30:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"

    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"

    if delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"

    if delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"

    return "just now"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes.

    Returns:
        str: Formatted file size (e.g., "1.5 MB").
    """
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate.
        max_length: Maximum length.
        suffix: Suffix to append if truncated.

    Returns:
        str: Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_list(items: list[Any], separator: str = ", ", max_items: Optional[int] = None) -> str:
    """
    Format a list as a string.

    Args:
        items: List of items.
        separator: Separator between items.
        max_items: Maximum number of items to display.

    Returns:
        str: Formatted list string.
    """
    if max_items and len(items) > max_items:
        displayed = items[:max_items]
        remaining = len(items) - max_items
        items_str = separator.join(str(item) for item in displayed)
        return f"{items_str}{separator}and {remaining} more"

    return separator.join(str(item) for item in items)


def format_json(data: Any, indent: int = 2) -> str:
    """
    Format data as pretty-printed JSON.

    Args:
        data: Data to format.
        indent: Indentation level.

    Returns:
        str: Formatted JSON string.
    """
    import json

    return json.dumps(data, indent=indent, ensure_ascii=False)


def format_boolean(value: bool, true_text: str = "Yes", false_text: str = "No") -> str:
    """
    Format a boolean value as text.

    Args:
        value: Boolean value.
        true_text: Text for True.
        false_text: Text for False.

    Returns:
        str: Formatted boolean text.
    """
    return true_text if value else false_text


def format_phone_number(phone: str, region: str = "CN") -> str:
    """
    Format a phone number.

    Args:
        phone: Phone number.
        region: Region code.

    Returns:
        str: Formatted phone number.
    """
    # Remove all non-digit characters
    digits = "".join(filter(str.isdigit, phone))

    # Format Chinese mobile numbers
    if region == "CN" and len(digits) == 11:
        return f"{digits[:3]} {digits[3:7]} {digits[7:]}"

    return phone


def capitalize_words(text: str) -> str:
    """
    Capitalize the first letter of each word.

    Args:
        text: Text to capitalize.

    Returns:
        str: Capitalized text.
    """
    return " ".join(word.capitalize() for word in text.split())
