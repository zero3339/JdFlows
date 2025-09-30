"""
Pytest Configuration and Global Fixtures

Provides common fixtures and configuration for all tests.
"""
import sys
from pathlib import Path

import pytest

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def mock_config():
    """Provide a mock configuration for testing."""
    return {
        "app": {"name": "JDFlows", "version": "0.1.0", "debug": True},
        "database": {"url": "sqlite:///:memory:"},
        "browser": {"headless": True, "timeout": 5000},
    }
