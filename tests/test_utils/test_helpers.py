"""Tests for helper utilities"""
from src.utils.helpers import (
    ensure_dir,
    compute_string_hash,
    truncate_string,
    safe_get,
    merge_dicts,
    format_file_size,
    get_system_info,
)


class TestHelpers:
    """Tests for helper functions"""

    def test_ensure_dir(self, tmp_path):
        """Test directory creation"""
        test_dir = tmp_path / "test" / "nested"
        result = ensure_dir(test_dir)

        assert result.exists()
        assert result.is_dir()

    def test_compute_string_hash(self):
        """Test string hashing"""
        hash1 = compute_string_hash("test")
        hash2 = compute_string_hash("test")
        hash3 = compute_string_hash("different")

        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64  # SHA256 produces 64 hex characters

    def test_truncate_string(self):
        """Test string truncation"""
        assert truncate_string("Hello World", 20) == "Hello World"
        assert truncate_string("Hello World", 8) == "Hello..."
        assert truncate_string("Test", 10) == "Test"

    def test_safe_get(self):
        """Test safe dictionary access"""
        data = {"key": "value"}

        assert safe_get(data, "key") == "value"
        assert safe_get(data, "missing") is None
        assert safe_get(data, "missing", "default") == "default"

    def test_merge_dicts(self):
        """Test dictionary merging"""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3}
        dict3 = {"b": 4, "d": 5}

        result = merge_dicts(dict1, dict2, dict3)

        assert result["a"] == 1
        assert result["b"] == 4  # Later dict overwrites
        assert result["c"] == 3
        assert result["d"] == 5

    def test_format_file_size(self):
        """Test file size formatting"""
        assert format_file_size(100) == "100.00 B"
        assert format_file_size(2048) == "2.00 KB"
        assert format_file_size(1048576) == "1.00 MB"

    def test_get_system_info(self):
        """Test system information retrieval"""
        info = get_system_info()

        assert "platform" in info
        assert "python_version" in info
        assert isinstance(info, dict)
