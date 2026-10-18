import mimetypes
import tempfile
from pathlib import Path

import fsspec
from kedro.io import DataCatalog
from kedro.pipeline import Pipeline, Node as KedroNode
from kedro_viz.server import run_server
from kedro_viz.api.rest.responses.save_responses import save_api_responses_to_fs
from kedro_viz.data_access import data_access_manager
from kedro_viz.server import populate_data
from quantum_llm import Pipeline as QuantumPipeline

# Tu pipeline de QuantumLLM
from examples.basic_training import (
    load_data, prepare_backend, build_quantum_model, 
    train_model, evaluate_model
)
from quantum_llm import Node

# Crear pipeline QuantumLLM
quantum_pipeline = QuantumPipeline([
    Node(load_data, [], ["data"]),
    Node(prepare_backend, [], ["backend_dict"]),
    Node(build_quantum_model, ["backend_dict"], ["model_dict"]),
    Node(train_model, ["data", "model_dict"], ["trained_model"]),
    Node(evaluate_model, ["data", "trained_model"], ["evaluation"]),
])

# Convertir a Kedro Pipeline
kedro_nodes = []
for node in quantum_pipeline.nodes:
    kedro_nodes.append(
        KedroNode(
            func=node.func,
            inputs=node.inputs or None,
            outputs=node.outputs,
            name=node.name,
            tags=list(node.tags) if node.tags else [],
        )
    )

kedro_pipeline = Pipeline(kedro_nodes)

# Lanzar visualizador
if __name__ == "__main__":
    mimetypes.add_type("application/javascript", ".js")
    with tempfile.TemporaryDirectory(prefix="quantum-llm-viz-") as temp_dir:
        populate_data(data_access_manager, DataCatalog(), {"__default__": kedro_pipeline}, {})
        save_api_responses_to_fs(temp_dir, fsspec.filesystem("file"), True)
        temp_path = Path(temp_dir)
        run_server(
            project_path=str(temp_path.parent),
            load_file=temp_path.name,
            host="127.0.0.1",
            port=4141,
        )