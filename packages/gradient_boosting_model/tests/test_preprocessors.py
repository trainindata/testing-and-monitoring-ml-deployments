from gradient_boosting_model.config.core import config
from gradient_boosting_model.processing import preprocessors as pp


def test_drop_unnecessary_features_transformer(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs
    assert config.model_config.drop_features in X_train.columns

    transformer = pp.DropUnecessaryFeatures(
        variables_to_drop=config.model_config.drop_features,
    )

    # When
    X_transformed = transformer.transform(X_train)

    # Then
    assert config.model_config.drop_features not in X_transformed.columns


def test_temporal_variable_estimator(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs

    transformer = pp.TemporalVariableEstimator(
        variables=config.model_config.temporal_vars,
        reference_variable=config.model_config.drop_features,
    )

    # When
    X_transformed = transformer.transform(X_train)

    # Then
    assert (
        X_transformed.iloc[0]["YearRemodAdd"]
        == X_train.iloc[0]["YrSold"] - X_train.iloc[0]["YearRemodAdd"]
    )
