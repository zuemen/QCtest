# Quantum Credit Risk Engine using Amplitude Estimation

This repository now combines three layers:

1. a **classical benchmark** for portfolio-loss analytics,
2. a **directly runnable local quantum mode** for constrained environments, and
3. a **paper-aligned professional design** inspired by the framework in *A More General Quantum Credit Risk Analysis Framework* (Entropy 2023), together with the official Qiskit Finance tutorials.

## Research references used for this design

### Primary paper reference
- Ferracin, Finžgar, Zheng, Woerner, Egger, and Gambella, **"A More General Quantum Credit Risk Analysis Framework"**, *Entropy* 25(4):593, 2023: https://www.mdpi.com/1099-4300/25/4/593

### Official Qiskit Finance references
- Qiskit Finance tutorials index: https://qiskit-community.github.io/qiskit-finance/tutorials/index.html
- Quantum Amplitude Estimation tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html
- Credit Risk Analysis tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/09_credit_risk_analysis.html
- `GaussianConditionalIndependenceModel` API: https://qiskit-community.github.io/qiskit-finance/stubs/qiskit_finance.circuit.library.GaussianConditionalIndependenceModel.html

## What changed to reflect the paper more professionally

Compared with the earlier starter version, this repository now models several ideas that are closer to the paper's framing:

- **multiple systemic risk factors** instead of a single scalar factor loading,
- **floating-point LGD/EAD inputs** as first-class portfolio data,
- explicit support for **expected loss (EL)**, **value at risk (VaR)**, **conditional value at risk (CVaR)**, and **economic capital (EC)**,
- and clearer separation between the current local execution mode and the future Qiskit Finance/Aer workflow.

## What is included

- A formal project proposal in `docs/proposal.md`.
- A Python package in `src/quantum_credit_risk`.
- Synthetic multi-factor credit portfolio generation.
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

## Quick start

Run both the classical and local quantum modes on a two-factor synthetic portfolio:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --portfolio-size 8 --systemic-factors 2 --trials 5000 --confidence 0.95 --mode compare
```

Show Qiskit stack status and official references:

```bash
PYTHONPATH=src python -m quantum_credit_risk.cli --show-qiskit-status
```

## Target architecture

The professional target, consistent with the paper and the official Qiskit Finance credit-risk tutorial, is:

- multi-factor latent credit-risk modeling,
- realistic floating-point portfolio inputs,
- direct loss-threshold evaluation without an oversized sum register where possible,
- amplitude-estimation-based CDF / VaR / CVaR workflows,
- and Aer-backed local execution when the Qiskit stack is available.

## Current limitation

The repository still does **not** ship a tested Aer-backed implementation inside this environment because the container currently lacks installable Qiskit packages. The code now makes that limitation explicit while keeping the project runnable and structurally aligned with the paper's more general framework.
