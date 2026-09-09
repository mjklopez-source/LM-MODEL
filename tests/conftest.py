"""Pytest configuration and fixtures."""

import pytest
import numpy as np
from pathlib import Path
import tempfile


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_data():
    """Provide sample training data."""
    np.random.seed(42)
    X = np.random.randn(10, 4)
    y = np.random.randint(0, 2, 10)
    return {"X": X, "y": y}


@pytest.fixture
def sample_params():
    """Provide sample parameters."""
    np.random.seed(42)
    return np.random.uniform(0, 2 * np.pi, 12)
