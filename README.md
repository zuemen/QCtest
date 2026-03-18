# Quantum Credit Risk Engine using Amplitude Estimation

This repository now includes a **directly runnable local quantum mode** for credit-risk estimation. It does not depend on Qiskit, so you can run it immediately in this environment. The local quantum mode simulates the measurement behavior of an ideal amplitude-estimation routine and uses it to estimate expected loss and VaR on a small synthetic credit portfolio, with a hybrid CVaR calculation.

## What is included

- A formal project proposal in `docs/proposal.md`.
- A Python package in `src/quantum_credit_risk`.
- Synthetic credit portfolio generation.
- Classical Monte Carlo and exact-enumeration risk analytics.
- A dependency-free local amplitude-estimation simulator.
- A CLI that can run classical, quantum, or compare mode.
- Unit tests that run with the Python standard library only.

## Quick start

Run both the classical and local quantum modes:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --trials 5000 --confidence 0.95 --mode compare
```

Run only the local quantum mode:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --confidence 0.95 --mode quantum --shots 512 --num-eval-qubits 7
```

## Modes

- `classical`: Monte Carlo baseline.
- `quantum`: directly runnable local amplitude-estimation mode.
- `compare`: classical baseline + exact benchmark + local quantum mode.

## What the local quantum mode does

- **Expected loss**: estimates each borrower's default probability with a local amplitude-estimation simulator and aggregates borrower-level loss contributions.
- **VaR**: scans exact discrete loss thresholds and estimates the CDF at each threshold with the local amplitude-estimation simulator.
- **CVaR**: uses the local-ae VaR estimate together with the exact tail distribution as a hybrid first-step implementation.

This is intentionally a practical bridge: you can run a quantum-style estimation workflow right now, then swap the backend to Qiskit Aer later.

## If Qiskit Aer becomes available

The `QuantumRiskEngine` interface is designed so the current local estimator can be replaced by:

- Qiskit state preparation,
- amplitude-estimation circuits,
- Aer-based simulation,
- and later hardware execution.

