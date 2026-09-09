# Arquitectura de QuantumLLM

## Visión General

QuantumLLM es una librería diseñada para entrenar Modelos de Lenguaje (LLMs) utilizando computación cuántica. Sigue una arquitectura modular inspirada en Kedro, permitiendo composición flexible de componentes cuánticos y clásicos.

## Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    Aplicación del Usuario                   │
│            (Scripts de Entrenamiento, Pipelines)            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Pipeline Framework                       │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────────────┐   │
│  │   Node       │  │ Pipeline │  │  PipelineRunner      │   │
│  │ (Units)      │  │  (DAG)   │  │  (Executor)          │   │
│  └──────────────┘  └──────────┘  └──────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│              Quantum & Machine Learning Layer               │
│                                                              │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Quantum        │  │  Data        │  │  Training    │   │
│  │  ├─ Backends    │  │  Encoding    │  │  ├─ Optimizers
│  │  ├─ Circuits    │  │              │  │  ├─ Callbacks │   │
│  │  └─ Gates       │  │  Strategies: │  │  └─ Metrics  │   │
│  │                 │  │  ├─ Angle    │  │              │   │
│  │  Backend Types: │  │  ├─ Amplitude│  │ Learning     │   │
│  │  ├─ Qiskit      │  │  ├─ Basis    │  │ Utilities:   │   │
│  │  ├─ PennyLane   │  │  └─ IQP      │  │ ├─ Layers    │   │
│  │  └─ Cirq        │  │              │  │ └─ Models    │   │
│  └─────────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                Configuration & Support                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │  Settings    │  │  Logger      │  │  Utilities     │    │
│  │  (YAML-based)│  │  (loguru)    │  │  ├─ Decorators │    │
│  │              │  │              │  │  └─ Validators │    │
│  └──────────────┘  └──────────────┘  └────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## Módulos Principales

### 1. Core Framework (`quantum_llm.core`)

**Propósito**: Orquestación de workflows tipo Kedro

#### Node
- Unidad básica de procesamiento
- Define inputs, outputs y la función a ejecutar
- Validación de dependencias
- Soporte para tags y metadatos

```python
@node(inputs=['data'], outputs=['processed'])
def preprocess(data):
    return data * 2
```

#### Pipeline
- Grafo Dirigido Acíclico (DAG) de Nodes
- Validación de consistencia
- Cálculo de orden de ejecución (topological sort)
- Detección de ciclos

```python
pipeline = Pipeline([
    node1,
    node2,  # Automáticamente ordenado
])
```

#### PipelineRunner
- Ejecutor del pipeline
- Gestión de contexto de ejecución
- Tracking de métricas
- Manejo de errores

### 2. Quantum Computing (`quantum_llm.quantum`)

**Propósito**: Abstracción de diferentes backends cuánticos

#### Backends
- Interfaz común para Qiskit, PennyLane, Cirq
- Operaciones: create_circuit, apply_gate, measure, execute
- Acceso a statevector y unitary

```python
backend = QiskitBackend(simulator="qasm_simulator")
circuit = backend.create_circuit(n_qubits=4)
results = backend.execute(circuit, shots=1024)
```

#### Ansatz (Circuit Patterns)
- BasicAnsatz: Rotaciones + entanglement lineal
- CircularAnsatz: Entanglement circular
- HardwareEfficientAnsatz: Optimizado para NISQ
- RotationalAnsatz: Solo rotaciones

```python
ansatz = get_ansatz("hardware_efficient", n_qubits=4, n_layers=2, backend)
circuit = ansatz.build(params)
```

#### Data Encoding
- AngleEncoding: Datos como ángulos de rotación
- AmplitudeEncoding: Datos como amplitudes
- BasisEncoding: Datos como estados de base
- IQPEncoding: Instantaneous Quantum Polynomial

```python
encoding = get_encoding("angle", backend)
circuit = encoding.encode(circuit, data, qubits)
```

### 3. Machine Learning (`quantum_llm.ml`)

**Propósito**: Componentes de ML cuántico-clásico

- **Embeddings**: Conversión de datos a representaciones cuánticas
- **Layers**: Capas QNN para redes híbridas
- **Models**: Modelos completos combinando componentes

### 4. Training (`quantum_llm.training`)

**Propósito**: Utilidades para entrenamiento

- **Trainers**: Bucles de entrenamiento
- **Optimizers**: Optimizadores cuánticos (QAOA, VQE, etc.)
- **Callbacks**: Hooks para monitoreo
- **Metrics**: Métricas de evaluación

