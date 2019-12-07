import typing as t
import math


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
