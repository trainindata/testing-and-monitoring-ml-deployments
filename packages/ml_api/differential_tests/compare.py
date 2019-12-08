import json
import math
import sys
import typing as t
from argparse import Namespace

from termcolor import cprint

from api.config import ROOT


def compare_differences(
    *,
    expected_predictions: t.List,
    actual_predictions: t.List,
    rel_tol: t.Optional[float] = None,
    abs_tol: t.Optional[float] = None,
) -> None:
    """
    :param rel_tol: is the relative tolerance – it is the maximum allowed difference
    between a and b, relative to the larger absolute value of a or b.
    For example, to set a tolerance of 5%, pass rel_tol=0.05. The default
    tolerance is 1e-09, which assures that the two values are the same within
    about 9 decimal digits. rel_tol must be greater than zero.

    :param abs_tol: abs_tol is the minimum absolute tolerance – useful for comparisons
    near zero. abs_tol must be at least zero.
    """
    only_in_expected = len(expected_predictions) - len(actual_predictions)

    if only_in_expected:
        raise ValueError(f"Missing {only_in_expected} predictions")

    only_in_actual = len(actual_predictions) - len(expected_predictions)

    if only_in_actual:
        raise ValueError(f"Found {only_in_actual} unexpected predictions")

    thresholds = {}

    if abs_tol is not None:
        thresholds["abs_tol"] = abs_tol

    if rel_tol is not None:
        thresholds["rel_tol"] = rel_tol

    for index, (actual_prediction, expected_prediction) in enumerate(
        zip(actual_predictions, expected_predictions)
    ):
        if not math.isclose(expected_prediction, actual_prediction, **thresholds):
            raise ValueError(
                f"Price prediction {index} has changed by more "
                f"than the thresholds: {thresholds}: "
                f"{expected_prediction} (expected) vs "
                f"{actual_prediction} (actual)"
            )


def compare_predictions(args: Namespace) -> None:
    expected_results_dir = ROOT / args.expected_results_dir
    actual_results_dir = ROOT / args.actual_results_dir

    expected_results_filenames = list(expected_results_dir.glob("*.json"))

    if not expected_results_filenames:
        print("No results found!")
        sys.exit(1)

    for expected_results_filename in sorted(expected_results_filenames):
        name = expected_results_filename.name
        actual_results_filename = actual_results_dir / name

        print(
            f"Comparing {expected_results_filename} with {actual_results_filename} ... ",
            end="",
        )

        with expected_results_filename.open() as f:
            expected_results = json.load(f)

        with actual_results_filename.open() as f:
            actual_results = json.load(f)

        try:
            compare_differences(
                expected_predictions=expected_results["predictions"],
                actual_predictions=actual_results["predictions"],
                rel_tol=args.rel_tol,
                abs_tol=args.abs_tol,
            )
        except ValueError as exc:
            cprint("ERROR", "red")
            cprint(f"  • {exc}", "red")
        else:
            cprint("OK", "green")
