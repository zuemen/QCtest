from __future__ import annotations

import argparse

from .classical import (
    MonteCarloRiskEngine,
    conditional_value_at_risk_from_distribution,
    economic_capital_from_distribution,
    exact_loss_distribution,
    expected_loss_from_distribution,
    value_at_risk_from_distribution,
)
from .portfolio import synthetic_portfolio
from .qiskit_backend import OFFICIAL_REFERENCES, detect_qiskit_backend
from .quantum import QuantumRiskEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quantum credit risk starter demo")
    parser.add_argument("--portfolio-size", type=int, default=8)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--systemic-factors", type=int, default=2)
    parser.add_argument(
        "--mode",
        choices=["classical", "quantum", "compare"],
        default="compare",
        help="Run only the classical baseline, only the local quantum mode, or both.",
    )
    parser.add_argument("--shots", type=int, default=256)
    parser.add_argument("--num-eval-qubits", type=int, default=6)
    parser.add_argument(
        "--show-qiskit-status",
        action="store_true",
        help="Print the detected Qiskit Finance stack status and official reference links.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    portfolio = synthetic_portfolio(size=args.portfolio_size, seed=args.seed, systemic_factors=args.systemic_factors)
    exact_distribution = exact_loss_distribution(portfolio)

    print(f"Portfolio size: {len(portfolio)}")
    print(f"Systemic factors: {portfolio.systemic_factor_count}")
    print(f"Total exposure: {portfolio.total_exposure:,.2f}")
    print(f"Max loss: {portfolio.max_loss:,.2f}")

    if args.mode in {"classical", "compare"}:
        mc_engine = MonteCarloRiskEngine(seed=args.seed)
        report = mc_engine.analyze(portfolio, trials=args.trials, confidence=args.confidence)
        print("\nClassical Monte Carlo estimates")
        print(f"  EL   : {report.expected_loss:,.2f}")
        print(f"  VaR  : {report.value_at_risk:,.2f}")
        print(f"  CVaR : {report.conditional_value_at_risk:,.2f}")
        print(f"  EC   : {report.economic_capital:,.2f}")

    print("\nExact benchmark")
    print(f"  EL   : {expected_loss_from_distribution(exact_distribution):,.2f}")
    print(f"  VaR  : {value_at_risk_from_distribution(exact_distribution, args.confidence):,.2f}")
    print(f"  CVaR : {conditional_value_at_risk_from_distribution(exact_distribution, args.confidence):,.2f}")
    print(f"  EC   : {economic_capital_from_distribution(exact_distribution, args.confidence):,.2f}")

    if args.mode in {"quantum", "compare"}:
        quantum_engine = QuantumRiskEngine(shots=args.shots, num_eval_qubits=args.num_eval_qubits, seed=args.seed)
        quantum_report = quantum_engine.analyze(portfolio, confidence=args.confidence)
        print("\nLocal quantum mode")
        print(f"  Backend : {quantum_engine.backend_name}")
        print(f"  EL      : {quantum_report.expected_loss.estimate:,.2f}")
        print(f"  VaR     : {quantum_report.value_at_risk.estimate:,.2f}")
        print(f"  CVaR    : {quantum_report.conditional_value_at_risk.estimate:,.2f}")
        print(f"  EC      : {quantum_report.economic_capital.estimate:,.2f}")
        print(f"  Notes   : {quantum_engine.implementation_notes()}")
        print(f"  EL detail   : {quantum_report.expected_loss.detail}")
        print(f"  VaR detail  : {quantum_report.value_at_risk.detail}")
        print(f"  CVaR detail : {quantum_report.conditional_value_at_risk.detail}")
        print(f"  EC detail   : {quantum_report.economic_capital.detail}")

    if args.show_qiskit_status:
        status = detect_qiskit_backend()
        print("\nQiskit Finance stack status")
        print(f"  Available : {status.available}")
        print(f"  Installed : {status.installed_versions or '{}'}")
        print(f"  Missing   : {status.missing_packages or '[]'}")
        print(f"  Install   : {status.install_command()}")
        print("\nOfficial references")
        for reference in OFFICIAL_REFERENCES:
            print(f"  - {reference.title}: {reference.url}")
            print(f"    {reference.note}")


if __name__ == "__main__":
    main()