### 5. Configuration (`quantum_llm.config`)

**Propósito**: Gestión centralizada de configuración

#### Settings
- Carga de YAML/Env
- Type-safe con Pydantic
- Soporte para perfiles

```python
settings = Settings.from_yaml("conf/base/parameters.yaml")
```

#### Logger
- Setup centralizado de logging
- Salida a consola y archivo
- Niveles configurables

### 6. Data Management (`quantum_llm.data`)

**Propósito**: Gestión de datos

- **Loaders**: Lectura de datasets
- **Preprocessors**: Transformación de datos
- **Catalog**: Registro de datos disponibles

### 7. Visualization (`quantum_llm.visualization`)

**Propósito**: Visualización y monitoreo

- **Circuit Visualization**: Dibujar circuitos
- **Metrics Plotting**: Gráficos de entrenamiento
- **Dashboard**: Monitor en tiempo real

## Flujo de Datos Típico

```
Input Data
    ↓
[Node: Load Data] → Dataset
    ↓
[Node: Preprocess] → Processed Data
    ↓
[Node: Create Model] → Quantum Model
    ↓
[Node: Encode] → Encoded Circuit
    ↓
[Node: Train] → Trained Parameters
    ↓
[Node: Evaluate] → Metrics
    ↓
Output (Saved Model + Metrics)
```

## Patrones de Uso

### 1. Pipeline Simple

```python
pipeline = Pipeline([
    Node(load_data, [], ['data']),
    Node(process, ['data'], ['processed']),
    Node(train, ['processed'], ['model']),
])

runner = PipelineRunner(pipeline)
results = runner.run()
```

### 2. Pipeline con Configuración

```python
settings = Settings.from_yaml('conf/base/parameters.yaml')

pipeline = Pipeline([...], name=f"training_{settings.model_type}")
```

### 3. Pipeline Condicional

```python
pipeline = Pipeline([
    Node(load_data, [], ['data']),
    Node(process, ['data'], ['processed']) if settings.use_processing else None,
    Node(train, ['processed'], ['model']),
])
```

### 4. Pipeline con Tags

```python
nodes = [
    Node(load_data, [], ['data'], tags={'io'}),
    Node(process, ['data'], ['processed'], tags={'preprocessing'}),
    Node(train, ['processed'], ['model'], tags={'training'}),
]

# Ejecutar solo nodos de preprocessing
preprocessing_nodes = [n for n in nodes if 'preprocessing' in n.tags]
```

## Flujos de Trabajo Recomendados

### Experimentación
1. Crear notebook jupyter
2. Cargar datos
3. Probar diferentes ansatz/encoding
4. Guardar configuración ganadora
5. Convertir a pipeline

### Producción
1. Definir pipeline en scripts
2. Centralizar configuración en YAML
3. Agregar validaciones y logging
4. Crear tests
5. Empaquetar e deployar

### Debugging
1. Usar `dry_run=True` para validar
2. Activar logging en DEBUG
3. Inspeccionar contexto intermedios
4. Usar pdb para breakpoints

## Extensibilidad

### Agregar Nuevo Backend

```python
class MyBackend(QuantumBackend):
    def create_circuit(self, n_qubits, name="circuit"):
        # Implementar
        pass
    
    # Implementar otros métodos
```

### Agregar Nuevo Ansatz

```python
class MyAnsatz(Ansatz):
    def _calculate_n_params(self):
        return 42
    
    def build(self, params):
        # Implementar
        pass
```

### Agregar Nuevo Encoding

```python
class MyEncoding(DataEncoding):
    def encode(self, circuit, data, qubits):
        # Implementar
        pass
```

## Performance Considerations

1. **Circuit Depth**: Minimizar profundidad para menos ruido
2. **Gate Count**: Más gates = más decoherence
3. **Qubit Count**: Trade-off entre expresividad y ruido
4. **Shot Count**: Más shots = mejor estadística pero más tiempo
5. **Batch Size**: Ajustar según memoria disponible

## Limitaciones Conocidas

1. Simuladores cuánticos limitados a ~30 qubits
2. Ruido en hardwares reales afecta resultados
3. Curvas estériles en optimization
4. Escalabilidad limitada actualmente

## Roadmap

- [ ] Soporte para más backends (Amazon Braket, IonQ, etc.)
- [ ] Métodos clásicos de optimización avanzados
- [ ] Compilación automática de circuitos
- [ ] Soporte para hardware real con mitigación de errores
- [ ] Integración con bibliotecas populares (PyTorch, TensorFlow)
- [ ] Benchmarking suite
