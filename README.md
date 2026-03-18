# Quantum Credit Risk Engine using Amplitude Estimation

This repository contains a practical starter project for building a credit risk analytics workflow around quantum amplitude estimation (QAE). The current implementation focuses on a fully runnable, dependency-light classical baseline, plus a quantum integration scaffold that can be connected to Qiskit later.

## What is included

- A formal project proposal in `docs/proposal.md`.
- A small Python package in `src/quantum_credit_risk`.
- Synthetic credit portfolio generation.
- Classical Monte Carlo and exact-enumeration risk analytics.
- A quantum-ready interface for future QAE integration.
- Unit tests that run with the Python standard library only.

## Quick start

```bash
python -m quantum_credit_risk.cli --portfolio-size 8 --trials 5000 --confidence 0.95
```

Or, if you prefer an explicit `PYTHONPATH`:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --trials 5000 --confidence 0.95
```

## Project roadmap

1. Build the classical benchmark.
2. Validate expected loss, VaR, and CVaR on small portfolios.
3. Replace the `QuantumRiskEngine` stub with a Qiskit-powered iterative amplitude estimation implementation.
4. Compare estimation accuracy, sampling cost, and runtime.

## Files

- `docs/proposal.md`: proposal and implementation plan.
- `src/quantum_credit_risk/portfolio.py`: borrower and portfolio models.
- `src/quantum_credit_risk/classical.py`: Monte Carlo and exact analytics.
- `src/quantum_credit_risk/quantum.py`: QAE integration scaffold.
- `src/quantum_credit_risk/cli.py`: command-line demo.
- `tests/test_risk_metrics.py`: regression-style tests for the baseline.

## Next upgrade for a real quantum run

Install `qiskit` and `qiskit-finance`, then implement the `QuantumRiskEngine.estimate_*` methods using:

- state preparation for the portfolio loss distribution,
- a threshold oracle for the loss event,
- iterative amplitude estimation for EL/VaR/CVaR.

