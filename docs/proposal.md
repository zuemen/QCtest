# Proposal: Quantum Credit Risk Engine using Amplitude Estimation

## 1. Project title

**Quantum Credit Risk Engine using Amplitude Estimation**

## 2. Background and motivation

Credit portfolio analysis estimates how much loss a lender may suffer from borrower defaults. Common risk metrics include expected loss (EL), value at risk (VaR), and conditional value at risk (CVaR). In classical finance workflows, these metrics are often estimated with Monte Carlo simulation, which can become expensive when the portfolio grows or when tail-risk precision is required.

Quantum Amplitude Estimation (QAE) is a promising quantum algorithmic primitive because it targets probability and expectation estimation directly. In theory, it offers a quadratic speedup in query complexity over plain Monte Carlo sampling. This makes QAE a natural candidate for credit risk estimation, especially for portfolio-loss probabilities and tail metrics such as VaR and CVaR.

This proposal is explicitly aligned with the official Qiskit Finance materials, especially the tutorials on Quantum Amplitude Estimation and Credit Risk Analysis, as well as the `GaussianConditionalIndependenceModel` API used in the finance credit-risk stack.

## 3. Official Qiskit Finance references

- Tutorials index: https://qiskit-community.github.io/qiskit-finance/tutorials/index.html
- Quantum Amplitude Estimation tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html
- Credit Risk Analysis tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/09_credit_risk_analysis.html
- `GaussianConditionalIndependenceModel` API reference: https://qiskit-community.github.io/qiskit-finance/stubs/qiskit_finance.circuit.library.GaussianConditionalIndependenceModel.html

## 4. Problem statement

This project asks:

1. Can QAE be used to estimate expected loss and tail-risk metrics for a credit portfolio?
2. How does a QAE-based workflow compare with classical Monte Carlo on a small synthetic portfolio?
3. What practical limitations arise from state preparation, discretization, circuit depth, and package/runtime availability?

## 5. Objectives

### Primary objective
Build a small, reproducible credit risk analytics engine that estimates:

- Expected Loss (EL)
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)

using a classical baseline today, a directly runnable local amplitude-estimation mode in constrained environments, and a Qiskit Finance/Aer upgrade path for a more realistic quantum workflow.

### Secondary objectives

- Generate synthetic borrower portfolios with PD, LGD, EAD, and correlation sensitivity.
- Support both independent-default and common-factor simulation logic.
- Provide exact-enumeration analytics for small portfolios to validate Monte Carlo outputs.
- Define a clean software interface for upgrading the local estimator to a Qiskit Aer-backed Iterative Amplitude Estimation workflow.
- Make the package and documentation professional enough to serve as a portfolio project or research prototype.

## 6. Scope

### In scope for the current repository version

- Small synthetic portfolios (5 to 12 borrowers)
- Classical Monte Carlo estimation
- Exact discrete enumeration for validation on small portfolios
- CLI demo and automated tests
- A dependency-free local amplitude-estimation mode
- Explicit Qiskit Finance stack detection and installation guidance
- Documentation aligned with official Qiskit Finance references

### Out of scope for the current repository version

- Real banking data
- Large-scale production optimization
- A tested full Qiskit Aer implementation inside this constrained environment
- Hardware execution on noisy quantum devices

## 7. Methodology

### 7.1 Portfolio model
Each borrower is represented by:

- `pd`: probability of default
- `lgd`: loss given default
- `ead`: exposure at default
- `rho`: loading on a common macro factor

Portfolio loss is defined as:

\[
L = \sum_i EAD_i \cdot LGD_i \cdot 1_{\text{default}_i}
\]

### 7.2 Classical benchmark
The initial benchmark uses Monte Carlo simulation.

Workflow:
1. Sample a common macro factor.
2. Convert unconditional PD and `rho` into conditional default triggers.
3. Generate borrower defaults.
4. Compute portfolio loss.
5. Aggregate losses across trials.
6. Estimate EL, VaR, and CVaR.

### 7.3 Direct-run local quantum mode
Because this environment may not have Qiskit packages installed, the repository includes a dependency-free local amplitude-estimation simulator. This mode approximates the measurement behavior of an ideal amplitude-estimation routine for a target probability and uses it to estimate borrower PDs and portfolio CDF thresholds.

Current direct-run workflow:
1. Generate a synthetic portfolio.
2. Estimate borrower default probabilities with the local amplitude-estimation simulator.
3. Aggregate borrower-level expected-loss contributions.
4. Estimate CDF values at loss thresholds to approximate VaR.
5. Use the estimated VaR together with the exact tail distribution for a hybrid CVaR result.

### 7.4 Target Qiskit Finance workflow
The long-term professional target follows the official credit-risk design used in Qiskit Finance:

1. Use `GaussianConditionalIndependenceModel` to model correlated defaults.
2. Build the loss register and objective function for EL, CDF, VaR, or CVaR.
3. Define an `EstimationProblem` for the target probability or payoff.
4. Run Iterative Amplitude Estimation from the Qiskit algorithms stack.
5. Execute locally with Aer and compare against classical and exact baselines.

## 8. Deliverables

- Proposal document
- Python package for synthetic portfolio generation and risk analytics
- Command-line demo
- Automated tests
- README with setup, references, and architecture notes
- Qiskit stack detection and install guidance

## 9. Evaluation plan

The current release will evaluate:

- Monte Carlo EL vs exact EL
- Monte Carlo VaR/CVaR vs exact VaR/CVaR
- Local quantum EL vs exact EL
- Stability as trial count, shots, and evaluation-qubit count increase
- Sensitivity to confidence level and borrower correlation

A later Qiskit-backed release will add:

- Aer-based QAE estimate vs exact value
- Query/sample complexity comparison
- Circuit-depth and qubit-cost discussion
- Comparison against the official Qiskit Finance tutorial workflow

## 10. Timeline

### Week 1
- Finalize proposal
- Implement synthetic portfolio model
- Implement exact analytics

### Week 2
- Implement Monte Carlo simulator
- Add CLI and tests
- Validate EL, VaR, and CVaR

### Week 3
- Add Qiskit stack detection and professional documentation
- Map loss threshold estimation to official Qiskit Finance building blocks
- Prepare experimental notebooks or scripts for Aer once the environment permits

### Week 4
- Run classical vs quantum experiments
- Upgrade to Aer-backed execution if package installation becomes available
- Prepare charts and final presentation

## 11. Risks and limitations

- Practical quantum advantage may not appear on small current-era devices.
- State preparation can dominate total circuit cost.
- Portfolio discretization may introduce approximation error.
- Synthetic data improves reproducibility but limits realism.
- Environment-level package restrictions may block immediate Qiskit Aer execution.

## 12. Expected outcome

By the end of the current phase, this project provides a usable baseline credit risk engine, a directly runnable local quantum-style mode, and a more professional Qiskit Finance-aligned architecture. This makes it a stronger portfolio piece for quantum finance learning, research proposals, and future extension into stress testing or a full Qiskit Aer implementation.
