"""Setup script for QuantumLLM."""

from setuptools import setup, find_packages

setup(
    name="quantum-llm",
    version="0.1.0",
    description="Quantum Computing Library for LLM Training",
    author="QuantumLLM Team",
    author_email="dev@quantumllm.io",
    url="https://github.com/quantum-llm/quantum-llm",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
