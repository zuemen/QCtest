from __future__ import annotations

from dataclasses import dataclass

from .portfolio import Portfolio


class QuantumEngineUnavailable(RuntimeError):
    """Raised when the optional quantum backend is not installed yet."""


@dataclass
class QuantumRiskEngine:
    backend_name: str = "qiskit-iterative-amplitude-estimation"

    def estimate_expected_loss(self, portfolio: Portfolio, confidence: float = 0.95) -> float:
        self._raise_unavailable(portfolio, confidence)

    def estimate_value_at_risk(self, portfolio: Portfolio, confidence: float = 0.95) -> float:
        self._raise_unavailable(portfolio, confidence)

    def estimate_conditional_value_at_risk(self, portfolio: Portfolio, confidence: float = 0.95) -> float:
        self._raise_unavailable(portfolio, confidence)

    def implementation_notes(self) -> str:
        return (
            "Planned implementation: encode the portfolio loss distribution, mark threshold/payoff states, "
            "and call iterative amplitude estimation through Qiskit Finance."
        )

    def _raise_unavailable(self, portfolio: Portfolio, confidence: float) -> None:
        raise QuantumEngineUnavailable(
            "Quantum execution is not wired yet. Use the classical baseline now, then replace this stub "
            f"with a Qiskit implementation for portfolio size {len(portfolio)} at confidence {confidence:.2f}."
        )
