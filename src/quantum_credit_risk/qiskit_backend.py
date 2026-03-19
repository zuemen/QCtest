from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
from typing import Dict, List


QISKIT_PACKAGES = {
    "qiskit": "qiskit>=1.0",
    "qiskit-aer": "qiskit-aer>=0.14",
    "qiskit-algorithms": "qiskit-algorithms>=0.3",
    "qiskit-finance": "qiskit-finance>=0.4",
}


class QiskitDependencyError(RuntimeError):
    """Raised when the optional Qiskit Finance stack is unavailable."""


@dataclass(frozen=True)
class QiskitBackendStatus:
    available: bool
    installed_versions: Dict[str, str]
    missing_packages: List[str]

    def install_command(self) -> str:
        packages = [QISKIT_PACKAGES[name] for name in self.missing_packages] or list(QISKIT_PACKAGES.values())
        return "python -m pip install " + " ".join(f"'{package}'" for package in packages)


@dataclass(frozen=True)
class QiskitFinanceReference:
    title: str
    url: str
    note: str


OFFICIAL_REFERENCES = [
    QiskitFinanceReference(
        title="Qiskit Finance Tutorials Index",
        url="https://qiskit-community.github.io/qiskit-finance/tutorials/index.html",
        note="Official list of finance tutorials, including Quantum Amplitude Estimation and Credit Risk Analysis.",
    ),
    QiskitFinanceReference(
        title="Quantum Amplitude Estimation tutorial",
        url="https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html",
        note="Shows the QAE workflow built around EstimationProblem, state preparation, Grover operator, and Sampler.",
    ),
    QiskitFinanceReference(
        title="Credit Risk Analysis tutorial",
        url="https://qiskit-community.github.io/qiskit-finance/tutorials/09_credit_risk_analysis.html",
        note="Demonstrates GaussianConditionalIndependenceModel, WeightedAdder, LinearAmplitudeFunction, IterativeAmplitudeEstimation, and qiskit_aer.primitives.Sampler.",
    ),
    QiskitFinanceReference(
        title="GaussianConditionalIndependenceModel API reference",
        url="https://qiskit-community.github.io/qiskit-finance/stubs/qiskit_finance.circuit.library.GaussianConditionalIndependenceModel.html",
        note="Official circuit-library entry point for the credit-risk latent-factor model used in Qiskit Finance.",
    ),
]


def detect_qiskit_backend() -> QiskitBackendStatus:
    installed_versions: Dict[str, str] = {}
    missing_packages: List[str] = []

    for package_name in QISKIT_PACKAGES:
        module_name = package_name.replace("-", "_")
        if find_spec(module_name) is None:
            missing_packages.append(package_name)
            continue
        try:
            installed_versions[package_name] = version(package_name)
        except PackageNotFoundError:
            installed_versions[package_name] = "installed-unknown-version"

    return QiskitBackendStatus(
        available=not missing_packages,
        installed_versions=installed_versions,
        missing_packages=missing_packages,
    )


def require_qiskit_backend() -> QiskitBackendStatus:
    status = detect_qiskit_backend()
    if not status.available:
        raise QiskitDependencyError(
            "Qiskit Finance backend is not available in this environment. "
            f"Missing packages: {', '.join(status.missing_packages)}. "
            f"Install with: {status.install_command()}"
        )
    return status
