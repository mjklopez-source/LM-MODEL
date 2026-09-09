"""Data encoding strategies for quantum circuits."""

from typing import Any, List, Optional
from abc import ABC, abstractmethod
import numpy as np
from quantum_llm.quantum.backends.base import QuantumBackend


class DataEncoding(ABC):
    """Abstract base class for data encoding strategies."""

    def __init__(self, backend: QuantumBackend):
        """Initialize encoder.

        Args:
            backend: Quantum backend
        """
        self.backend = backend

    @abstractmethod
    def encode(self, circuit: Any, data: np.ndarray, qubits: List[int]) -> Any:
        """Encode data into quantum circuit.

        Args:
            circuit: Quantum circuit
            data: Data to encode
            qubits: Qubits to use for encoding

        Returns:
            Modified circuit
        """
        pass


class AngleEncoding(DataEncoding):
    """Encode data as rotation angles."""

    def encode(self, circuit: Any, data: np.ndarray, qubits: List[int]) -> Any:
        """Encode data as rotation angles."""
        if len(data) != len(qubits):
            raise ValueError(f"Data size {len(data)} doesn't match qubits {len(qubits)}")

        for qubit, value in zip(qubits, data):
            # Normalize value to [0, 2π]
            angle = np.pi * (value + 1) / 2
            self.backend.apply_ry_gate(circuit, qubit, angle)

        return circuit


class AmplitudeEncoding(DataEncoding):
    """Encode data as amplitudes in the quantum state."""

    def encode(self, circuit: Any, data: np.ndarray, qubits: List[int]) -> Any:
        """Encode data as amplitudes."""
        # Normalize data
        data_normalized = data / np.linalg.norm(data)

        # This is a simplified version - full implementation would use state preparation
        # For now, encode each element as a rotation
        n_qubits = len(qubits)
        n_data = len(data)

        if n_data != 2 ** n_qubits:
            raise ValueError(
                f"Data size {n_data} should be 2^{n_qubits} for amplitude encoding"
            )

        # Create rotation angles from amplitudes
        angles = 2 * np.arcsin(np.sqrt(np.abs(data_normalized)))

        for i, qubit in enumerate(qubits):
            if i < len(angles):
                self.backend.apply_ry_gate(circuit, qubit, angles[i])

        return circuit


class BasisEncoding(DataEncoding):
    """Encode data as computational basis states."""

    def encode(self, circuit: Any, data: np.ndarray, qubits: List[int]) -> Any:
        """Encode data as basis states."""
        # Binarize data
        binary_data = (data > 0).astype(int)

        if len(binary_data) != len(qubits):
            raise ValueError(
                f"Data size {len(binary_data)} doesn't match qubits {len(qubits)}"
            )

        # Apply X gates based on binary data
        for qubit, bit in zip(qubits, binary_data):
            if bit == 1:
                self.backend.apply_gate(circuit, "X", [qubit])

        return circuit


class IQPEncoding(DataEncoding):
    """Instantaneous Quantum Polynomial (IQP) encoding."""

    def encode(self, circuit: Any, data: np.ndarray, qubits: List[int]) -> Any:
        """Apply IQP encoding."""
        if len(data) != len(qubits):
            raise ValueError(f"Data size {len(data)} doesn't match qubits {len(qubits)}")

        # Hadamard layer
        for qubit in qubits:
            self.backend.apply_gate(circuit, "H", [qubit])

        # Diagonal gates
        for i, qubit in enumerate(qubits):
            angle = np.pi * data[i]
            self.backend.apply_rz_gate(circuit, qubit, angle)

        # Entangling layer
        for i, qubit in enumerate(qubits[:-1]):
            angle = np.pi * data[i] * data[i + 1]
            # Approximate two-qubit interaction
            self.backend.apply_cnot_gate(circuit, qubit, qubits[i + 1])
            self.backend.apply_rz_gate(circuit, qubits[i + 1], angle)
            self.backend.apply_cnot_gate(circuit, qubit, qubits[i + 1])

        return circuit


def get_encoding(name: str, backend: QuantumBackend) -> DataEncoding:
    """Get an encoding strategy by name.

    Args:
        name: Encoding name (angle, amplitude, basis, iqp)
        backend: Quantum backend

    Returns:
        Encoding instance

    Raises:
        ValueError: If encoding name is unknown
    """
    encodings = {
        "angle": AngleEncoding,
        "amplitude": AmplitudeEncoding,
        "basis": BasisEncoding,
        "iqp": IQPEncoding,
    }

    if name.lower() not in encodings:
        raise ValueError(f"Unknown encoding: {name}. Available: {list(encodings.keys())}")

    return encodings[name.lower()](backend)
