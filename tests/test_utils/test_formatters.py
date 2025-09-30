"""Tests for formatters"""
from src.utils.formatters import (
    format_price,
    format_number,
    format_percentage,
    format_duration,
    format_file_size,
    truncate_text,
    format_boolean,
    format_phone_number,
    capitalize_words,
)


class TestFormatters:
    """Tests for formatting functions"""

    def test_format_price(self):
        """Test price formatting"""
        assert format_price(99.99) == "¥99.99"
        assert format_price(100, currency="$") == "$100.00"
        assert format_price("invalid") == "¥0.00"

    def test_format_number(self):
        """Test number formatting"""
        assert format_number(1000) == "1,000"
        assert format_number(1000000) == "1,000,000"
        assert format_number(1000, separator=" ") == "1 000"

    def test_format_percentage(self):
        """Test percentage formatting"""
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(0.123, decimals=2) == "12.30%"

    def test_format_duration(self):
        """Test duration formatting"""
        assert format_duration(30) == "30s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(3661) == "1h 1m"

    def test_format_file_size(self):
        """Test file size formatting"""
        assert format_file_size(100) == "100.00 B"
        assert format_file_size(1024) == "1.00 KB"
        assert format_file_size(1048576) == "1.00 MB"

    def test_truncate_text(self):
        """Test text truncation"""
        assert truncate_text("Hello World", 20) == "Hello World"
        assert truncate_text("Hello World", 8) == "Hello..."
        assert truncate_text("Hello World", 8, suffix="..") == "Hello .."

    def test_format_boolean(self):
        """Test boolean formatting"""
        assert format_boolean(True) == "Yes"
        assert format_boolean(False) == "No"
        assert format_boolean(True, "On", "Off") == "On"

    def test_format_phone_number(self):
        """Test phone number formatting"""
        assert format_phone_number("13800138000", "CN") == "138 0013 8000"
        assert format_phone_number("12345", "CN") == "12345"

    def test_capitalize_words(self):
        """Test word capitalization"""
        assert capitalize_words("hello world") == "Hello World"
        assert capitalize_words("test") == "Test"
