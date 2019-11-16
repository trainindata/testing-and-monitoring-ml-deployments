from sklearn.model_selection import train_test_split

from gradient_boosting_model import pipeline
from gradient_boosting_model.processing.data_management import (
    load_dataset,
    save_pipeline,
)
from gradient_boosting_model.config.core import config
from gradient_boosting_model import __version__ as _version

import logging


_logger = logging.getLogger(__name__)


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config['training_data_file'])

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config['features'].data],
        data[config['target'].data],
        test_size=0.1,
        random_state=0,  # we are setting the seed here
    )

    pipeline.price_pipe.fit(X_train, y_train)

    _logger.warning(f"saving model version: {_version}")
    save_pipeline(pipeline_to_persist=pipeline.price_pipe)


if __name__ == "__main__":
    run_training()