import pytest
from sklearn.model_selection import train_test_split

from gradient_boosting_model.config.core import config
from gradient_boosting_model.processing.data_management import load_dataset


@pytest.fixture(scope="module")
def pipeline_inputs():
    # For larger datasets, here we would use a testing sub-sample.
    data = load_dataset(file_name=config.app_config.training_data_file)

    # Divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=0.1,
        # we are setting the random seed here
        # for reproducibility
        random_state=0,
    )

    return X_train, X_test, y_train, y_test
