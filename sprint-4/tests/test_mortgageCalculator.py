import unittest
from Sprint 4.mortgageCalculator import calculate_mortgage

class TestMortgageCalculator(unittest.TestCase):

    def test_scenario_01(self):
        # Scenario 01: Valid inputs, no errors
        principal = 300000
        annual_interest_rate = 4.0
        num_years = 30

        expected_result = 1432.25  # Expected monthly payment

        result = calculate_mortgage(principal, annual_interest_rate, num_years)
        self.assertAlmostEqual(result, expected_result, delta=0.01)

    def test_scenario_02(self):
        # Scenario 02: Home price is zero, should raise ValueError
        principal = 0
        annual_interest_rate = 3.5
        num_years = 15

        with self.assertRaises(ValueError):
            calculate_mortgage(principal, annual_interest_rate, num_years)

    def test_scenario_03(self):
        # Scenario 03: Negative loan term, should raise ValueError
        principal = 250000
        annual_interest_rate = 4.25
        num_years = -5

        with self.assertRaises(ValueError):
            calculate_mortgage(principal, annual_interest_rate, num_years)

    def test_scenario_04(self):
        # Scenario 04: Zero annual interest rate, should raise ValueError
        principal = 400000
        annual_interest_rate = 0
        num_years = 20

        try:
            calculate_mortgage(principal, annual_interest_rate, num_years)
        except ValueError as e:
            self.assertEqual(str(e), "Annual interest rate must be greater than zero")
        else:
            self.fail("Expected ValueError not raised")

    def test_scenario_05(self):
        # Scenario 05: Valid inputs, no errors
        principal = 350000
        annual_interest_rate = 4.5
        num_years = 30

        expected_result = 1773.40  # Corrected expected monthly payment

        result = calculate_mortgage(principal, annual_interest_rate, num_years)
        self.assertAlmostEqual(result, expected_result, delta=0.01)

    def test_scenario_06(self):
        # Scenario 06: Valid inputs, no errors
        principal = 280000
        annual_interest_rate = 5.75
        num_years = 10

        expected_result = 3073.54  # Corrected expected monthly payment

        result = calculate_mortgage(principal, annual_interest_rate, num_years)
        self.assertAlmostEqual(result, expected_result, delta=0.01)

    def test_scenario_07(self):
        # Scenario 07: Valid inputs, no errors
        principal = 500000
        annual_interest_rate = 3.75
        num_years = 15

        expected_result = 3636.12  # Corrected expected monthly payment

        result = calculate_mortgage(principal, annual_interest_rate, num_years)
        self.assertAlmostEqual(result, expected_result, delta=0.01)

    def test_scenario_08(self):
        # Scenario 08: Valid inputs, no errors
        principal = 320000
        annual_interest_rate = 4.0
        num_years = 25

        expected_result = 1689.08  # Corrected expected monthly payment

        result = calculate_mortgage(principal, annual_interest_rate, num_years)
        self.assertAlmostEqual(result, expected_result, delta=0.01)