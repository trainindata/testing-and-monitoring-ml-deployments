import json

import numpy as np
import pytest
from gradient_boosting_model.processing.data_management import load_dataset


@pytest.mark.integration
def test_health_endpoint(client):
    # When
    response = client.get("/")

    # Then
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "ok"}


@pytest.mark.integration
def test_prediction_endpoint(client):
    # Given
    # Load the test dataset which is included in the model package
    test_inputs_df = load_dataset(file_name="test.csv")  # dataframe
    input_length = len(test_inputs_df)  # test csv contains 1459 rows
    expected_output_length = input_length - 2  # we expect 2 rows to be filtered

    # When
    response = client.post(
        "/v1/predictions", json=test_inputs_df.to_dict(orient="records")
    )

    # Then
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["errors"] is None
    assert len(data["predictions"]) == expected_output_length


# parameterizationa allows us to try many combinations of data
# within the same test, see the pytest docs for details:
# https://docs.pytest.org/en/latest/parametrize.html
@pytest.mark.parametrize(
    "field, field_value, index, expected_error",
    (
        (
            "BldgType",
            1,  # expected str
            33,
            {"33": {"BldgType": ["Not a valid string."]}},
        ),
        (
            "GarageArea",  # model feature
            "abc",  # expected float
            45,
            {"45": {"GarageArea": ["Not a valid number."]}},
        ),
        (
            "CentralAir",
            np.nan,  # nan not allowed
            34,
            {"34": {"CentralAir": ["Field may not be null."]}},
        ),
        ("LotArea", "", 2, {"2": {"LotArea": ["Not a valid integer."]}},),
    ),
)
@pytest.mark.integration
def test_prediction_validation(field, field_value, index, expected_error, client):
    # Given
    # Load the test dataset which is included in the model package
    test_inputs_df = load_dataset(file_name="test.csv")  # dataframe

    # Check gradient_boosting_model.processing.validation import HouseDataInputSchema
    # and you will see the expected values for the inputs to the house price prediction
    # model. In this test, inputs are changed to incorrect values to check the validation.
    test_inputs_df.loc[index, field] = field_value

    # When
    response = client.post(
        "/v1/predictions", json=test_inputs_df.to_dict(orient="records")
    )

    # Then
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == expected_error
