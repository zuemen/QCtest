# Proposal: Quantum Credit Risk Engine using Amplitude Estimation

## 1. Project title

**Quantum Credit Risk Engine using Amplitude Estimation**

## 2. Background and motivation

Credit portfolio analysis estimates how much loss a lender may suffer from borrower defaults. Common risk metrics include expected loss (EL), value at risk (VaR), conditional value at risk (CVaR), and economic capital (EC). In classical finance workflows, these metrics are often estimated with Monte Carlo simulation, which can become expensive when the portfolio grows or when tail-risk precision is required.

Quantum Amplitude Estimation (QAE) is a promising quantum algorithmic primitive because it targets probability and expectation estimation directly. In theory, it offers a quadratic speedup in query complexity over plain Monte Carlo sampling. This makes QAE a natural candidate for credit risk estimation, especially for portfolio-loss probabilities and tail metrics.

This proposal is aligned with two primary sources:

1. the official Qiskit Finance tutorials on amplitude estimation and credit risk, and
2. the paper *A More General Quantum Credit Risk Analysis Framework* (Entropy 2023), which extends the professional framing beyond the original toy-model setup by supporting richer inputs, multiple systemic factors, and a more flexible loss-evaluation strategy.

## 3. References

### Paper
- Ferracin, Finžgar, Zheng, Woerner, Egger, and Gambella, **"A More General Quantum Credit Risk Analysis Framework"**, *Entropy* 25(4):593, 2023: https://www.mdpi.com/1099-4300/25/4/593

### Official Qiskit Finance material
- Tutorials index: https://qiskit-community.github.io/qiskit-finance/tutorials/index.html
- Quantum Amplitude Estimation tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/00_amplitude_estimation.html
- Credit Risk Analysis tutorial: https://qiskit-community.github.io/qiskit-finance/tutorials/09_credit_risk_analysis.html
- `GaussianConditionalIndependenceModel` API reference: https://qiskit-community.github.io/qiskit-finance/stubs/qiskit_finance.circuit.library.GaussianConditionalIndependenceModel.html

## 4. Key design principles derived from the paper

The paper suggests several improvements that make a credit-risk framework more realistic and more scalable than a narrow tutorial-style implementation. This repository now follows those design principles more closely:

1. **Multiple systemic risk factors** should be supported, rather than assuming a single common latent factor for all assets.
2. **Floating-point LGD and exposure values** should be treated as natural financial inputs.
3. The framework should support multiple output metrics, especially **EL, VaR, CVaR, and EC**.
4. The software architecture should distinguish between a current practical execution path and a future high-fidelity quantum path.
5. The quantum path should remain compatible with the official Qiskit Finance credit-risk building blocks.

## 5. Objectives

### Primary objective
Build a small, reproducible credit risk analytics engine that estimates:

- Expected Loss (EL)
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)
- Economic Capital (EC)

using a classical baseline today, a directly runnable local amplitude-estimation mode in constrained environments, and a Qiskit Finance/Aer upgrade path for a more realistic quantum workflow.

### Secondary objectives

- Generate synthetic borrower portfolios with PD, LGD, EAD, and **multiple factor loadings**.
- Support both exact discrete validation and Monte Carlo simulation.
- Keep the package runnable even when Qiskit packages are unavailable.
- Align the design narrative with the referenced paper and the official Qiskit Finance stack.

## 6. Scope

### In scope for the current repository version

- Small synthetic portfolios (5 to 12 borrowers)
- Multiple systemic factors in the classical portfolio model
- Classical Monte Carlo estimation
- Exact discrete enumeration for validation on small portfolios
- CLI demo and automated tests
- A dependency-free local amplitude-estimation mode
- Explicit Qiskit Finance stack detection and installation guidance
- Documentation aligned with the paper and official Qiskit Finance references

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
- `factor_loadings`: loadings on one or more systemic factors

Portfolio loss is defined as:

\[
L = \sum_i EAD_i \cdot LGD_i \cdot 1_{\text{default}_i}
\]

### 7.2 Classical benchmark
The benchmark uses a Monte Carlo model with multiple systemic factors and an idiosyncratic residual component.

Workflow:
1. Sample the systemic factors.
2. Sample the idiosyncratic component for each borrower.
3. Form a latent asset variable using the borrower's factor loadings.
4. Trigger default when the latent variable crosses the PD threshold.
5. Compute portfolio loss.
6. Estimate EL, VaR, CVaR, and EC.

### 7.3 Direct-run local quantum mode
Because this environment may not have Qiskit packages installed, the repository includes a dependency-free local amplitude-estimation simulator. This mode is not a substitute for Qiskit, but it preserves the project’s runnable status and provides a simple approximation workflow for:

- borrower-level probability estimation,
- CDF threshold estimation,
- VaR approximation,
- hybrid CVaR,
- and EC reporting.

### 7.4 Target Qiskit Finance workflow
The long-term professional target follows the official credit-risk design used in Qiskit Finance and the more general perspective advocated by the paper:

1. Use `GaussianConditionalIndependenceModel` or an extended multi-factor latent model.
2. Build the loss/objective evaluation circuit without forcing unrealistic integer-only portfolio assumptions where possible.
3. Define an `EstimationProblem` for the desired metric.
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
- Monte Carlo VaR/CVaR/EC vs exact VaR/CVaR/EC
- Local quantum EL vs exact EL
- Stability as trial count, shots, and evaluation-qubit count increase
- Sensitivity to confidence level and factor configuration

A later Qiskit-backed release will add:

- Aer-based QAE estimate vs exact value
- Query/sample complexity comparison
- Circuit-depth and qubit-cost discussion
- Comparison against the official Qiskit Finance tutorial workflow and the general paper framework

## 10. Risks and limitations

- Practical quantum advantage may not appear on small current-era devices.
- State preparation can dominate total circuit cost.
- Portfolio discretization may introduce approximation error.
- Synthetic data improves reproducibility but limits realism.
- Environment-level package restrictions may block immediate Qiskit Aer execution.

## 11. Expected outcome

By the end of the current phase, this project provides a usable baseline credit risk engine, a directly runnable local quantum-style mode, and a code/documentation structure that is more faithful to the professional framing of the cited paper. This makes it a stronger portfolio piece for quantum finance learning, research proposals, and future extension into stress testing or a full Qiskit Aer implementation.
