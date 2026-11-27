#!/usr/bin/env python3
"""Offline planning estimates; two equal independent groups, binary increase.

Uses the same normal-approximation sample formula as GrowthLayer's
calculateSampleSize. It is a narrow planning aid, not a results analyzer.
Python 3.8+ standard library only. No network, files, credentials or telemetry.
"""
import argparse
import json
import math
from statistics import NormalDist


def finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(name + " must be a finite number.")
    if not math.isfinite(value):
        raise ValueError(name + " must be a finite number.")
    return value


def sample_per_group(baseline, target, alpha=0.05, power=0.80):
    """Two-sided normal approximation, no continuity correction; ceil per arm."""
    for value, name in [(baseline, "baseline"), (target, "target"),
                        (alpha, "alpha"), (power, "power")]:
        finite_number(value, name)
    if not 0 < baseline < target < 1:
        raise ValueError("Require 0 < baseline < target < 1 for an increase.")
    if not 0 < alpha < 0.5 or not 0.5 < power < 1:
        raise ValueError("Require 0 < alpha < 0.5 and 0.5 < power < 1.")
    pooled = (baseline + target) / 2
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    numerator = (z_alpha * math.sqrt(2 * pooled * (1 - pooled))
                 + z_power * math.sqrt(baseline * (1 - baseline)
                                       + target * (1 - target))) ** 2
    denominator = (target - baseline) ** 2
    if denominator == 0:
        raise ValueError("Effect is too small for supported numerical precision.")
    result = numerator / denominator
    if not math.isfinite(result):
        raise ValueError("Inputs exceed the supported numerical range.")
    return math.ceil(result)


def make_plan(baseline, weekly_eligible, weeks, relative_mde=None,
              followup_days=0, alpha=0.05, power=0.80):
    for value, name in [(baseline, "baseline"), (weekly_eligible, "weekly_eligible"),
                        (weeks, "weeks"), (followup_days, "followup_days"),
                        (alpha, "alpha"), (power, "power")]:
        finite_number(value, name)
    if not 0 < alpha < 0.5 or not 0.5 < power < 1:
        raise ValueError("Require 0 < alpha < 0.5 and 0.5 < power < 1.")
    if not 0 < baseline < 1:
        raise ValueError("Baseline must be between 0 and 1; zero-event baselines need method review.")
    if weekly_eligible <= 0 or weeks <= 0:
        raise ValueError("Weekly eligible people and decision weeks must be positive.")
    if followup_days < 0 or int(followup_days) != followup_days:
        raise ValueError("Follow-up days must be a nonnegative integer.")
    if not math.isfinite(weeks * 7) or weeks * 7 < 1:
        raise ValueError("Decision window must be at least one day and within numerical limits.")
    window_days = math.floor(weeks * 7)
    effects = [relative_mde] if relative_mde is not None else [0.10, 0.20, 0.30]
    scenarios = []
    for effect in effects:
        finite_number(effect, "relative_mde")
        if effect <= 0:
            raise ValueError("Relative MDE must be a positive increase, expressed as a proportion.")
        target = baseline * (1 + effect)
        if target >= 1 and relative_mde is None:
            scenarios.append({"relative_mde": effect, "status": "invalid_target_rate",
                              "sample_fits_window": None})
            continue
        n = sample_per_group(baseline, target, alpha, power)
        try:
            raw_days = 2 * n * 7 / weekly_eligible
            available = weekly_eligible * max(0, window_days - followup_days) / 14
        except OverflowError as error:
            raise ValueError("Inputs exceed the supported numerical range.") from error
        if not math.isfinite(raw_days) or not math.isfinite(available):
            raise ValueError("Inputs exceed the supported numerical range.")
        enrollment_days = math.ceil(raw_days)
        readout_days = enrollment_days + int(followup_days)
        expected_counts = [n * baseline, n * (1 - baseline),
                           n * target, n * (1 - target)]
        review = min(expected_counts) < 10
        scenarios.append({
            "relative_mde": effect,
            "target_rate": target,
            "absolute_change_percentage_points": (target - baseline) * 100,
            "sample_per_group": n,
            "total_sample": 2 * n,
            "available_sample_per_group_by_deadline": math.floor(available),
            "enrollment_days_estimate": enrollment_days,
            "earliest_readout_days_estimate": readout_days,
            "sample_fits_window": None if review else readout_days <= window_days,
            "status": "method_review_needed" if review else "planning_estimate",
            "normal_approximation_caution": "Expected success/failure count below 10 in an arm." if review else None,
        })
    return {
        "method": "Two-sided normal-approximation planning, no continuity correction",
        "scope": "Two equally allocated groups; independent people; binary conversion increase; fixed horizon",
        "baseline_rate": baseline,
        "weekly_eligible_people": weekly_eligible,
        "decision_window_days": window_days,
        "outcome_followup_days": int(followup_days),
        "alpha": alpha,
        "power": power,
        "allocation": "50/50",
        "effects_are_illustrative": relative_mde is None,
        "scenarios": scenarios,
        "limits": [
            "A sample fitting the window does not establish business value or launch readiness.",
            "Inputs must describe the same eligible population and independent unit.",
            "Stable traffic is assumed; cycles, ramp-up, exclusions and outcome delays may extend the calendar.",
            "No guarantee of significance, a conclusive result or conversion lift.",
            "No results analysis, clustering, continuous metrics, unequal allocation, multiple variants or sequential inference.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=float, help="Proportion, e.g. 0.05 for 5%%")
    parser.add_argument("--weekly-eligible", required=True, type=float, help="New eligible independent people per week")
    parser.add_argument("--weeks", required=True, type=float, help="Available decision window in weeks")
    parser.add_argument("--relative-mde", type=float, help="Relative increase, e.g. 0.20 for +20%%; omit for scenarios")
    parser.add_argument("--followup-days", type=int, default=0, help="Required observation time after the last entrant")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--power", type=float, default=0.80)
    args = parser.parse_args()
    try:
        plan = make_plan(args.baseline, args.weekly_eligible, args.weeks,
                         args.relative_mde, args.followup_days, args.alpha, args.power)
    except (ValueError, OverflowError) as error:
        parser.error(str(error))
    print(json.dumps(plan, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
