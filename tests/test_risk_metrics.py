import unittest

from quantum_credit_risk.classical import (
    MonteCarloRiskEngine,
    conditional_value_at_risk_from_distribution,
    economic_capital_from_distribution,
    exact_loss_distribution,
    expected_loss_from_distribution,
    value_at_risk_from_distribution,
)
from quantum_credit_risk.portfolio import Borrower, Portfolio, synthetic_portfolio
from quantum_credit_risk.quantum import LocalAmplitudeEstimator, QuantumRiskEngine


class RiskMetricTests(unittest.TestCase):
    def test_exact_expected_loss_matches_manual_sum(self):
        portfolio = Portfolio(
            [
                Borrower("A", pd=0.1, lgd=0.5, ead=100.0, factor_loadings=(0.1, 0.05)),
                Borrower("B", pd=0.2, lgd=0.4, ead=150.0, factor_loadings=(0.08, 0.03)),
            ]
        )
        distribution = exact_loss_distribution(portfolio)
        expected = (0.1 * 50.0) + (0.2 * 60.0)
        self.assertAlmostEqual(expected_loss_from_distribution(distribution), expected, places=8)

    def test_var_cvar_and_economic_capital_are_ordered(self):
        portfolio = synthetic_portfolio(size=5, seed=11, systemic_factors=2)
        distribution = exact_loss_distribution(portfolio)
        el = expected_loss_from_distribution(distribution)
        var_95 = value_at_risk_from_distribution(distribution, 0.95)
        cvar_95 = conditional_value_at_risk_from_distribution(distribution, 0.95)
        ec_95 = economic_capital_from_distribution(distribution, 0.95)
        self.assertGreaterEqual(cvar_95, var_95)
        self.assertAlmostEqual(ec_95, var_95 - el, places=8)

    def test_monte_carlo_expected_loss_is_close_to_exact(self):
        portfolio = synthetic_portfolio(size=4, seed=5, systemic_factors=2)
        exact_distribution = exact_loss_distribution(portfolio)
        exact_el = expected_loss_from_distribution(exact_distribution)

        engine = MonteCarloRiskEngine(seed=5)
        report = engine.analyze(portfolio, trials=20000, confidence=0.95)
        tolerance = 0.2 * max(exact_el, 1.0)
        self.assertLess(abs(report.expected_loss - exact_el), tolerance)

    def test_local_amplitude_estimator_returns_valid_probability(self):
        estimator = LocalAmplitudeEstimator(num_eval_qubits=6, shots=512, seed=1)
        estimate = estimator.estimate(0.2)
        self.assertGreaterEqual(estimate, 0.0)
        self.assertLessEqual(estimate, 1.0)

    def test_quantum_expected_loss_is_reasonably_close_to_exact(self):
        portfolio = synthetic_portfolio(size=4, seed=2, systemic_factors=2)
        exact_el = expected_loss_from_distribution(exact_loss_distribution(portfolio))
        quantum_engine = QuantumRiskEngine(num_eval_qubits=7, shots=1024, seed=2)
        estimate = quantum_engine.estimate_expected_loss(portfolio).estimate
        tolerance = 0.25 * max(exact_el, 1.0)
        self.assertLess(abs(estimate - exact_el), tolerance)

    def test_portfolio_tracks_multiple_systemic_factors(self):
        portfolio = synthetic_portfolio(size=3, seed=3, systemic_factors=3)
        self.assertEqual(portfolio.systemic_factor_count, 3)
        self.assertTrue(all(len(b.factor_loadings) == 3 for b in portfolio.borrowers))


if __name__ == "__main__":
    unittest.main()
