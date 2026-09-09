"""Base backend interface for quantum computing."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


class QuantumBackend(ABC):
    """Abstract base class for quantum backends.

    Defines the interface that all quantum backends must implement.
    """

    def __init__(self, name: str, **kwargs):
        """Initialize backend.

        Args:
            name: Backend name
            **kwargs: Backend-specific configuration
        """
        self.name = name
        self.config = kwargs

    @abstractmethod
    def create_circuit(self, n_qubits: int, name: str = "circuit") -> Any:
        """Create an empty quantum circuit.

        Args:
            n_qubits: Number of qubits
            name: Circuit name

        Returns:
            Quantum circuit object
        """
        pass

    @abstractmethod
    def apply_gate(self, circuit: Any, gate: str, qubits: List[int]) -> Any:
        """Apply a quantum gate to a circuit.

        Args:
            circuit: Quantum circuit
            gate: Gate name (X, Y, Z, H, CNOT, etc.)
            qubits: Qubits to apply gate to

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def apply_rx_gate(self, circuit: Any, qubit: int, angle: float) -> Any:
        """Apply RX rotation gate.

        Args:
            circuit: Quantum circuit
            qubit: Target qubit
            angle: Rotation angle in radians

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def apply_ry_gate(self, circuit: Any, qubit: int, angle: float) -> Any:
        """Apply RY rotation gate.

        Args:
            circuit: Quantum circuit
            qubit: Target qubit
            angle: Rotation angle in radians

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def apply_rz_gate(self, circuit: Any, qubit: int, angle: float) -> Any:
        """Apply RZ rotation gate.

        Args:
            circuit: Quantum circuit
            qubit: Target qubit
            angle: Rotation angle in radians

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def apply_cnot_gate(self, circuit: Any, control: int, target: int) -> Any:
        """Apply CNOT (CX) gate.

        Args:
            circuit: Quantum circuit
            control: Control qubit
            target: Target qubit

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def measure(self, circuit: Any, qubits: Optional[List[int]] = None) -> Any:
        """Add measurement to circuit.

        Args:
            circuit: Quantum circuit
            qubits: Qubits to measure (all if None)

        Returns:
            Modified circuit
        """
        pass

    @abstractmethod
    def execute(
        self, circuit: Any, shots: int = 1024
    ) -> Dict[str, int]:
        """Execute circuit and get measurement results.

        Args:
            circuit: Quantum circuit
            shots: Number of shots to run

        Returns:
            Dictionary mapping bitstrings to counts
        """
        pass

    @abstractmethod
    def get_statevector(self, circuit: Any) -> np.ndarray:
        """Get the statevector of a circuit.

        Args:
            circuit: Quantum circuit

        Returns:
            State vector as numpy array
        """
        pass

    @abstractmethod
    def get_unitary(self, circuit: Any) -> np.ndarray:
        """Get the unitary matrix of a circuit.

        Args:
            circuit: Quantum circuit

        Returns:
            Unitary matrix as numpy array
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
