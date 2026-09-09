# QuantumLLM - Guía de Inicio Rápido

## Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/quantum-llm/quantum-llm.git
cd quantum-llm

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar librería
pip install -r requirements.txt
pip install -e .
```

## Ejemplo Mínimo

```python
from quantum_llm import Pipeline, Node
from quantum_llm.quantum import QiskitBackend, get_ansatz

# Crear backend
backend = QiskitBackend(simulator="qasm_simulator")

# Crear nodos
def load_data():
    return {"data": [1, 2, 3, 4]}

def build_model(data):
    ansatz = get_ansatz("basic", n_qubits=4, n_layers=2, backend=backend)
    return {"ansatz": ansatz, "params": [0.1, 0.2, 0.3]}

# Crear pipeline
pipeline = Pipeline([
    Node(load_data, [], ["data"]),
    Node(build_model, ["data"], ["model"]),
])

# Ejecutar
from quantum_llm import PipelineRunner
runner = PipelineRunner(pipeline)
results = runner.run()
```

## Conceptos Clave

### 1. Pipeline
```python
from quantum_llm import Pipeline, Node

pipeline = Pipeline([node1, node2, node3])
pipeline.describe()  # Ver estructura
```

### 2. Nodes
```python
from quantum_llm import Node

@Node(inputs=["a", "b"], outputs=["c"])
def my_function(a, b):
    return a + b
```

### 3. Backends Cuánticos
```python
from quantum_llm.quantum import QiskitBackend, PennyLaneBackend

# Qiskit
qiskit_backend = QiskitBackend(simulator="qasm_simulator")

# PennyLane
pl_backend = PennyLaneBackend(device="default.qubit", n_qubits=4)
```

### 4. Ansatz (Circuitos Variacionales)
```python
from quantum_llm.quantum import get_ansatz

ansatz = get_ansatz("basic", n_qubits=4, n_layers=2, backend=backend)
# Opciones: basic, circular, hardware_efficient, rotational
```

### 5. Data Encoding
```python
from quantum_llm.quantum import get_encoding

encoding = get_encoding("angle", backend)
# Opciones: angle, amplitude, basis, iqp
```

## Tareas Comunes

### Crear un Modelo Cuántico Simple

```python
import numpy as np
from quantum_llm.quantum import QiskitBackend, get_ansatz

backend = QiskitBackend()
ansatz = get_ansatz("basic", n_qubits=4, n_layers=2, backend=backend)

# Parámetros aleatorios
params = np.random.uniform(0, 2*np.pi, ansatz.n_params)

# Construir circuito
circuit = ansatz.build(params)

# Medir
backend.measure(circuit)
results = backend.execute(circuit, shots=1024)
print(f"Resultados: {results}")
```

### Entrenar un Modelo

```python
from quantum_llm import Pipeline, Node, PipelineRunner
from quantum_llm.quantum import QiskitBackend, get_ansatz

def train(backend, params, data):
    # Tu lógica de entrenamiento
    for epoch in range(10):
        # actualizar params
        pass
    return params

# Crear pipeline de entrenamiento
pipeline = Pipeline([
    Node(lambda: QiskitBackend(), [], ["backend"]),
    Node(lambda: np.random.uniform(0, 2*np.pi, 12), [], ["params"]),
    Node(lambda: np.random.randn(10, 4), [], ["data"]),
    Node(train, ["backend", "params", "data"], ["trained_params"]),
])

runner = PipelineRunner(pipeline)
results = runner.run()
```

### Crear un Modelo Híbrido

```python
import torch
import torch.nn as nn
from quantum_llm.quantum import QiskitBackend, get_ansatz

class HybridNet(nn.Module):
    def __init__(self, backend, n_qubits=4, n_layers=2):
        super().__init__()
        self.backend = backend
        self.ansatz = get_ansatz("basic", n_qubits, n_layers, backend)
        self.classical = nn.Linear(4, 4)
        
    def forward(self, x):
        # Capa clásica
        x = self.classical(x)
        x = torch.relu(x)
        
        # Capa cuántica (simulada)
        # En práctica real, integrar con QNN
        
        return x

# Usar con PyTorch
model = HybridNet(QiskitBackend())
```

## Configuración

### Variables de Entorno

```bash
export QUANTUM_BACKEND=qiskit
export QISKIT_SIMULATOR=qasm_simulator
export N_QUBITS=4
export BATCH_SIZE=32
export LEARNING_RATE=0.01
export LOG_LEVEL=INFO
```

### Archivo YAML

```yaml
# conf/base/parameters.yaml
quantum:
  backend: qiskit
  n_qubits: 4
  n_layers: 2

training:
  batch_size: 32
  learning_rate: 0.01
  epochs: 10
```

## Debugging

### Ver Estructura del Pipeline

```python
pipeline.describe()
# Muestra nodos en orden de ejecución
```

### Dry Run (validar sin ejecutar)

```python
runner = PipelineRunner(pipeline, dry_run=True)
results = runner.run()
```

### Logging Detallado

```python
from quantum_llm.config import setup_logger

logger = setup_logger(level="DEBUG")
logger.debug("Información detallada")
```

### Ver Resultados de Ejecución

```python
runner = PipelineRunner(pipeline)
results = runner.run()

print(runner.get_report())
# {'status': 'success', 'nodes_executed': 3, 'execution_time': 1.23, ...}
```

## Recursos

- 📚 [Documentación Completa](./docs/)
- 🔍 [Ejemplos](./examples/)
- 🧪 [Tests](./tests/)
- ⚙️ [Configuración](./conf/)

## Próximos Pasos

1. Revisar [DEVELOPMENT.md](./DEVELOPMENT.md) para configurar entorno
2. Ejecutar ejemplos: `python examples/basic_training.py`
3. Explorar tests: `pytest -v`
4. Personalizar configuración en `conf/base/`

## Ayuda

- Ver docstrings: `help(Pipeline)`
- Tests como ejemplos: Ver `tests/`
- Issues: https://github.com/quantum-llm/quantum-llm/issues
