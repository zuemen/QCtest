# Quantum Credit Risk Engine using Amplitude Estimation

This repository now has two professional layers:

1. a **directly runnable local quantum mode** that works without external dependencies, and
2. an **explicit Qiskit Finance integration path** that documents the package stack, official references, and the target backend architecture.

That means you can run the project immediately today, while also seeing clearly how it should evolve toward a Qiskit Finance / Qiskit Aer implementation.

## Official Qiskit Finance references

This project is aligned with the official Qiskit Finance materials:

- Qiskit Finance tutorials index: https://qiskit-community.github.io/qiskit-finance/tutorials/index.html
- Quantum Amplitude Estimation tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html
- Credit Risk Analysis tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/09_credit_risk_analysis.html
- `GaussianConditionalIndependenceModel` API: https://qiskit-community.github.io/qiskit-finance/stubs/qiskit_finance.circuit.library.GaussianConditionalIndependenceModel.html

## What is included

- A formal project proposal in `docs/proposal.md`.
- A Python package in `src/quantum_credit_risk`.
- Synthetic credit portfolio generation.
- Classical Monte Carlo and exact-enumeration risk analytics.
- A dependency-free local amplitude-estimation simulator.
- A CLI that can run classical, quantum, or compare mode.
- Qiskit-stack detection and installation guidance.
- Unit tests that run with the Python standard library only.

## Install guidance

### Direct-run mode only

No external quantum packages are required for the local mode already included in this repo.

### Qiskit Finance stack

If your environment can install packages, use either of these:

```bash
python -m pip install -e '.[qiskit]'
```

or:

```bash
python -m pip install -r requirements-qiskit.txt
```

The optional Qiskit stack declared by this repo is:

- `qiskit>=1.0`
- `qiskit-aer>=0.14`
- `qiskit-algorithms>=0.3`
- `qiskit-finance>=0.4`

## Quick start

Run both the classical and local quantum modes:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --trials 5000 --confidence 0.95 --mode compare
```

Run only the local quantum mode:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --confidence 0.95 --mode quantum --shots 512 --num-eval-qubits 7
```

Show Qiskit stack status and official references:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --show-qiskit-status
```

## Modes

- `classical`: Monte Carlo baseline.
- `quantum`: directly runnable local amplitude-estimation mode.
- `compare`: classical baseline + exact benchmark + local quantum mode.

## What the local quantum mode does

- **Expected loss**: estimates each borrower's default probability with a local amplitude-estimation simulator and aggregates borrower-level loss contributions.
- **VaR**: scans exact discrete loss thresholds and estimates the CDF at each threshold with the local amplitude-estimation simulator.
- **CVaR**: uses the local-AE VaR estimate together with the exact tail distribution as a hybrid first-step implementation.

## Target Qiskit Finance architecture

This repository now explicitly tracks the official Qiskit Finance credit-risk architecture:

- `GaussianConditionalIndependenceModel` for the latent credit factor model,
- a weighted-loss construction for portfolio loss,
- a threshold/payoff objective for CDF, VaR, or CVaR,
- amplitude estimation using the Qiskit algorithms stack,
- and local simulation on Aer when available.

## Why this structure is more professional

Instead of pretending Qiskit is already installed, the repository now:

- tells you exactly which Qiskit packages belong in the stack,
- gives you the install commands,
- points you to the official finance tutorials and API docs,
- and keeps a runnable fallback mode so the project remains executable in restricted environments.

