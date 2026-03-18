# Proposal: Quantum Credit Risk Engine using Amplitude Estimation

## 1. Project title

**Quantum Credit Risk Engine using Amplitude Estimation**

## 2. Background and motivation

Credit portfolio analysis estimates how much loss a lender may suffer from borrower defaults. Common risk metrics include expected loss (EL), value at risk (VaR), and conditional value at risk (CVaR). In classical finance workflows, these metrics are often estimated with Monte Carlo simulation, which can become expensive when the portfolio grows or when tail-risk precision is required.

Quantum Amplitude Estimation (QAE) is a promising quantum algorithmic primitive because it targets probability and expectation estimation directly. In theory, it offers a quadratic speedup in query complexity over plain Monte Carlo sampling. This makes QAE a natural candidate for credit risk estimation, especially for portfolio-loss probabilities and tail metrics such as VaR and CVaR.

## 3. Problem statement

This project asks:

1. Can QAE be used to estimate expected loss and tail-risk metrics for a credit portfolio?
2. How does a QAE-based workflow compare with classical Monte Carlo on a small synthetic portfolio?
3. What practical limitations arise from state preparation, discretization, and circuit complexity?

## 4. Objectives

### Primary objective
Build a small, reproducible credit risk analytics engine that estimates:

- Expected Loss (EL)
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)

using a classical baseline today and a directly runnable local amplitude-estimation mode, while keeping the design ready for later Qiskit Aer integration.

### Secondary objectives

- Generate synthetic borrower portfolios with PD, LGD, EAD, and correlation sensitivity.
- Support both independent-default and common-factor simulation logic.
- Provide exact-enumeration analytics for small portfolios to validate Monte Carlo outputs.
- Define a clean software interface for upgrading the local estimator to a Qiskit Aer-backed Iterative Amplitude Estimation workflow in a later phase.

## 5. Scope

### In scope for the initial implementation

- Small synthetic portfolios (5 to 12 borrowers)
- Classical Monte Carlo estimation
- Exact discrete enumeration for validation on small portfolios
- CLI demo and automated tests
- Proposal, architecture, and a directly runnable local amplitude-estimation mode

### Out of scope for the first version

- Real banking data
- Large-scale production optimization
- Full Qiskit Aer integration inside this repository version
- Hardware execution on noisy quantum devices

## 6. Methodology

### 6.1 Portfolio model
Each borrower is represented by:

- `pd`: probability of default
- `lgd`: loss given default
- `ead`: exposure at default
- `rho`: loading on a common macro factor

Portfolio loss is defined as:

\[
L = \sum_i EAD_i \cdot LGD_i \cdot 1_{\text{default}_i}
\]

### 6.2 Classical benchmark
The initial benchmark uses Monte Carlo simulation.

Workflow:
1. Sample a common macro factor.
2. Convert unconditional PD and `rho` into conditional default triggers.
3. Generate borrower defaults.
4. Compute portfolio loss.
5. Aggregate losses across trials.
6. Estimate EL, VaR, and CVaR.

### 6.3 Exact validation
For small portfolios, the project enumerates all default states to compute the exact discrete loss distribution. This serves as a correctness check against Monte Carlo outputs.

### 6.4 Direct-run quantum mode and upgrade plan
The software now provides a dependency-free local amplitude-estimation simulator so the project is runnable immediately. This local mode approximates the measurement behavior of an ideal amplitude-estimation routine for a target probability and uses it to estimate borrower PDs and portfolio CDF thresholds.

Current direct-run workflow:
1. Generate a synthetic portfolio.
2. Estimate borrower default probabilities with the local amplitude-estimation simulator.
3. Aggregate borrower-level expected-loss contributions.
4. Estimate CDF values at loss thresholds to approximate VaR.
5. Use the estimated VaR together with the exact tail distribution for a hybrid CVaR result.

Future Qiskit Aer upgrade path:
1. Encode the portfolio loss distribution into a quantum state.
2. Build an objective qubit that marks a loss event or payoff.
3. Define an estimation problem for EL or threshold probability.
4. Use Iterative Amplitude Estimation on Aer to estimate amplitudes.
5. Recover EL, VaR, or CVaR from the estimated amplitudes.

## 7. Deliverables

- Proposal document
- Python package for synthetic portfolio generation and risk analytics
- Command-line demo
- Automated tests
- README with setup and roadmap

## 8. Evaluation plan

The first release will evaluate:

- Monte Carlo EL vs exact EL
- Monte Carlo VaR/CVaR vs exact VaR/CVaR
- Stability as trial count increases
- Sensitivity to confidence level and borrower correlation

The later quantum release will add:

- QAE estimate vs exact value
- Query/sample complexity comparison
- Circuit-depth and qubit-cost discussion

## 9. Timeline

### Week 1
- Finalize proposal
- Implement synthetic portfolio model
- Implement exact analytics

### Week 2
- Implement Monte Carlo simulator
- Add CLI and tests
- Validate EL, VaR, and CVaR

### Week 3
- Add Qiskit integration points
- Map loss threshold estimation to amplitude estimation problems
- Prepare experimental notebooks

### Week 4
- Run classical vs quantum experiments
- Prepare charts and final presentation

## 10. Risks and limitations

- Practical quantum advantage may not appear on small current-era devices.
- State preparation can dominate total circuit cost.
- Portfolio discretization may introduce approximation error.
- Synthetic data improves reproducibility but limits realism.

## 11. Expected outcome

By the end of the first phase, this project will provide a usable baseline credit risk engine and a clean path toward a genuine QAE implementation. That makes it a strong portfolio piece for quantum finance learning, research proposals, and future extension into stress testing or hybrid quantum-classical workflows.
