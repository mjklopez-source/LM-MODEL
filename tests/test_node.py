"""Tests for Node class."""

import pytest
from quantum_llm.core.node import Node, node


def dummy_func(x: int) -> int:
    """Dummy function for testing."""
    return x * 2


def test_node_creation():
    """Test creating a node."""
    n = Node(dummy_func, inputs=["a"], outputs=["b"])
    assert n.name == "dummy_func"
    assert n.inputs == ["a"]
    assert n.outputs == ["b"]


def test_node_with_custom_name():
    """Test creating a node with custom name."""
    n = Node(dummy_func, inputs=["a"], outputs=["b"], name="custom_node")
    assert n.name == "custom_node"


def test_node_with_tags():
    """Test creating a node with tags."""
    n = Node(dummy_func, inputs=["a"], outputs=["b"], tags={"preprocessing", "feature"})
    assert "preprocessing" in n.tags
    assert "feature" in n.tags


def test_node_validate_outputs():
    """Test output validation."""
    n = Node(dummy_func, inputs=["a"], outputs=[])
    with pytest.raises(ValueError):
        n.validate_outputs()


def test_node_duplicate_outputs():
    """Test that duplicate outputs raise error."""
    n = Node(dummy_func, inputs=["a"], outputs=["b", "b"])
    with pytest.raises(ValueError):
        n.validate_outputs()


def test_node_get_dependencies():
    """Test getting node dependencies."""
    n = Node(dummy_func, inputs=["a", "b"], outputs=["c"])
    deps = n.get_dependencies()
    assert "a" in deps
    assert "b" in deps


def test_node_decorator():
    """Test node decorator."""
    @node(inputs=["x"], outputs=["y"])
    def my_func(x):
        return x + 1

    assert isinstance(my_func, Node)
    assert my_func.inputs == ["x"]
    assert my_func.outputs == ["y"]


def test_node_call():
    """Test calling a node."""
    n = Node(dummy_func, inputs=["a"], outputs=["b"])
    result = n(5)
    assert result == 10
