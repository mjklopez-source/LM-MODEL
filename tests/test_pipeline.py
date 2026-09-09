"""Tests for Pipeline class."""

import pytest
from quantum_llm.core.pipeline import Pipeline
from quantum_llm.core.node import Node


def add_func(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def multiply_func(x: int) -> int:
    """Multiply by 2."""
    return x * 2


def test_pipeline_creation():
    """Test creating a pipeline."""
    node1 = Node(add_func, inputs=["a", "b"], outputs=["sum"])
    node2 = Node(multiply_func, inputs=["sum"], outputs=["result"])

    pipeline = Pipeline([node1, node2])
    assert len(pipeline.nodes) == 2
    assert pipeline.name == "default"


def test_pipeline_with_custom_name():
    """Test pipeline with custom name."""
    node = Node(add_func, inputs=["a", "b"], outputs=["sum"])
    pipeline = Pipeline([node], name="custom_pipeline")
    assert pipeline.name == "custom_pipeline"


def test_pipeline_execution_order():
    """Test getting correct execution order."""
    node1 = Node(add_func, inputs=["a", "b"], outputs=["sum"])
    node2 = Node(multiply_func, inputs=["sum"], outputs=["result"])

    pipeline = Pipeline([node2, node1])  # Deliberately out of order
    order = pipeline.get_execution_order()

    assert order[0].name == "add_func"
    assert order[1].name == "multiply_func"


def test_pipeline_duplicate_names():
    """Test that duplicate node names raise error."""
    node1 = Node(add_func, inputs=["a", "b"], outputs=["sum"], name="node")
    node2 = Node(multiply_func, inputs=["sum"], outputs=["result"], name="node")

    with pytest.raises(ValueError):
        Pipeline([node1, node2])


def test_pipeline_circular_dependency():
    """Test detection of circular dependencies."""
    node1 = Node(lambda x: x, inputs=["b"], outputs=["a"])
    node2 = Node(lambda x: x, inputs=["a"], outputs=["b"])

    with pytest.raises(ValueError):
        Pipeline([node1, node2])


def test_pipeline_get_node_by_name():
    """Test getting node by name."""
    node = Node(add_func, inputs=["a", "b"], outputs=["sum"], name="adder")
    pipeline = Pipeline([node])

    found = pipeline.get_node_by_name("adder")
    assert found is not None
    assert found.name == "adder"


def test_pipeline_get_nodes_with_tag():
    """Test getting nodes by tag."""
    node1 = Node(add_func, inputs=["a", "b"], outputs=["sum"], tags={"preprocessing"})
    node2 = Node(multiply_func, inputs=["sum"], outputs=["result"], tags={"processing"})

    pipeline = Pipeline([node1, node2])
    preprocessing_nodes = pipeline.get_nodes_with_tag("preprocessing")

    assert len(preprocessing_nodes) == 1
    assert preprocessing_nodes[0].name == "add_func"


def test_pipeline_describe():
    """Test pipeline description."""
    node1 = Node(add_func, inputs=["a", "b"], outputs=["sum"])
    node2 = Node(multiply_func, inputs=["sum"], outputs=["result"])

    pipeline = Pipeline([node1, node2], name="test_pipeline")
    description = pipeline.describe()

    assert "test_pipeline" in description
    assert "add_func" in description
    assert "multiply_func" in description
