"""Basic example of training with QuantumLLM.

Demonstrates:
- Creating a quantum backend
- Building a variational quantum circuit
- Creating a training pipeline
- Executing the pipeline
"""

import numpy as np
from quantum_llm import Pipeline, Node
from quantum_llm.quantum import QiskitBackend, get_ansatz, get_encoding
from quantum_llm.config import setup_logger


logger = setup_logger(level="INFO")


def load_data() -> dict:
    """Load example training data."""
    logger.info("Loading training data...")

    # Generate synthetic data
    n_samples = 10
    n_features = 4

    X = np.random.randn(n_samples, n_features)
    y = np.random.randint(0, 2, n_samples)

    return {"X": X, "y": y}


def prepare_backend() -> dict:
    """Prepare quantum backend."""
    logger.info("Preparing quantum backend...")

    backend = QiskitBackend(simulator="statevector")
    logger.info(f"Using backend: {backend.name}")

    return {"backend": backend}


def build_quantum_model(backend_dict: dict, params_dict: dict = None) -> dict:
    """Build quantum neural network model."""
    logger.info("Building quantum model...")

    backend = backend_dict["backend"]
    n_qubits = 4
    n_layers = 2

    # Get ansatz
    ansatz = get_ansatz("basic", n_qubits, n_layers, backend)
    logger.info(f"Ansatz: {ansatz.__class__.__name__} with {ansatz.n_params} parameters")

    # Initialize parameters
    if params_dict is None:
        params = np.random.uniform(0, 2 * np.pi, ansatz.n_params)
    else:
        params = params_dict.get("params", np.random.uniform(0, 2 * np.pi, ansatz.n_params))

    return {
        "model": ansatz,
        "params": params,
        "backend": backend,
    }


def train_model(data: dict, model_dict: dict) -> dict:
    """Simple training step."""
    logger.info("Training quantum model...")

    X = data["X"]
    y = data["y"]
    model = model_dict["model"]
    params = model_dict["params"]
    backend = model_dict["backend"]

    n_epochs = 3
    learning_rate = 0.01

    # Simplified training loop
    for epoch in range(n_epochs):
        total_loss = 0

        for i, (x_sample, y_true) in enumerate(zip(X, y)):
            # Encode data
            encoding = get_encoding("angle", backend)
            circuit = encoding.encode(
                backend.create_circuit(model.n_qubits),
                x_sample,
                list(range(model.n_qubits)),
            )

            # Apply ansatz
            circuit = model.build(params)

            # Measure
            backend.measure(circuit)

            # Execute (simplified)
            results = backend.execute(circuit, shots=1024)

            # Convert results to probability
            counts = results
            measured_0 = counts.get("0" * model.n_qubits, 0)
            prob_0 = measured_0 / 1024
            prediction = 0 if prob_0 > 0.5 else 1

            # Simple loss
            loss = (prediction - y_true) ** 2
            total_loss += loss

            # Update parameters (simplified gradient descent)
            params += -learning_rate * np.random.randn(*params.shape) * 0.1

        avg_loss = total_loss / len(X)
        logger.info(f"Epoch {epoch + 1}/{n_epochs} - Loss: {avg_loss:.4f}")

    return {
        "model": model,
        "trained_params": params,
        "backend": backend,
        "final_loss": avg_loss,
    }


def evaluate_model(data: dict, trained_model: dict) -> dict:
    """Evaluate the trained model."""
    logger.info("Evaluating model...")

    X = data["X"]
    y = data["y"]
    model = trained_model["model"]
    params = trained_model["trained_params"]
    backend = trained_model["backend"]

    # Simple accuracy evaluation
    correct = 0
    for x_sample, y_true in zip(X, y):
        encoding = get_encoding("angle", backend)
        circuit = encoding.encode(
            backend.create_circuit(model.n_qubits),
            x_sample,
            list(range(model.n_qubits)),
        )
        circuit = model.build(params)
        backend.measure(circuit)
        results = backend.execute(circuit, shots=1024)

        counts = results
        measured_0 = counts.get("0" * model.n_qubits, 0)
        prob_0 = measured_0 / 1024
        prediction = 0 if prob_0 > 0.5 else 1

        if prediction == y_true:
            correct += 1

    accuracy = correct / len(X)
    logger.info(f"Accuracy: {accuracy:.2%}")

    return {"accuracy": accuracy, "model": model, "params": params}


def main():
    """Main example execution."""
    logger.info("Starting QuantumLLM basic training example...")

    # Create pipeline nodes
    pipeline = Pipeline(
        [
            Node(load_data, [], ["data"]),
            Node(prepare_backend, [], ["backend_dict"]),
            Node(build_quantum_model, ["backend_dict"], ["model_dict"]),
            Node(train_model, ["data", "model_dict"], ["trained_model"]),
            Node(evaluate_model, ["data", "trained_model"], ["evaluation"]),
        ]
    )

    # Print pipeline info
    print("\n" + pipeline.describe() + "\n")

    # Execute pipeline
    from quantum_llm import PipelineRunner

    runner = PipelineRunner(pipeline, dry_run=False)
    results = runner.run()

    logger.info("Pipeline completed successfully!")
    logger.info(f"Final Accuracy: {results['evaluation']['accuracy']:.2%}")
    print(f"\nResults: {results}")


if __name__ == "__main__":
    main()
