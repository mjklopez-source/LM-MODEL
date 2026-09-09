"""
Settings and configuration management.
"""

from typing import Any, Dict, Optional
from pathlib import Path
import yaml
import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings from environment and config files.

    Supports YAML configuration files and environment variable overrides.
    """

    # Quantum backends
    quantum_backend: str = Field(default="qiskit", env="QUANTUM_BACKEND")
    qiskit_simulator: str = Field(default="qasm_simulator", env="QISKIT_SIMULATOR")
    pennylane_device: str = Field(default="default.qubit", env="PENNYLANE_DEVICE")

    # Model configuration
    n_qubits: int = Field(default=4, env="N_QUBITS")
    n_layers: int = Field(default=2, env="N_LAYERS")
    model_type: str = Field(default="vqc", env="MODEL_TYPE")

    # Training configuration
    batch_size: int = Field(default=32, env="BATCH_SIZE")
    learning_rate: float = Field(default=0.01, env="LEARNING_RATE")
    epochs: int = Field(default=10, env="EPOCHS")
    optimizer: str = Field(default="adam", env="OPTIMIZER")

    # Data configuration
    data_dir: Path = Field(default=Path("data"), env="DATA_DIR")
    output_dir: Path = Field(default=Path("outputs"), env="OUTPUT_DIR")
    cache_dir: Path = Field(default=Path(".cache"), env="CACHE_DIR")

    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[Path] = Field(default=None, env="LOG_FILE")

    # Execution configuration
    device: str = Field(default="cpu", env="DEVICE")
    seed: int = Field(default=42, env="SEED")
    num_workers: int = Field(default=4, env="NUM_WORKERS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        """Load settings from a YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            Settings instance

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, "r") as f:
            config_dict = yaml.safe_load(f) or {}

        return cls(**config_dict)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables and .env file.

        Returns:
            Settings instance
        """
        return cls()

    def save_yaml(self, path: Path) -> None:
        """Save settings to a YAML file.

        Args:
            path: Path to save YAML file
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary.

        Returns:
            Dictionary of settings
        """
        return self.dict()

    def to_yaml(self) -> str:
        """Convert settings to YAML string.

        Returns:
            YAML representation
        """
        return yaml.dump(self.dict(), default_flow_style=False)
