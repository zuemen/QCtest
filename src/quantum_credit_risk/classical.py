from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import sqrt
from random import Random
from statistics import NormalDist
from typing import Dict, List, Sequence, Tuple

from .portfolio import Portfolio


@dataclass
class RiskReport:
    expected_loss: float
    value_at_risk: float
    conditional_value_at_risk: float
    losses: List[float]


class MonteCarloRiskEngine:
    def __init__(self, seed: int = 42) -> None:
        self._rng = Random(seed)
        self._standard_normal = NormalDist()

    def simulate_losses(self, portfolio: Portfolio, trials: int = 10_000) -> List[float]:
        losses: List[float] = []
        systemic = self._standard_normal
        for _ in range(trials):
            factor = self._rng.gauss(0.0, 1.0)
            loss = 0.0
            for borrower in portfolio:
                epsilon = self._rng.gauss(0.0, 1.0)
                asset_value = sqrt(max(1e-12, borrower.rho)) * factor + sqrt(max(1e-12, 1.0 - borrower.rho)) * epsilon
                threshold = systemic.inv_cdf(borrower.pd)
                defaulted = asset_value < threshold
                if defaulted:
                    loss += borrower.loss_if_default
            losses.append(round(loss, 8))
        return losses

    def analyze(self, portfolio: Portfolio, trials: int = 10_000, confidence: float = 0.95) -> RiskReport:
        losses = self.simulate_losses(portfolio, trials=trials)
        distribution = distribution_from_losses(losses)
        return RiskReport(
            expected_loss=expected_loss_from_distribution(distribution),
            value_at_risk=value_at_risk_from_distribution(distribution, confidence),
            conditional_value_at_risk=conditional_value_at_risk_from_distribution(distribution, confidence),
            losses=losses,
        )


def distribution_from_losses(losses: Sequence[float]) -> Dict[float, float]:
    distribution: Dict[float, float] = {}
    total = float(len(losses))
    for loss in losses:
        distribution[loss] = distribution.get(loss, 0.0) + 1.0 / total
    return dict(sorted(distribution.items(), key=lambda item: item[0]))


def exact_loss_distribution(portfolio: Portfolio) -> Dict[float, float]:
    distribution: Dict[float, float] = {}
    borrowers = list(portfolio)
    for default_state in product([0, 1], repeat=len(borrowers)):
        probability = 1.0
        loss = 0.0
        for state, borrower in zip(default_state, borrowers):
            if state:
                probability *= borrower.pd
                loss += borrower.loss_if_default
            else:
                probability *= 1.0 - borrower.pd
        loss = round(loss, 8)
        distribution[loss] = distribution.get(loss, 0.0) + probability
    return dict(sorted(distribution.items(), key=lambda item: item[0]))


def expected_loss_from_distribution(distribution: Dict[float, float]) -> float:
    return sum(loss * probability for loss, probability in distribution.items())


def value_at_risk_from_distribution(distribution: Dict[float, float], confidence: float = 0.95) -> float:
    cumulative = 0.0
    for loss, probability in sorted(distribution.items()):
        cumulative += probability
        if cumulative >= confidence:
            return loss
    return max(distribution)


def conditional_value_at_risk_from_distribution(distribution: Dict[float, float], confidence: float = 0.95) -> float:
    var = value_at_risk_from_distribution(distribution, confidence)
    tail_probability = sum(probability for loss, probability in distribution.items() if loss >= var)
    if tail_probability == 0.0:
        return var
    tail_expectation = sum(loss * probability for loss, probability in distribution.items() if loss >= var)
    return tail_expectation / tail_probability
