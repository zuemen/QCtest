from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class Borrower:
    borrower_id: str
    pd: float
    lgd: float
    ead: float
    rho: float = 0.0
    sector: str = "general"
    factor_loadings: Tuple[float, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        loadings = self.factor_loadings or ((self.rho,) if self.rho > 0.0 else tuple())
        loading_sum = sum(loadings)
        if loading_sum >= 1.0:
            raise ValueError("The sum of factor loadings must be less than 1.0.")
        object.__setattr__(self, "factor_loadings", tuple(loadings))
        object.__setattr__(self, "rho", loading_sum)

    @property
    def loss_if_default(self) -> float:
        return self.lgd * self.ead

    @property
    def idiosyncratic_loading(self) -> float:
        return 1.0 - sum(self.factor_loadings)


@dataclass(frozen=True)
class Portfolio:
    borrowers: List[Borrower]

    def __iter__(self) -> Iterable[Borrower]:
        return iter(self.borrowers)

    def __len__(self) -> int:
        return len(self.borrowers)

    @property
    def total_exposure(self) -> float:
        return sum(b.ead for b in self.borrowers)

    @property
    def max_loss(self) -> float:
        return sum(b.loss_if_default for b in self.borrowers)

    @property
    def systemic_factor_count(self) -> int:
        if not self.borrowers:
            return 0
        return max(len(b.factor_loadings) for b in self.borrowers)


def synthetic_portfolio(size: int = 8, seed: int = 7, systemic_factors: int = 2) -> Portfolio:
    rng = Random(seed)
    sectors = ["retail", "energy", "healthcare", "manufacturing"]
    borrowers = []
    for index in range(size):
        pd = round(rng.uniform(0.01, 0.12), 4)
        lgd = round(rng.uniform(0.35, 0.7), 4)
        ead = round(rng.uniform(50_000, 250_000), 2)
        remaining = 0.35
        factor_loadings = []
        for factor_index in range(systemic_factors):
            max_loading = min(0.18, remaining)
            if factor_index == systemic_factors - 1:
                loading = round(max(0.0, remaining * rng.uniform(0.3, 0.7)), 4)
            else:
                loading = round(rng.uniform(0.02, max_loading), 4)
            factor_loadings.append(loading)
            remaining = max(0.0, remaining - loading)
        sector = sectors[index % len(sectors)]
        borrowers.append(
            Borrower(
                borrower_id=f"B{index + 1:02d}",
                pd=pd,
                lgd=lgd,
                ead=ead,
                sector=sector,
                factor_loadings=tuple(factor_loadings),
            )
        )
    return Portfolio(borrowers)
