import json

import pytest
from gradient_boosting_model.processing.data_management import load_dataset

from tests.test_api import SECONDARY_VARIABLES_TO_RENAME
from .compare import compare_differences


@pytest.mark.differential
def test_model_prediction_differentials(client):
    test_inputs_df = load_dataset(file_name="test.csv")
    secondary_test_inputs_df = test_inputs_df.rename(
        columns=SECONDARY_VARIABLES_TO_RENAME)

    primary_response = client.post('v1/predictions/primary',
                           json=test_inputs_df.to_dict(orient="records"))
    primary_predictions = json.loads(primary_response.data)['predictions']

    secondary_response = client.post('v1/predictions/secondary',
                           json=secondary_test_inputs_df.to_dict(orient="records"))
    secondary_predictions = json.loads(secondary_response.data)['predictions']

    compare_differences(
        expected_predictions=secondary_predictions[:10],
        actual_predictions=primary_predictions[:10],
        rel_tol=0.2,
    )
