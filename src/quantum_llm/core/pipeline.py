"""
Pipeline orchestration for quantum LLM training.

Manages nodes, their dependencies, and execution order.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, deque
from quantum_llm.core.node import Node
import logging


logger = logging.getLogger(__name__)


class Pipeline:
    """Orchestrates a directed acyclic graph (DAG) of nodes.

    Similar to Kedro's Pipeline, this class manages:
    - Node registration
    - Dependency resolution
    - Execution order computation
    - Execution validation

    Attributes:
        nodes: List of nodes in the pipeline
        name: Optional pipeline name
    """

    def __init__(self, nodes: List[Node], name: Optional[str] = None):
        """Initialize a pipeline.

        Args:
            nodes: List of Node objects
            name: Optional pipeline name

        Raises:
            ValueError: If pipeline configuration is invalid
        """
        self.nodes = nodes
        self.name = name or "default"
        self._node_dict: Dict[str, Node] = {}
        self._validate()

    def _validate(self) -> None:
        """Validate pipeline configuration."""
        # Check for duplicate node names
        node_names = [n.name for n in self.nodes]
        if len(node_names) != len(set(node_names)):
            raise ValueError("Duplicate node names found in pipeline")

        # Build node dictionary
        for node in self.nodes:
            self._node_dict[node.name] = node
            node.validate_outputs()

        # Check for circular dependencies
        if self._has_circular_dependency():
            raise ValueError("Circular dependency detected in pipeline")

        # Validate input/output consistency
        self._validate_io_consistency()

    def _has_circular_dependency(self) -> bool:
        """Check if the pipeline has circular dependencies.

        Returns:
            True if a circular dependency is detected
        """
        visited = set()
        rec_stack = set()

        def has_cycle(node_name: str) -> bool:
            visited.add(node_name)
            rec_stack.add(node_name)

            node = self._node_dict[node_name]
            # Get names of nodes that this node depends on
            dependencies = set()
            for dep in node.inputs:
                for n in self.nodes:
                    if dep in n.outputs:
                        dependencies.add(n.name)

            for neighbor in dependencies:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node_name)
            return False

        for node_name in self._node_dict:
            if node_name not in visited:
                if has_cycle(node_name):
                    return True

        return False

    def _validate_io_consistency(self) -> None:
        """Validate that inputs match available outputs."""
        available_outputs = set()

        # Collect all available outputs from nodes
        for node in self.nodes:
            available_outputs.update(node.outputs)

        # Validate each node's inputs
        for node in self.nodes:
            for input_name in node.inputs:
                if input_name not in available_outputs:
                    # Check if it's an external input
                    is_external = True
                    for other_node in self.nodes:
                        if input_name in other_node.outputs:
                            is_external = False
                            break
                    if is_external:
                        logger.warning(
                            f"Node '{node.name}' requires external input '{input_name}'"
                        )

    def get_execution_order(self) -> List[Node]:
        """Get the execution order of nodes using topological sort.

        Returns:
            List of nodes in execution order

        Raises:
            ValueError: If the pipeline has cycles
        """
        if self._has_circular_dependency():
            raise ValueError("Cannot determine execution order: circular dependency detected")

        # Build adjacency list (who depends on whom)
        in_degree = {node.name: 0 for node in self.nodes}
        dependencies = defaultdict(list)

        # Get output providers
        output_providers = {}
        for node in self.nodes:
            for output in node.outputs:
                output_providers[output] = node.name

        # Build dependency graph
        for node in self.nodes:
            for input_name in node.inputs:
                if input_name in output_providers:
                    provider = output_providers[input_name]
                    if provider != node.name:
                        dependencies[provider].append(node.name)
                        in_degree[node.name] += 1

        # Kahn's algorithm for topological sort
        queue = deque([name for name in in_degree if in_degree[name] == 0])
        ordered_names = []

        while queue:
            current = queue.popleft()
            ordered_names.append(current)

            for dependent in dependencies[current]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Convert names back to nodes
        ordered_nodes = [self._node_dict[name] for name in ordered_names]

        if len(ordered_nodes) != len(self.nodes):
            raise ValueError("Topological sort failed: circular dependency detected")

        return ordered_nodes

    def get_node_by_name(self, name: str) -> Optional[Node]:
        """Get a node by its name.

        Args:
            name: Node name

        Returns:
            The node or None if not found
        """
        return self._node_dict.get(name)

    def get_nodes_with_tag(self, tag: str) -> List[Node]:
        """Get all nodes with a specific tag.

        Args:
            tag: Tag name

        Returns:
            List of nodes with the tag
        """
        return [node for node in self.nodes if tag in node.tags]

    def describe(self) -> str:
        """Get a string description of the pipeline.

        Returns:
            Formatted description
        """
        lines = [f"Pipeline: {self.name}"]
        lines.append(f"Nodes: {len(self.nodes)}")
        lines.append("\nExecution order:")

        try:
            ordered = self.get_execution_order()
            for i, node in enumerate(ordered, 1):
                inputs_str = ", ".join(node.inputs) if node.inputs else "none"
                outputs_str = ", ".join(node.outputs) if node.outputs else "none"
                lines.append(f"  {i}. {node.name}")
                lines.append(f"     Inputs: {inputs_str}")
                lines.append(f"     Outputs: {outputs_str}")
        except ValueError as e:
            lines.append(f"  Error: {e}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Pipeline(name='{self.name}', nodes={len(self.nodes)})"
