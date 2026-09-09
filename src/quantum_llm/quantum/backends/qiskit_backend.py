"""Qiskit backend implementation."""

from typing import Any, Dict, List, Optional
import numpy as np
from quantum_llm.quantum.backends.base import QuantumBackend

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit_aer import AerSimulator
    from qiskit.circuit import Parameter
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False


class QiskitBackend(QuantumBackend):
    """Qiskit quantum backend implementation."""

    def __init__(self, simulator: str = "statevector", **kwargs):
        """Initialize Qiskit backend.

        Args:
            simulator: Simulator type (statevector, automatic, density_matrix, etc.)
            **kwargs: Additional configuration
        """
        if not HAS_QISKIT:
            raise ImportError("Qiskit is not installed. Install with: pip install qiskit")

        super().__init__("qiskit", **kwargs)
        self.simulator_type = simulator
        # Map old names to new Aer simulator methods
        method_map = {
            "qasm_simulator": "automatic",
            "statevector_simulator": "statevector",
            "unitary_simulator": "unitary",
        }
        method = method_map.get(simulator, simulator)
        self.simulator = AerSimulator(method=method)

    def create_circuit(self, n_qubits: int, name: str = "circuit") -> QuantumCircuit:
        """Create a quantum circuit."""
        qreg = QuantumRegister(n_qubits, "q")
        creg = ClassicalRegister(n_qubits, "c")
        circuit = QuantumCircuit(qreg, creg, name=name)
        return circuit

    def apply_gate(self, circuit: QuantumCircuit, gate: str, qubits: List[int]) -> QuantumCircuit:
        """Apply a quantum gate."""
        gate_upper = gate.upper()

        if gate_upper == "H":
            for q in qubits:
                circuit.h(q)
        elif gate_upper == "X":
            for q in qubits:
                circuit.x(q)
        elif gate_upper == "Y":
            for q in qubits:
                circuit.y(q)
        elif gate_upper == "Z":
            for q in qubits:
                circuit.z(q)
        elif gate_upper == "S":
            for q in qubits:
                circuit.s(q)
        elif gate_upper == "T":
            for q in qubits:
                circuit.t(q)
        elif gate_upper == "CNOT" or gate_upper == "CX":
            if len(qubits) >= 2:
                circuit.cx(qubits[0], qubits[1])
        else:
            raise ValueError(f"Unknown gate: {gate}")

        return circuit

    def apply_rx_gate(self, circuit: QuantumCircuit, qubit: int, angle: float) -> QuantumCircuit:
        """Apply RX rotation gate."""
        circuit.rx(angle, qubit)
        return circuit

    def apply_ry_gate(self, circuit: QuantumCircuit, qubit: int, angle: float) -> QuantumCircuit:
        """Apply RY rotation gate."""
        circuit.ry(angle, qubit)
        return circuit

    def apply_rz_gate(self, circuit: QuantumCircuit, qubit: int, angle: float) -> QuantumCircuit:
        """Apply RZ rotation gate."""
        circuit.rz(angle, qubit)
        return circuit

    def apply_cnot_gate(self, circuit: QuantumCircuit, control: int, target: int) -> QuantumCircuit:
        """Apply CNOT gate."""
        circuit.cx(control, target)
        return circuit

    def measure(
        self, circuit: QuantumCircuit, qubits: Optional[List[int]] = None
    ) -> QuantumCircuit:
        """Add measurement to circuit."""
        if qubits is None:
            qubits = list(range(circuit.num_qubits))

        circuit.measure(qubits, qubits)
        return circuit

    def execute(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict[str, int]:
        """Execute circuit and return measurement results."""
        # Ensure circuit has measurements
        if circuit.num_clbits == 0:
            circuit = circuit.copy()
            self.measure(circuit)

        job = self.simulator.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()

        return counts

    def get_statevector(self, circuit: QuantumCircuit) -> np.ndarray:
        """Get statevector of the circuit."""
        circuit_copy = circuit.copy()
        circuit_copy.remove_final_measurements(inplace=True)

        from qiskit_aer import AerSimulator
        simulator = AerSimulator(method="statevector")
        job = simulator.run(circuit_copy)
        result = job.result()
        statevector = result.get_statevector()

        return np.array(statevector)

    def get_unitary(self, circuit: QuantumCircuit) -> np.ndarray:
        """Get unitary matrix of the circuit."""
        from qiskit_aer import AerSimulator
        simulator = AerSimulator(method="unitary")
        job = simulator.run(circuit)
        result = job.result()
        unitary = result.get_unitary()

        return np.array(unitary)

    def draw_circuit(self, circuit: QuantumCircuit) -> str:
        """Draw the circuit as ASCII art."""
        return circuit.draw(output="text")

    def get_circuit_depth(self, circuit: QuantumCircuit) -> int:
        """Get circuit depth."""
        return circuit.depth()

    def get_circuit_size(self, circuit: QuantumCircuit) -> int:
        """Get number of gates in circuit."""
        return circuit.size()
