# Guía de Desarrollo para QuantumLLM

## Configuración del Entorno

### Requisitos Previos
- Python 3.8+
- pip o conda

### Instalación de Dependencias

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalación en modo desarrollo
pip install -e .

# Instalar dependencias de desarrollo
pip install -e ".[dev]"
```

## Estructura del Proyecto

```
quantum_llm/
├── src/quantum_llm/          # Código fuente principal
├── tests/                    # Tests unitarios e integración
├── examples/                 # Scripts de ejemplo
├── conf/                     # Archivos de configuración
├── docs/                     # Documentación
└── pyproject.toml           # Configuración del proyecto
```

## Desarrollo

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests con cobertura
pytest --cov=src/quantum_llm

# Tests específicos
pytest tests/test_pipeline.py -v

# Tests con marker
pytest -m "not slow"
```

### Formatos y Linting

```bash
# Formatear código
black src/ tests/ examples/
isort src/ tests/ examples/

# Verificar linting
flake8 src/ tests/
mypy src/

# Todo junto
black . && isort . && flake8 . && mypy src/
```

### Ejecutar Ejemplos

```bash
# Ejemplo básico
python examples/basic_training.py

# Con output detallado
python -m examples.basic_training
```

## Arquitectura

### Core Framework (Kedro-like)

- **Node**: Unidad de procesamiento individual
- **Pipeline**: Grafo dirigido acíclico (DAG) de nodos
- **PipelineRunner**: Ejecutor del pipeline

### Quantum Computing

- **Backends**: Implementaciones para Qiskit, PennyLane, Cirq
- **Ansatz**: Patrones de circuitos cuánticos variacionales
- **Encoding**: Estrategias de codificación de datos

### Machine Learning

- **Embeddings**: Embeddings cuánticos
- **Layers**: Capas de redes neuronales cuánticas
- **Training**: Utilidades de entrenamiento

## Convenciones de Código

### Nombres

- Usar `snake_case` para funciones y variables
- Usar `CamelCase` para clases
- Usar `UPPER_CASE` para constantes
- Usar nombres descriptivos

### Documentación

Cada función debe tener docstring en formato Google:

```python
def my_function(arg1: str, arg2: int) -> bool:
    """Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong
    """
    pass
```

### Type Hints

Usar type hints en todas las funciones públicas:

```python
from typing import List, Optional, Dict, Any

def process_data(
    data: List[float],
    threshold: Optional[float] = None
) -> Dict[str, Any]:
    """Process data."""
    pass
```

## Contribuciones

1. Crear rama desde `main`
2. Hacer cambios con commits claros
3. Añadir tests para nuevas features
4. Asegurar que todos los tests pasen
5. Hacer PR con descripción clara

## Recursos Útiles

- [Kedro Documentation](https://kedro.org/)
- [Qiskit Documentation](https://qiskit.org/)
- [PennyLane Documentation](https://pennylane.ai/)
- [PyTest Documentation](https://docs.pytest.org/)

## Troubleshooting

### Problema: ImportError para Qiskit
```bash
pip install qiskit qiskit-aer
```

### Problema: Tests fallan
```bash
# Limpiar cache
pytest --cache-clear

# Reinstalar en modo desarrollo
pip install -e . --no-cache-dir
```

### Problema: Versión incorrecta de dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```
