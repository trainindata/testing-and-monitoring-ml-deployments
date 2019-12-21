from unittest import mock
import pytest

from api.persistence.data_access import PredictionPersistence, ModelType

from api.persistence.models import (
    GradientBoostingModelPredictions,
    LassoModelPredictions,
)


# parameterizationa allows us to try many combinations of data
# within the same test, see the pytest docs for details:
# https://docs.pytest.org/en/latest/parametrize.html
@pytest.mark.parametrize(
    "model_type, model,",
    (
        (ModelType.GRADIENT_BOOSTING, GradientBoostingModelPredictions),
        (ModelType.LASSO, LassoModelPredictions),
    ),
)
def test_data_access(model_type, model, test_inputs_df):
    # Given
    # We mock the database session
    mock_session = mock.MagicMock()
    _persistence = PredictionPersistence(db_session=mock_session)

    # When
    _persistence.make_save_predictions(
        db_model=model_type, input_data=test_inputs_df.to_dict(orient="records")
    )

    # Then
    assert mock_session.commit.call_count == 1
    assert mock_session.add.call_count == 1
    assert isinstance(mock_session.add.call_args[0][0], model)
