import typing as t
import math


def compare_differences(
    *,
    expected_predictions: t.List,
    actual_predictions: t.List,
    rel_tol: t.Optional[float] = None,
    abs_tol: t.Optional[float] = None,
) -> None:
    only_in_expected = set(expected_predictions) - set(actual_predictions)

    if only_in_expected:
        raise ValueError(f"Missing predictions: {', '.join(only_in_expected)}")

    only_in_actual = set(actual_predictions) - set(expected_predictions)

    if only_in_actual:
        raise ValueError(f"Unexpected predictions: {', '.join(only_in_actual)}")

    thresholds = {}

    if abs_tol is not None:
        thresholds["abs_tol"] = abs_tol

    if rel_tol is not None:
        thresholds["rel_tol"] = rel_tol

    for index, (actual_prediction, expected_prediction) in enumerate(zip(
    actual_predictions['predictions'], expected_predictions['predictions'])):

        if not math.isclose(expected_prediction, actual_prediction, **thresholds):
            raise ValueError(
                f"Probability for prediction {index} has changed: "
                f"{expected_prediction} (expected) vs "
                f"{actual_prediction} (actual)"
            )