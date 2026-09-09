"""
QuantumLLM - Quantum Computing Library for LLM Training

A modern Python library for training Language Models using quantum computing,
inspired by Kedro's architecture and best practices.
"""

__version__ = "0.1.0"
__author__ = "QuantumLLM Team"

from quantum_llm.core.node import Node
from quantum_llm.core.pipeline import Pipeline
from quantum_llm.core.runner import PipelineRunner
from quantum_llm.config.settings import Settings
from quantum_llm.config.logger import setup_logger

__all__ = [
    "Node",
    "Pipeline",
    "PipelineRunner",
    "Settings",
    "setup_logger",
]
