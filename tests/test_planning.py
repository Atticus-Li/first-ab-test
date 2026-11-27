"""Checks actual calculations and failure paths, not skill wording."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/plan-first-ab-test/scripts/plan_binary_test.py"
SPEC = importlib.util.spec_from_file_location("planner", SCRIPT)
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)


class PlanningTests(unittest.TestCase):
    def test_published_r_benchmark_is_per_group_and_rounded_up(self):
        # R power.prop.test(p1=.50, p2=.75, power=.90) reports n≈76.7.
        self.assertEqual(planner.sample_per_group(0.50, 0.75, power=0.90), 77)

    def test_known_formula_example(self):
        self.assertEqual(planner.sample_per_group(0.05, 0.06), 8158)

    def test_calendar_adds_followup_after_final_enrollment(self):
        row = planner.make_plan(0.05, 2000, 10, 0.20, 7)["scenarios"][0]
        self.assertEqual(row["sample_per_group"], 8158)
        self.assertEqual(row["total_sample"], 16316)
        self.assertEqual(row["enrollment_days_estimate"], 58)
        self.assertEqual(row["earliest_readout_days_estimate"], 65)
        self.assertTrue(row["sample_fits_window"])
        self.assertAlmostEqual(row["target_rate"], 0.06)
        self.assertAlmostEqual(row["absolute_change_percentage_points"], 1.0)

    def test_followup_can_change_window_verdict(self):
        no_delay = planner.make_plan(0.05, 2000, 9, 0.20)["scenarios"][0]
        delayed = planner.make_plan(0.05, 2000, 9, 0.20, 7)["scenarios"][0]
        self.assertTrue(no_delay["sample_fits_window"])
        self.assertFalse(delayed["sample_fits_window"])

    def test_low_traffic_is_a_duration_constraint_not_a_universal_cutoff(self):
        short = planner.make_plan(0.05, 100, 4, 0.20)["scenarios"][0]
        long = planner.make_plan(0.05, 100, 200, 0.20)["scenarios"][0]
        self.assertFalse(short["sample_fits_window"])
        self.assertTrue(long["sample_fits_window"])
        self.assertEqual(short["sample_per_group"], long["sample_per_group"])

    def test_scenarios_do_not_choose_a_business_target(self):
        plan = planner.make_plan(0.05, 10000, 4)
        self.assertTrue(plan["effects_are_illustrative"])
        self.assertEqual([s["relative_mde"] for s in plan["scenarios"]], [0.10, 0.20, 0.30])
        self.assertGreater(plan["scenarios"][0]["sample_per_group"], plan["scenarios"][1]["sample_per_group"])

    def test_sparse_expected_cells_require_method_review(self):
        row = planner.make_plan(0.00001, 10000, 4, 80000)["scenarios"][0]
        self.assertEqual(row["status"], "method_review_needed")
        self.assertIsNone(row["sample_fits_window"])

    def test_invalid_scenarios_near_one_are_not_fabricated(self):
        rows = planner.make_plan(0.90, 1000, 4)["scenarios"]
        self.assertEqual(rows[1]["status"], "invalid_target_rate")
        self.assertIsNone(rows[1]["sample_fits_window"])

    def test_invalid_design_is_rejected_even_if_all_default_targets_are_invalid(self):
        for parameter in [{"alpha": float("nan")}, {"power": float("nan")},
                          {"alpha": 0.9}, {"power": 0.1}]:
            with self.subTest(parameter=parameter), self.assertRaises(ValueError):
                planner.make_plan(0.99, 1000, 4, **parameter)

    def test_input_failures_never_produce_a_plan(self):
        cases = [(0, 1000, 4, 0.2), (1, 1000, 4, 0.2),
                 (float("nan"), 1000, 4, 0.2), (0.05, float("inf"), 4, 0.2),
                 (0.05, 0, 4, 0.2), (0.05, 1000, 0, 0.2),
                 (0.05, 1000, 4, 0), (0.05, 1000, 4, -0.2),
                 (0.9, 1000, 4, 0.2), (0.05, 1000, 4, 1e-300),
                 (True, 1000, 4, 0.2)]
        for values in cases:
            with self.subTest(values=values), self.assertRaises(ValueError):
                planner.make_plan(*values)
        for arguments in [{"alpha": 0}, {"alpha": float("nan")},
                          {"power": 1}, {"power": 0.4},
                          {"followup_days": -1}, {"followup_days": 0.5}]:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                planner.make_plan(0.05, 1000, 4, 0.20, **arguments)

    def test_calendar_accounts_for_incomplete_days_and_no_enrollment_time(self):
        plan = planner.make_plan(0.05, 1000, 1, 0.2, 14)
        self.assertEqual(plan["scenarios"][0]["available_sample_per_group_by_deadline"], 0)
        self.assertFalse(plan["scenarios"][0]["sample_fits_window"])

    def test_cli_success_and_failures(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--baseline", ".05",
                              "--weekly-eligible", "2000", "--weeks", "4"],
                             capture_output=True, text=True, timeout=5)
        self.assertEqual(run.returncode, 0)
        self.assertEqual(len(json.loads(run.stdout)["scenarios"]), 3)
        bad = subprocess.run([sys.executable, str(SCRIPT), "--baseline", "nan",
                              "--weekly-eligible", "2000", "--weeks", "4"],
                             capture_output=True, text=True, timeout=5)
        self.assertNotEqual(bad.returncode, 0)
        self.assertEqual(bad.stdout, "")
        self.assertNotIn("Traceback", bad.stderr)


if __name__ == "__main__":
    unittest.main()
