"""Tests for validators"""
from src.utils.validators import (
    is_valid_email,
    is_valid_url,
    is_valid_phone,
    is_valid_port,
    is_non_empty_string,
    is_positive_integer,
    is_valid_jd_product_id,
    is_valid_price,
    sanitize_filename,
    validate_dict_keys,
)


class TestValidators:
    """Tests for validation functions"""

    def test_is_valid_email(self):
        """Test email validation"""
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("invalid.email") is False
        assert is_valid_email("@example.com") is False

    def test_is_valid_url(self):
        """Test URL validation"""
        assert is_valid_url("https://www.example.com") is True
        assert is_valid_url("http://example.com") is True
        assert is_valid_url("not_a_url") is False

    def test_is_valid_phone(self):
        """Test phone number validation"""
        assert is_valid_phone("13800138000", "CN") is True
        assert is_valid_phone("12345678901", "CN") is False
        assert is_valid_phone("138001380001", "CN") is False

    def test_is_valid_port(self):
        """Test port validation"""
        assert is_valid_port(80) is True
        assert is_valid_port(8080) is True
        assert is_valid_port(0) is False
        assert is_valid_port(70000) is False

    def test_is_non_empty_string(self):
        """Test non-empty string check"""
        assert is_non_empty_string("test") is True
        assert is_non_empty_string("   ") is False
        assert is_non_empty_string("") is False
        assert is_non_empty_string(123) is False

    def test_is_positive_integer(self):
        """Test positive integer check"""
        assert is_positive_integer(1) is True
        assert is_positive_integer(100) is True
        assert is_positive_integer(0) is False
        assert is_positive_integer(-1) is False
        assert is_positive_integer(1.5) is False

    def test_is_valid_jd_product_id(self):
        """Test JD product ID validation"""
        assert is_valid_jd_product_id("1234567890") is True
        assert is_valid_jd_product_id("abc123") is False
        assert is_valid_jd_product_id("") is False

    def test_is_valid_price(self):
        """Test price validation"""
        assert is_valid_price(99.99) is True
        assert is_valid_price("199.99") is True
        assert is_valid_price(0) is False
        assert is_valid_price(-10) is False

    def test_sanitize_filename(self):
        """Test filename sanitization"""
        assert sanitize_filename("test.txt") == "test.txt"
        assert sanitize_filename("test:file.txt") == "test_file.txt"
        assert sanitize_filename("test/file.txt") == "test_file.txt"
        assert sanitize_filename("   ") == "unnamed"

    def test_validate_dict_keys(self):
        """Test dictionary key validation"""
        data = {"name": "test", "age": 25}
        assert validate_dict_keys(data, ["name", "age"]) is True
        assert validate_dict_keys(data, ["name", "email"]) is False
