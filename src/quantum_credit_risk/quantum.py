from __future__ import annotations

from dataclasses import dataclass
from math import asin, pi, sin
from random import Random
from typing import Dict, List, Tuple

from .classical import (
    conditional_value_at_risk_from_distribution,
    economic_capital_from_distribution,
    exact_loss_distribution,
)
from .portfolio import Portfolio


class QuantumEngineUnavailable(RuntimeError):
    """Raised when an optional quantum backend cannot be used."""


@dataclass
class QuantumEstimate:
    estimate: float
    confidence: float
    shots: int
    detail: str


@dataclass
class QuantumRiskSummary:
    expected_loss: QuantumEstimate
    value_at_risk: QuantumEstimate
    conditional_value_at_risk: QuantumEstimate
    economic_capital: QuantumEstimate


@dataclass
class LocalAmplitudeEstimator:
    """Dependency-free simulator of ideal amplitude-estimation outcome statistics."""

    num_eval_qubits: int = 6
    shots: int = 256
    seed: int = 123

    def estimate(self, probability: float) -> float:
        probability = min(max(probability, 0.0), 1.0)
        if probability in (0.0, 1.0):
            return probability

        outcomes = self._outcome_probabilities(probability)
        rng = Random(self.seed)
        counts: Dict[int, int] = {index: 0 for index in outcomes}
        cumulative: List[Tuple[float, int]] = []
        running = 0.0
        for index, outcome_probability in outcomes.items():
            running += outcome_probability
            cumulative.append((running, index))

        for _ in range(self.shots):
            draw = rng.random()
            for cutoff, index in cumulative:
                if draw <= cutoff:
                    counts[index] += 1
                    break

        best_index = max(counts, key=counts.get)
        scale = 2 ** self.num_eval_qubits
        return sin(pi * best_index / scale) ** 2

    def _outcome_probabilities(self, probability: float) -> Dict[int, float]:
        theta = asin(probability ** 0.5) / pi
        scale = 2 ** self.num_eval_qubits
        probabilities: Dict[int, float] = {}
        for index in range(scale):
            shifted = theta - index / scale
            if abs(sin(pi * shifted)) < 1e-12:
                value = 1.0
            else:
                numerator = sin(pi * scale * shifted) ** 2
                denominator = (scale * sin(pi * shifted)) ** 2
                value = numerator / denominator
            probabilities[index] = value

        total = sum(probabilities.values())
        return {index: value / total for index, value in probabilities.items()}


@dataclass
class QuantumRiskEngine:
    backend_name: str = "local-amplitude-estimation"
    num_eval_qubits: int = 6
    shots: int = 256
    seed: int = 123

    def estimate_expected_loss(self, portfolio: Portfolio, confidence: float = 0.95) -> QuantumEstimate:
        estimator = self._estimator_for("expected-loss")
        expected_loss = 0.0
        details: List[str] = []
        for borrower in portfolio:
            pd_estimate = estimator.estimate(borrower.pd)
            contribution = borrower.loss_if_default * pd_estimate
            expected_loss += contribution
            details.append(
                f"{borrower.borrower_id}: factors={borrower.factor_loadings}, pd≈{pd_estimate:.4f}, contribution≈{contribution:.2f}"
            )
        return QuantumEstimate(expected_loss, confidence, self.shots, "; ".join(details))

    def estimate_value_at_risk(self, portfolio: Portfolio, confidence: float = 0.95) -> QuantumEstimate:
        distribution = exact_loss_distribution(portfolio)
        distinct_losses = sorted(distribution)
        estimator = self._estimator_for("value-at-risk")
        selected = distinct_losses[-1]
        selected_probability = 1.0
        for threshold in distinct_losses:
            cdf = sum(probability for loss, probability in distribution.items() if loss <= threshold)
            cdf_estimate = estimator.estimate(cdf)
            if cdf_estimate >= confidence:
                selected = threshold
                selected_probability = cdf_estimate
                break
        return QuantumEstimate(selected, confidence, self.shots, f"Estimated CDF at VaR threshold ≈ {selected_probability:.4f}")

    def estimate_conditional_value_at_risk(self, portfolio: Portfolio, confidence: float = 0.95) -> QuantumEstimate:
        distribution = exact_loss_distribution(portfolio)
        var_estimate = self.estimate_value_at_risk(portfolio, confidence)
        cvar = conditional_value_at_risk_from_distribution(
            {loss: probability for loss, probability in distribution.items() if loss >= var_estimate.estimate},
            confidence=0.0,
        )
        return QuantumEstimate(
            cvar,
            confidence,
            self.shots,
            f"Hybrid estimate using local AE VaR={var_estimate.estimate:.2f} and exact tail distribution.",
        )

    def estimate_economic_capital(self, portfolio: Portfolio, confidence: float = 0.95) -> QuantumEstimate:
        distribution = exact_loss_distribution(portfolio)
        ec = economic_capital_from_distribution(distribution, confidence)
        return QuantumEstimate(
            ec,
            confidence,
            self.shots,
            "Economic capital defined as VaR minus expected loss, matching common credit-risk practice.",
        )

    def analyze(self, portfolio: Portfolio, confidence: float = 0.95) -> QuantumRiskSummary:
        return QuantumRiskSummary(
            expected_loss=self.estimate_expected_loss(portfolio, confidence),
            value_at_risk=self.estimate_value_at_risk(portfolio, confidence),
            conditional_value_at_risk=self.estimate_conditional_value_at_risk(portfolio, confidence),
            economic_capital=self.estimate_economic_capital(portfolio, confidence),
        )

    def implementation_notes(self) -> str:
        return (
            "Direct-run mode mirrors the paper-inspired workflow at a high level: richer portfolio inputs, "
            "floating-point LGD support, and risk metrics beyond expected loss. The true Qiskit upgrade path "
            "still points to GaussianConditionalIndependenceModel plus IterativeAmplitudeEstimation."
        )

    def _estimator_for(self, purpose: str) -> LocalAmplitudeEstimator:
        purpose_offset = sum(ord(character) for character in purpose)
        return LocalAmplitudeEstimator(self.num_eval_qubits, self.shots, self.seed + purpose_offset)
