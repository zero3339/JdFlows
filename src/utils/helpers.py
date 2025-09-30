"""
Helper Utilities

Provides general-purpose utility functions.
"""
import hashlib
import json
import os
import platform
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json_file(file_path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
        return data


def write_json_file(file_path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """Write data to a JSON file."""
    ensure_dir(file_path.parent)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def compute_string_hash(text: str, algorithm: str = "sha256") -> str:
    """Compute the hash of a string."""
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def get_system_info() -> Dict[str, str]:
    """Get system information."""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "python_version": platform.python_version(),
    }


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Optional[Any]:
    """Safely get a value from a dictionary."""
    return dictionary.get(key, default)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries."""
    result: Dict[str, Any] = {}
    for d in dicts:
        result.update(d)
    return result
