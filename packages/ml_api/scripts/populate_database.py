from gradient_boosting_model.processing.data_management import load_dataset
from gradient_boosting_model.config.core import config
import requests
import pandas as pd

from random import randint
from itertools import islice
import json
import os
import typing as t
import time


LOCAL_URL = f'http://{os.getenv("DB_HOST", "localhost")}:5000'

HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

LOT_AREA_MAP = {"min": 1470, "max": 56600}

FIRST_FLR_SF_MAP = {"min": 407, "max": 5095}

SECOND_FLR_SF_MAP = {"min": 0, "max": 1862}


def _generate_random_int(value: int, value_ranges: t.Mapping) -> int:
    """Generate random integer within a min and max range."""
    random_value = randint(value_ranges["min"], value_ranges["max"])

    return int(random_value)


def _prepare_inputs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepare input data by removing key rows with NA values."""
    clean_inputs_df = dataframe.dropna(
        subset=config.model_config.features + ["KitchenQual", "LotFrontage"]
    ).copy()

    clean_inputs_df.loc[:, "FirstFlrSF"] = clean_inputs_df["FirstFlrSF"].apply(
        _generate_random_int, value_ranges=FIRST_FLR_SF_MAP
    )
    clean_inputs_df.loc[:, "SecondFlrSF"] = clean_inputs_df["SecondFlrSF"].apply(
        _generate_random_int, value_ranges=SECOND_FLR_SF_MAP
    )
    clean_inputs_df.loc[:, "LotArea"] = clean_inputs_df["LotArea"].apply(
        _generate_random_int, value_ranges=LOT_AREA_MAP
    )

    return clean_inputs_df


def populate_database(n_predictions: int = 500) -> None:
    """
    Manipulate the test data to generate random
    predictions and save them to the database.
    Before running this script, ensure that the
    API and Database docker containers are running.
    """

    print(f"Preparing to generate: {n_predictions} predictions.")

    # Load the gradient boosting test dataset which
    # is included in the model package
    test_inputs_df = load_dataset(file_name="test.csv")
    clean_inputs_df = _prepare_inputs(dataframe=test_inputs_df)
    if len(clean_inputs_df) < n_predictions:
        print(
            f"If you want {n_predictions} predictions, you need to"
            "extend the script to handle more predictions."
        )

    for index, data in clean_inputs_df.iterrows():
        if index > n_predictions:
            break

        response = requests.post(
            f"{LOCAL_URL}/v1/predictions/regression",
            headers=HEADERS,
            json=[data.to_dict()],
        )
        response.raise_for_status()

        if index % 50 == 0:
            print(f"{index} predictions complete")

            # prevent overloading the server
            time.sleep(0.5)

    print("Prediction generation complete.")


if __name__ == "__main__":
    populate_database(n_predictions=500)
