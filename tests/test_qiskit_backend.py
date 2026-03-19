import unittest

from quantum_credit_risk.qiskit_backend import OFFICIAL_REFERENCES, detect_qiskit_backend


class QiskitBackendTests(unittest.TestCase):
    def test_detect_qiskit_backend_returns_status(self):
        status = detect_qiskit_backend()
        self.assertIsInstance(status.available, bool)
        self.assertIsInstance(status.installed_versions, dict)
        self.assertIsInstance(status.missing_packages, list)
        self.assertTrue(status.install_command().startswith("python -m pip install "))

    def test_official_references_include_credit_risk(self):
        urls = [reference.url for reference in OFFICIAL_REFERENCES]
        self.assertTrue(any("credit_risk_analysis" in url for url in urls))


if __name__ == "__main__":
    unittest.main()
