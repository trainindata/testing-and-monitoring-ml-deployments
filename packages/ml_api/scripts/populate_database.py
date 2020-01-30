import argparse
import os
import time
import typing as t
from random import randint

import pandas as pd
import requests
from gradient_boosting_model.config.core import config
from gradient_boosting_model.processing.data_management import load_dataset

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


def populate_database(n_predictions: int = 500, anomaly: bool = False) -> None:
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

    if anomaly:
        # set extremely low values to generate an outlier
        n_predictions = 1
        clean_inputs_df.loc[:, "FirstFlrSF"] = 1
        clean_inputs_df.loc[:, "LotArea"] = 1
        clean_inputs_df.loc[:, "OverallQual"] = 1
        clean_inputs_df.loc[:, "GrLivArea"] = 1

    for index, data in clean_inputs_df.iterrows():
        if index > n_predictions:
            if anomaly:
                print('Created 1 anomaly')
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
    anomaly = False
    parser = argparse.ArgumentParser(
        description='Send random requests to House Price API.')
    parser.add_argument('--anomaly', help="generate unusual inputs")
    args = parser.parse_args()
    if args.anomaly:
        print("Generating unusual inputs")
        anomaly = True

    populate_database(n_predictions=500, anomaly=anomaly)
