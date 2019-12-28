from gradient_boosting_model.processing.data_management import load_dataset
import requests

from random import randint
from itertools import islice
import json
import os
import typing as t


LOT_AREA_MAP = {
    "min": 1470,
    "max": 56600
}

FIRST_FLR_SF_MAP = {
    "min": 407,
    "max": 5095
}

SECOND_FLR_SF_MAP = {
    "min": 0,
    "max": 1862
}


def _generate_random_int(value: int, value_ranges: t.Mapping) -> int:
    random_value = randint(
        value_ranges['min'], value_ranges['max'])

    return random_value



def populate_database(n_predictions: int = 1000) -> None:
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
    test_inputs_df['FirstFlrSF'] = test_inputs_df['FirstFlrSF'].apply(
        _generate_random_int, value_ranges=FIRST_FLR_SF_MAP)
    test_inputs_df['SecondFlrSF'] = test_inputs_df['SecondFlrSF'].apply(
        _generate_random_int, value_ranges=SECOND_FLR_SF_MAP)
    test_inputs_df['LotArea'] = test_inputs_df['LotArea'].apply(
        _generate_random_int, value_ranges=LOT_AREA_MAP)

    print(test_inputs_df.head())
    local_url = f'http://{os.environ["DB_HOST"]}:5000'

    # iterrows and unpacking
    for index in range(n_predictions):
        requests.post(f'{local_url}/v1/primary', data=test_inputs_df.iloc[index].to_json())


if __name__ == "__main__":
    populate_database(n_predictions=100)