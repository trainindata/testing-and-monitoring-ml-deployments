from gradient_boosting_model.predict import make_prediction
from gradient_boosting_model.config.core import config

from sklearn.metrics import mean_squared_error

from regression_model.predict import make_prediction as alt_make_prediction


def test_prediction_quality_against_benchmark(raw_training_data, sample_input_data):
    # Given
    input_df = raw_training_data.drop(config.model_config.target, axis=1)
    output_df = raw_training_data[config.model_config.target]

    # Generate rough benchmarks (you would tweak depending on your model)
    benchmark_flexibility = 50000
    benchmark_lower_boundary = (
        round(output_df.iloc[0], ndigits=-4) - benchmark_flexibility
    )  # 160000
    benchmark_upper_boundary = (
        round(output_df.iloc[0], ndigits=-4) + benchmark_flexibility
    )  # 260000

    # When
    subject = make_prediction(input_data=input_df[0:1])

    # Then
    assert subject is not None
    assert isinstance(subject.get("predictions")[0], float)
    prediction = subject.get("predictions")[0]
    assert isinstance(prediction, float)
    assert prediction > benchmark_lower_boundary
    assert prediction < benchmark_upper_boundary


def test_prediction_quality_against_another_model(raw_training_data, sample_input_data):
    # Given
    input_df = raw_training_data.drop(config.model_config.target, axis=1)
    output_df = raw_training_data[config.model_config.target]
    current_predictions = make_prediction(input_data=input_df)

    # the older model has these variable names reversed
    input_df.rename(
        columns={
            "FirstFlrSF": "1stFlrSF",
            "SecondFlrSF": "2ndFlrSF",
            "ThreeSsnPortch": "3SsnPorch",
        },
        inplace=True,
    )
    alternative_predictions = alt_make_prediction(input_data=input_df)

    # When
    current_mse = mean_squared_error(
        y_true=output_df.values, y_pred=current_predictions["predictions"]
    )

    alternative_mse = mean_squared_error(
        y_true=output_df.values, y_pred=alternative_predictions["predictions"]
    )

    # Then
    assert current_mse < alternative_mse
