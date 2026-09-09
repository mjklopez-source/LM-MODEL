"""Hybrid Classical-Quantum Model Example

Demonstrates combining classical neural networks with quantum layers.
"""

import numpy as np
from typing import Dict, Tuple
from quantum_llm import Node, Pipeline, PipelineRunner
from quantum_llm.quantum import QiskitBackend, get_ansatz, get_encoding
from quantum_llm.config import setup_logger


logger = setup_logger(level="INFO")


class HybridModel:
    """Hybrid classical-quantum model."""

    def __init__(self, backend, n_qubits: int = 4, n_layers: int = 2):
        """Initialize hybrid model.

        Args:
            backend: Quantum backend
            n_qubits: Number of qubits
            n_layers: Number of ansatz layers
        """
        self.backend = backend
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.ansatz = get_ansatz("basic", n_qubits, n_layers, backend)
        self.encoding = get_encoding("angle", backend)

    def classical_preprocessing(self, x: np.ndarray) -> np.ndarray:
        """Apply classical preprocessing.

        Args:
            x: Input data

        Returns:
            Processed features
        """
        # Example: Normalize and project to quantum feature space
        x_norm = (x - np.mean(x)) / (np.std(x) + 1e-8)
        # Project to [0, 1]
        x_projected = (np.tanh(x_norm) + 1) / 2
        return x_projected[:self.n_qubits]

    def quantum_layer(self, classical_features: np.ndarray, params: np.ndarray) -> float:
        """Apply quantum layer.

        Args:
            classical_features: Features from classical layer
            params: Quantum parameters

        Returns:
            Expectation value
        """
        # Create circuit
        circuit = self.backend.create_circuit(self.n_qubits)

        # Encode classical features
        circuit = self.encoding.encode(circuit, classical_features, list(range(self.n_qubits)))

        # Apply variational ansatz
        ansatz_circuit = self.ansatz.build(params)
        # In practice, would merge circuits

        # For demo, just return a simulated expectation value
        return float(np.mean(classical_features))

    def forward(self, x: np.ndarray, params: np.ndarray) -> float:
        """Forward pass.

        Args:
            x: Input data
            params: Model parameters

        Returns:
            Output prediction
        """
        # Classical preprocessing
        features = self.classical_preprocessing(x)

        # Quantum layer
        output = self.quantum_layer(features, params)

        # Post-processing
        prediction = np.tanh(output)

        return prediction


def create_hybrid_model(backend_dict: Dict) -> Dict:
    """Create hybrid model."""
    logger.info("Creating hybrid classical-quantum model...")

    backend = backend_dict["backend"]
    model = HybridModel(backend, n_qubits=4, n_layers=2)

    params = np.random.uniform(0, 2 * np.pi, model.ansatz.n_params)

    logger.info(f"Model created with {model.ansatz.n_params} quantum parameters")

    return {
        "model": model,
        "params": params,
    }


def train_hybrid_model(
    data_dict: Dict, model_dict: Dict
) -> Dict:
    """Train hybrid model."""
    logger.info("Training hybrid model...")

    X = data_dict["X"]
    y = data_dict["y"]

    model = model_dict["model"]
    params = model_dict["params"]

    n_epochs = 3
    learning_rate = 0.01

    for epoch in range(n_epochs):
        total_loss = 0
        correct = 0

        for x_sample, y_true in zip(X, y):
            # Forward pass
            prediction = model.forward(x_sample, params)

            # Binary classification
            pred_class = 1 if prediction > 0.5 else 0

            # Loss
            loss = (pred_class - y_true) ** 2
            total_loss += loss

            if pred_class == y_true:
                correct += 1

            # Simplified parameter update
            params += -learning_rate * np.random.randn(*params.shape) * 0.01

        avg_loss = total_loss / len(X)
        accuracy = correct / len(X)

        logger.info(
            f"Epoch {epoch + 1}/{n_epochs} - "
            f"Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2%}"
        )

    return {
        "model": model,
        "trained_params": params,
        "final_accuracy": accuracy,
    }


def evaluate_hybrid_model(data_dict: Dict, trained_dict: Dict) -> Dict:
    """Evaluate hybrid model."""
    logger.info("Evaluating hybrid model...")

    X = data_dict["X"]
    y = data_dict["y"]

    model = trained_dict["model"]
    params = trained_dict["trained_params"]

    correct = 0
    for x_sample, y_true in zip(X, y):
        prediction = model.forward(x_sample, params)
        pred_class = 1 if prediction > 0.5 else 0

        if pred_class == y_true:
            correct += 1

    accuracy = correct / len(X)
    logger.info(f"Final Accuracy: {accuracy:.2%}")

    return {
        "accuracy": accuracy,
        "model": model,
        "params": params,
    }


def main():
    """Main hybrid model example."""
    logger.info("Starting Hybrid Classical-Quantum Model Example...")

    # Load backend
    from quantum_llm.quantum import QiskitBackend

    backend = QiskitBackend()

    # Create pipeline
    pipeline = Pipeline(
        [
            Node(
                lambda: {"X": np.random.randn(10, 4), "y": np.random.randint(0, 2, 10)},
                [],
                ["data"],
            ),
            Node(lambda: {"backend": backend}, [], ["backend_dict"]),
            Node(create_hybrid_model, ["backend_dict"], ["model_dict"]),
            Node(train_hybrid_model, ["data", "model_dict"], ["trained_model"]),
            Node(evaluate_hybrid_model, ["data", "trained_model"], ["evaluation"]),
        ]
    )

    print("\n" + pipeline.describe() + "\n")

    # Execute pipeline
    runner = PipelineRunner(pipeline)
    results = runner.run()

    logger.info("Pipeline completed!")
    print(f"\nFinal Results: {results['evaluation']}")


if __name__ == "__main__":
    main()
