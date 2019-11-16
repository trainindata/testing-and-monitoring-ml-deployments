import math

from gradient_boosting_model.predict import make_prediction
from gradient_boosting_model.processing.data_management import load_dataset
from gradient_boosting_model.config.core import config


def test_predict():
    # Given
    training_data = load_dataset(file_name=config['training_data_file'].data)
    test_inputs = training_data.drop(labels='SalePrice', axis='columns')

    # When
    subject = make_prediction(input_data=test_inputs)

    # Then
    assert subject is not None
    assert isinstance(subject.get('predictions')[0], float)
