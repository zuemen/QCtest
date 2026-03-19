from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable, List


@dataclass(frozen=True)
class Borrower:
    borrower_id: str
    pd: float
    lgd: float
    ead: float
    rho: float = 0.0
    sector: str = "general"

    @property
    def loss_if_default(self) -> float:
        return self.lgd * self.ead


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


def synthetic_portfolio(size: int = 8, seed: int = 7) -> Portfolio:
    rng = Random(seed)
    sectors = ["retail", "energy", "healthcare", "manufacturing"]
    borrowers = []
    for index in range(size):
        pd = round(rng.uniform(0.01, 0.12), 4)
        lgd = round(rng.uniform(0.35, 0.7), 4)
        ead = round(rng.uniform(50_000, 250_000), 2)
        rho = round(rng.uniform(0.05, 0.3), 4)
        sector = sectors[index % len(sectors)]
        borrowers.append(
            Borrower(
                borrower_id=f"B{index + 1:02d}",
                pd=pd,
                lgd=lgd,
                ead=ead,
                rho=rho,
                sector=sector,
            )
        )
    return Portfolio(borrowers)
