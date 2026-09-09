"""Quantum backend implementations."""

from quantum_llm.quantum.backends.base import QuantumBackend
from quantum_llm.quantum.backends.qiskit_backend import QiskitBackend
from quantum_llm.quantum.backends.pennylane_backend import PennyLaneBackend

__all__ = ["QuantumBackend", "QiskitBackend", "PennyLaneBackend"]


def get_backend(name: str, **kwargs) -> QuantumBackend:
    """Factory function to get a quantum backend.

    Args:
        name: Backend name (qiskit, pennylane, cirq)
        **kwargs: Backend configuration

    Returns:
        Backend instance

    Raises:
        ValueError: If backend name is unknown
    """
    backends = {
        "qiskit": QiskitBackend,
        "pennylane": PennyLaneBackend,
    }

    if name.lower() not in backends:
        raise ValueError(f"Unknown backend: {name}. Available: {list(backends.keys())}")

    return backends[name.lower()](**kwargs)
