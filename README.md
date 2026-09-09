# QuantumLLM - Quantum Computing Library for LLM Training

Una librería Python moderna para entrenar modelos de lenguaje (LLMs) utilizando computación cuántica. Inspirada en la estructura de [Kedro](https://kedro.org/), proporciona un framework modular, escalable y fácil de usar.

## Características

- 🚀 **Pipeline-Based Architecture**: Gestión de flujos de trabajo siguiendo patrones de Kedro
- ⚛️ **Soporte Multi-Backend Cuántico**: Qiskit, PennyLane, Cirq
- 🔄 **Integración con PyTorch/TensorFlow**: Entrenamiento híbrido clásico-cuántico
- 📊 **Visualización y Monitoreo**: Herramientas integradas para visualizar circuitos y resultados
- 🧪 **Testing Completo**: Suite de tests con pytest
- 📚 **Documentación y Ejemplos**: Ejemplos funcionales y bien documentados

## Estructura del Proyecto

```
quantum_llm/
├── conf/                          # Configuración
│   ├── base/                     # Configuración base
│   │   ├── parameters.yaml       # Parámetros globales
│   │   ├── logging.yaml          # Configuración de logging
│   │   └── catalog.yaml          # Catálogo de datos
│   └── credentials.yaml          # Credenciales (git-ignored)
├── src/
│   └── quantum_llm/
│       ├── __init__.py
│       ├── core/                 # Core framework
│       │   ├── pipeline.py       # Pipeline orchestration
│       │   ├── node.py           # Node definitions
│       │   └── runner.py         # Pipeline runner
│       ├── quantum/              # Quantum computing
│       │   ├── backends/         # Backend implementations
│       │   │   ├── qiskit_backend.py
│       │   │   ├── pennylane_backend.py
│       │   │   └── cirq_backend.py
│       │   ├── circuits/         # Quantum circuits
│       │   │   ├── ansatz.py     # Circuit ansatz patterns
│       │   │   ├── encoding.py   # Data encoding strategies
│       │   │   └── optimization.py
│       │   ├── gates.py          # Custom gates
│       │   └── utils.py          # Quantum utilities
│       ├── ml/                   # Machine Learning
│       │   ├── embeddings.py     # Quantum embeddings
│       │   ├── layers.py         # Quantum neural layers
│       │   └── models.py         # Model definitions
│       ├── data/                 # Data management
│       │   ├── loaders.py        # Data loading
│       │   ├── preprocessors.py  # Data preprocessing
│       │   └── catalog.py        # Data catalog
│       ├── training/             # Training utilities
│       │   ├── trainer.py        # Trainer class
│       │   ├── optimizers.py     # Quantum optimizers
│       │   └── callbacks.py      # Training callbacks
│       ├── visualization/        # Visualization tools
│       │   ├── circuits.py       # Circuit visualization
│       │   ├── metrics.py        # Metrics plotting
│       │   └── dashboard.py      # Monitoring dashboard
│       ├── config/               # Configuration management
│       │   ├── settings.py       # Settings loader
│       │   └── logger.py         # Logger setup
│       └── utils/                # Utilities
│           ├── decorators.py     # Decorators
│           ├── validators.py     # Input validation
│           └── helpers.py        # Helper functions
├── pipelines/                    # Pipeline definitions
│   ├── __init__.py
│   ├── data_pipeline.py          # Data processing pipeline
│   ├── training_pipeline.py      # Training pipeline
│   └── evaluation_pipeline.py    # Evaluation pipeline
├── examples/                     # Example scripts
│   ├── basic_training.py         # Basic example
│   ├── hybrid_model.py           # Hybrid classical-quantum
│   └── distributed_training.py   # Distributed training
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/                         # Documentation
│   ├── source/
│   ├── build/
│   └── index.md
├── pyproject.toml               # Project configuration
├── requirements.txt             # Dependencies
├── setup.py                     # Setup script
├── pytest.ini                   # Pytest config
├── .gitignore
└── LICENSE
```

## Instalación

```bash
pip install -r requirements.txt
pip install -e .
```

## Inicio Rápido

```python
from quantum_llm import Pipeline, Node
from quantum_llm.quantum import QiskitBackend
from quantum_llm.ml import QuantumEmbedding

# Crear backend cuántico
backend = QiskitBackend(simulator='qasm_simulator')

# Crear embedding cuántico
embedding = QuantumEmbedding(n_qubits=4, backend=backend)

# Crear pipeline
pipeline = Pipeline([
    Node('load_data', load_data_fn, inputs=[], outputs=['data']),
    Node('encode', encode_fn, inputs=['data'], outputs=['encoded']),
    Node('train', train_fn, inputs=['encoded'], outputs=['model']),
])

# Ejecutar pipeline
results = pipeline.run()
```

## Requisitos

- Python 3.8+
- qiskit >= 0.39.0
- pennylane >= 0.31.0
- cirq >= 1.0.0
- torch >= 2.0.0
- transformers >= 4.30.0
- kedro >= 0.18.0

## Licencia

MIT
