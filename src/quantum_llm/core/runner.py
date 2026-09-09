"""
Pipeline runner for executing nodes in the correct order.
"""

from typing import Any, Dict, Optional, List
from quantum_llm.core.pipeline import Pipeline
from quantum_llm.core.node import Node
import logging
from datetime import datetime
import time


logger = logging.getLogger(__name__)


class PipelineRunner:
    """Executes a pipeline of nodes.

    Manages execution flow, handles node inputs/outputs, and provides
    execution tracking and reporting.

    Attributes:
        pipeline: The pipeline to execute
        dry_run: If True, only validates without executing
    """

    def __init__(self, pipeline: Pipeline, dry_run: bool = False):
        """Initialize the pipeline runner.

        Args:
            pipeline: Pipeline instance
            dry_run: If True, validates without executing
        """
        self.pipeline = pipeline
        self.dry_run = dry_run
        self.execution_report: Dict[str, Any] = {}

    def run(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the pipeline.

        Args:
            inputs: Dictionary of external inputs to the pipeline

        Returns:
            Dictionary of all outputs produced by the pipeline

        Raises:
            RuntimeError: If execution fails
        """
        inputs = inputs or {}
        context: Dict[str, Any] = dict(inputs)

        logger.info(f"Starting pipeline execution: {self.pipeline.name}")
        start_time = datetime.now()

        try:
            # Get execution order
            ordered_nodes = self.pipeline.get_execution_order()
            logger.info(f"Pipeline has {len(ordered_nodes)} nodes to execute")

            if self.dry_run:
                logger.info("Running in DRY RUN mode - no actual execution")
                return self._dry_run(ordered_nodes, context)

            # Execute nodes
            for i, node in enumerate(ordered_nodes, 1):
                logger.info(f"Executing node {i}/{len(ordered_nodes)}: {node.name}")
                self._execute_node(node, context)

            # Collect outputs
            outputs = self._extract_outputs(context, ordered_nodes)

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Pipeline completed successfully in {elapsed:.2f}s")

            self.execution_report = {
                "status": "success",
                "pipeline": self.pipeline.name,
                "nodes_executed": len(ordered_nodes),
                "execution_time": elapsed,
                "timestamp": start_time.isoformat(),
            }

            return outputs

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.error(f"Pipeline execution failed after {elapsed:.2f}s: {e}")

            self.execution_report = {
                "status": "failed",
                "pipeline": self.pipeline.name,
                "error": str(e),
                "execution_time": elapsed,
                "timestamp": start_time.isoformat(),
            }

            raise RuntimeError(f"Pipeline execution failed: {e}") from e

    def _execute_node(self, node: Node, context: Dict[str, Any]) -> None:
        """Execute a single node.

        Args:
            node: Node to execute
            context: Current execution context (modified in-place)

        Raises:
            RuntimeError: If node execution fails
        """
        try:
            # Collect inputs
            node_inputs = {}
            for input_name in node.inputs:
                if input_name not in context:
                    raise ValueError(
                        f"Required input '{input_name}' not found in context. "
                        f"Available: {list(context.keys())}"
                    )
                node_inputs[input_name] = context[input_name]

            logger.debug(f"Node '{node.name}' inputs: {list(node_inputs.keys())}")

            # Execute node
            start_time = time.time()
            if len(node_inputs) == 1 and len(node.outputs) == 1:
                # Single input/output case
                result = node(list(node_inputs.values())[0])
            elif len(node_inputs) == 1:
                # Single input, multiple outputs
                result = node(list(node_inputs.values())[0])
            else:
                # Multiple inputs
                result = node(**node_inputs)

            elapsed = time.time() - start_time

            # Store outputs
            if len(node.outputs) == 1:
                context[node.outputs[0]] = result
            else:
                # Multiple outputs - expect tuple/list
                if not isinstance(result, (tuple, list)):
                    raise ValueError(
                        f"Node '{node.name}' expected multiple outputs "
                        f"but returned {type(result).__name__}"
                    )
                if len(result) != len(node.outputs):
                    raise ValueError(
                        f"Node '{node.name}' returned {len(result)} outputs "
                        f"but expected {len(node.outputs)}"
                    )
                for output_name, output_value in zip(node.outputs, result):
                    context[output_name] = output_value

            logger.debug(
                f"Node '{node.name}' completed in {elapsed:.3f}s. "
                f"Outputs: {node.outputs}"
            )

        except Exception as e:
            raise RuntimeError(f"Node '{node.name}' execution failed: {e}") from e

    def _extract_outputs(self, context: Dict[str, Any], nodes: List[Node]) -> Dict[str, Any]:
        """Extract final outputs from context.

        Args:
            context: Execution context
            nodes: Executed nodes

        Returns:
            Dictionary of final outputs
        """
        # Get outputs from the last node(s) or all outputs
        outputs = {}
        for node in nodes:
            for output_name in node.outputs:
                if output_name in context:
                    outputs[output_name] = context[output_name]

        return outputs

    def _dry_run(
        self, ordered_nodes: List[Node], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform a dry run without actually executing nodes.

        Args:
            ordered_nodes: Nodes in execution order
            context: Execution context

        Returns:
            Validation results
        """
        logger.info("Validating pipeline structure...")

        for node in ordered_nodes:
            logger.info(f"Validating node: {node.name}")

            # Check inputs
            for input_name in node.inputs:
                if input_name not in context:
                    logger.warning(
                        f"Node '{node.name}' requires input '{input_name}' "
                        f"which is not available"
                    )

        logger.info("Dry run validation completed")
        return {"status": "dry_run", "nodes_validated": len(ordered_nodes)}

    def get_report(self) -> Dict[str, Any]:
        """Get the execution report.

        Returns:
            Execution report dictionary
        """
        return self.execution_report
