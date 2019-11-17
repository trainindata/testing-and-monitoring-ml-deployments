from gradient_boosting_model import pipeline
from gradient_boosting_model.config.core import config


def test_pipeline_drops_unnecessary_features(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs
    assert config.model_config.drop_features in X_train.columns

    # When
    # We use the scikit-learn Pipeline private method `_fit` which is called
    # by the `fit` method, since this allows us to access the transformed
    # dataframe. For other models we could use the `transform` method, but
    # the GradientBoostingRegressor does not have a `transform` method.
    X_transformed, _ = pipeline.price_pipe._fit(X_train, y_train)

    # Then
    assert config.model_config.drop_features in X_train.columns
    assert config.model_config.drop_features not in X_transformed.columns


def test_pipeline_transforms_temporal_features(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs

    # When
    # We use the scikit-learn Pipeline private method `_fit` which is called
    # by the `fit` method, since this allows us to access the transformed
    # dataframe. For other models we could use the `transform` method, but
    # the GradientBoostingRegressor does not have a `transform` method.
    X_transformed, _ = pipeline.price_pipe._fit(X_train, y_train)

    # Then
    assert (
            X_transformed.iloc[0]["YearRemodAdd"]
            == X_train.iloc[0]["YrSold"] - X_train.iloc[0]["YearRemodAdd"]
    )
