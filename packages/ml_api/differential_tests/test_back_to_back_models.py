from .compare import compare_differences

from regression_model



def test_model_prediction_differentials():

    compare_differences(
        expected_predictions=expected_results,
        actual_predictions=actual_results,
        rel_tol=args.rel_tol,
        abs_tol=args.abs_tol,
    )