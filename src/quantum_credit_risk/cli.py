from __future__ import annotations

import argparse
from textwrap import dedent

from .classical import (
    MonteCarloRiskEngine,
    conditional_value_at_risk_from_distribution,
    exact_loss_distribution,
    expected_loss_from_distribution,
    value_at_risk_from_distribution,
)
from .portfolio import synthetic_portfolio
from .quantum import QuantumRiskEngine, QuantumEngineUnavailable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quantum credit risk starter demo")
    parser.add_argument("--portfolio-size", type=int, default=8)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--confidence", type=float, default=0.95)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    portfolio = synthetic_portfolio(size=args.portfolio_size, seed=args.seed)
    mc_engine = MonteCarloRiskEngine(seed=args.seed)
    report = mc_engine.analyze(portfolio, trials=args.trials, confidence=args.confidence)
    exact_distribution = exact_loss_distribution(portfolio)

    exact_el = expected_loss_from_distribution(exact_distribution)
    exact_var = value_at_risk_from_distribution(exact_distribution, args.confidence)
    exact_cvar = conditional_value_at_risk_from_distribution(exact_distribution, args.confidence)

    print(f"Portfolio size: {len(portfolio)}")
    print(f"Total exposure: {portfolio.total_exposure:,.2f}")
    print(f"Max loss: {portfolio.max_loss:,.2f}")
    print("\nClassical Monte Carlo estimates")
    print(f"  EL   : {report.expected_loss:,.2f}")
    print(f"  VaR  : {report.value_at_risk:,.2f}")
    print(f"  CVaR : {report.conditional_value_at_risk:,.2f}")

    print("\nExact benchmark")
    print(f"  EL   : {exact_el:,.2f}")
    print(f"  VaR  : {exact_var:,.2f}")
    print(f"  CVaR : {exact_cvar:,.2f}")

    quantum_engine = QuantumRiskEngine()
    try:
        quantum_engine.estimate_expected_loss(portfolio, confidence=args.confidence)
    except QuantumEngineUnavailable as exc:
        print("\nQuantum status")
        print(dedent(f"""
        {exc}
        Notes: {quantum_engine.implementation_notes()}
        """).strip())


if __name__ == "__main__":
    main()
