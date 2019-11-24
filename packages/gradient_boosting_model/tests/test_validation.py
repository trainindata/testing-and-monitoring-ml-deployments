from gradient_boosting_model.processing.validation import validate_inputs
from gradient_boosting_model.processing.data_management import load_dataset


def test_validate_inputs():
    # Given
    test_inputs = load_dataset(file_name="test.csv")

    # When
    validated_inputs, errors = validate_inputs(input_data=test_inputs)

    # Then
    # we expect that 2 rows are removed due to missing vars
    assert len(test_inputs) == 1459
    assert len(validated_inputs) == 1457


def test_validate_inputs_identifies_errors():
    # Given
    test_inputs = load_dataset(file_name="test.csv")

    # introduce errors
    test_inputs.at[1, "BldgType"] = 50  # we expect a string

    # When
    validated_inputs, errors = validate_inputs(input_data=test_inputs)

    # Then
    assert errors
    assert errors[1] == {"BldgType": ["Not a valid string."]}
