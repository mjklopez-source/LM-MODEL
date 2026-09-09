"""
Node definition for pipeline nodes.

Similar to Kedro's node.py, defines individual processing units in the pipeline.
"""

from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass
from functools import wraps
import inspect


@dataclass
class Node:
    """Represents a single node in the pipeline.

    A node is a wrapper around a function that describes:
    - What the function does
    - What inputs it requires
    - What outputs it produces

    Attributes:
        func: The function to execute
        inputs: List of input names
        outputs: List of output names
        name: Optional node name (defaults to function name)
        tags: Optional tags for categorization
        confirm: Whether to confirm before execution
    """

    func: Callable
    inputs: List[str]
    outputs: List[str]
    name: Optional[str] = None
    tags: Optional[Set[str]] = None
    confirm: bool = False

    def __post_init__(self):
        """Initialize node after dataclass initialization."""
        if self.name is None:
            self.name = self.func.__name__
        if self.tags is None:
            self.tags = set()
        else:
            self.tags = set(self.tags)

    def __call__(self, *args, **kwargs) -> Any:
        """Execute the node's function."""
        return self.func(*args, **kwargs)

    def __repr__(self) -> str:
        return (
            f"Node(name='{self.name}', "
            f"inputs={self.inputs}, "
            f"outputs={self.outputs}, "
            f"tags={self.tags})"
        )

    @property
    def signature(self) -> inspect.Signature:
        """Get the function signature."""
        return inspect.signature(self.func)

    def validate_inputs(self, available_inputs: Set[str]) -> bool:
        """Validate that all required inputs are available.

        Args:
            available_inputs: Set of available input names

        Returns:
            True if all inputs are available

        Raises:
            ValueError: If any required input is missing
        """
        missing = set(self.inputs) - available_inputs
        if missing:
            raise ValueError(
                f"Node '{self.name}' requires inputs {missing} "
                f"but they are not available. Available: {available_inputs}"
            )
        return True

    def validate_outputs(self) -> bool:
        """Validate output configuration.

        Returns:
            True if outputs are valid

        Raises:
            ValueError: If outputs are invalid
        """
        if not self.outputs:
            raise ValueError(f"Node '{self.name}' has no outputs defined")

        if len(self.outputs) != len(set(self.outputs)):
            raise ValueError(
                f"Node '{self.name}' has duplicate output names: {self.outputs}"
            )

        return True

    def get_dependencies(self) -> Set[str]:
        """Get the set of input dependencies."""
        return set(self.inputs)

    def get_products(self) -> Set[str]:
        """Get the set of output products."""
        return set(self.outputs)


def node(
    func: Optional[Callable] = None,
    inputs: Optional[List[str]] = None,
    outputs: Optional[List[str]] = None,
    name: Optional[str] = None,
    tags: Optional[Set[str]] = None,
) -> Callable:
    """Decorator to convert a function into a Node.

    Example:
        @node(inputs=['data'], outputs=['processed_data'])
        def preprocess(data):
            return data * 2
    """
    def decorator(f: Callable) -> Node:
        return Node(
            func=f,
            inputs=inputs or [],
            outputs=outputs or [],
            name=name or f.__name__,
            tags=tags,
        )

    if func is None:
        return decorator
    else:
        return decorator(func)
