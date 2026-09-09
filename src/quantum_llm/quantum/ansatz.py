"""Quantum circuit ansatz patterns for variational quantum algorithms."""

from typing import Any, List, Optional
from abc import ABC, abstractmethod
from quantum_llm.quantum.backends.base import QuantumBackend
import numpy as np


class Ansatz(ABC):
    """Abstract base class for quantum circuit ansatz."""

    def __init__(self, n_qubits: int, n_layers: int, backend: QuantumBackend):
        """Initialize ansatz.

        Args:
            n_qubits: Number of qubits
            n_layers: Number of layers
            backend: Quantum backend
        """
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.backend = backend
        self.n_params = self._calculate_n_params()

    @abstractmethod
    def _calculate_n_params(self) -> int:
        """Calculate number of parameters needed."""
        pass

    @abstractmethod
    def build(self, params: np.ndarray) -> Any:
        """Build the circuit with given parameters.

        Args:
            params: Parameter array

        Returns:
            Quantum circuit
        """
        pass


class BasicAnsatz(Ansatz):
    """Basic ansatz with single qubit rotations and entanglement."""

    def _calculate_n_params(self) -> int:
        """Calculate number of parameters: 3 * n_qubits per layer."""
        return 3 * self.n_qubits * self.n_layers

    def build(self, params: np.ndarray) -> Any:
        """Build basic ansatz circuit."""
        if len(params) != self.n_params:
            raise ValueError(
                f"Expected {self.n_params} parameters but got {len(params)}"
            )

        circuit = self.backend.create_circuit(self.n_qubits, "basic_ansatz")

        idx = 0
        for layer in range(self.n_layers):
            # Single qubit rotations
            for qubit in range(self.n_qubits):
                self.backend.apply_rx_gate(circuit, qubit, params[idx])
                self.backend.apply_ry_gate(circuit, qubit, params[idx + 1])
                self.backend.apply_rz_gate(circuit, qubit, params[idx + 2])
                idx += 3

            # Entangling layer
            for qubit in range(self.n_qubits - 1):
                self.backend.apply_cnot_gate(circuit, qubit, qubit + 1)

        return circuit


class CircularAnsatz(Ansatz):
    """Ansatz with circular entanglement pattern."""

    def _calculate_n_params(self) -> int:
        """Calculate number of parameters."""
        return 3 * self.n_qubits * self.n_layers

    def build(self, params: np.ndarray) -> Any:
        """Build circular ansatz circuit."""
        if len(params) != self.n_params:
            raise ValueError(
                f"Expected {self.n_params} parameters but got {len(params)}"
            )

        circuit = self.backend.create_circuit(self.n_qubits, "circular_ansatz")

        idx = 0
        for layer in range(self.n_layers):
            # Single qubit rotations
            for qubit in range(self.n_qubits):
                self.backend.apply_ry_gate(circuit, qubit, params[idx])
                self.backend.apply_rz_gate(circuit, qubit, params[idx + 1])
                idx += 2

            # Circular entanglement
            for qubit in range(self.n_qubits):
                next_qubit = (qubit + 1) % self.n_qubits
                self.backend.apply_cnot_gate(circuit, qubit, next_qubit)

        return circuit

    def _calculate_n_params(self) -> int:
        """Calculate number of parameters."""
        return 2 * self.n_qubits * self.n_layers


class HardwareEfficientAnsatz(Ansatz):
    """Hardware-efficient ansatz suitable for NISQ devices."""

    def _calculate_n_params(self) -> int:
        """Calculate number of parameters."""
        return 2 * self.n_qubits * self.n_layers

    def build(self, params: np.ndarray) -> Any:
        """Build hardware-efficient ansatz."""
        if len(params) != self.n_params:
            raise ValueError(
                f"Expected {self.n_params} parameters but got {len(params)}"
            )

        circuit = self.backend.create_circuit(self.n_qubits, "hardware_efficient")

        idx = 0
        for layer in range(self.n_layers):
            # Parallel single qubit rotations
            for qubit in range(self.n_qubits):
                self.backend.apply_ry_gate(circuit, qubit, params[idx])
                self.backend.apply_rz_gate(circuit, qubit, params[idx + 1])
                idx += 2

            # Entanglement: alternating pattern
            for qubit in range(0 if layer % 2 == 0 else 1, self.n_qubits - 1, 2):
                self.backend.apply_cnot_gate(circuit, qubit, qubit + 1)

        return circuit


class RotationalAnsatz(Ansatz):
    """Ansatz with only rotational gates."""

    def _calculate_n_params(self) -> int:
        """Calculate number of parameters."""
        return self.n_qubits * self.n_layers

    def build(self, params: np.ndarray) -> Any:
        """Build rotational ansatz."""
        if len(params) != self.n_params:
            raise ValueError(
                f"Expected {self.n_params} parameters but got {len(params)}"
            )

        circuit = self.backend.create_circuit(self.n_qubits, "rotational")

        idx = 0
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                self.backend.apply_ry_gate(circuit, qubit, params[idx])
                idx += 1

        return circuit


def get_ansatz(
    name: str, n_qubits: int, n_layers: int, backend: QuantumBackend
) -> Ansatz:
    """Get an ansatz by name.

    Args:
        name: Ansatz name
        n_qubits: Number of qubits
        n_layers: Number of layers
        backend: Quantum backend

    Returns:
        Ansatz instance

    Raises:
        ValueError: If ansatz name is unknown
    """
    ansatze = {
        "basic": BasicAnsatz,
        "circular": CircularAnsatz,
        "hardware_efficient": HardwareEfficientAnsatz,
        "rotational": RotationalAnsatz,
    }

    if name.lower() not in ansatze:
        raise ValueError(f"Unknown ansatz: {name}. Available: {list(ansatze.keys())}")

    return ansatze[name.lower()](n_qubits, n_layers, backend)
