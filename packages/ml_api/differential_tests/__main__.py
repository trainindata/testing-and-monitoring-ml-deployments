import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Mapping

from differential_tests.compare import compare_predictions
from api.config import ROOT

from termcolor import cprint
from yarl import URL
import requests

Marginals = Mapping[str, Mapping[str, float]]


def parse_args() -> Namespace:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    compute_parser = subparsers.add_parser(
        "compute", help="Compute the predictions for a test set"
    )
    compute_parser.add_argument(
        "--base-url",
        default=URL("http://0.0.0.0:5000"),
        type=URL,
        help="Base URL of the service to test",
    )
    compute_parser.add_argument(
        "tests_dir", type=Path, help="Directory containing the test set to use"
    )
    compute_parser.add_argument(
        "results_dir", type=Path, help="Directory to save the prediction results to"
    )

    compare_parser = subparsers.add_parser(
        "compare", help="Compare the actual results with the expected results"
    )
    compare_parser.add_argument(
        "--absolute-tolerance",
        dest="abs_tol",
        metavar="X",
        type=float,
        help="math.isclose(a, b, abs_tol=X)",
        default=1e-5,
    )
    compare_parser.add_argument(
        "--relative-tolerance",
        dest="rel_tol",
        metavar="X",
        type=float,
        default=1e-5,
        help="math.isclose(a, b, rel_tol=X)",
    )
    compare_parser.add_argument(
        "expected_results_dir",
        type=Path,
        help="Directory containing the expected results",
    )
    compare_parser.add_argument(
        "actual_results_dir", type=Path, help="Directory containing the actual results"
    )

    return parser.parse_args()


def main(args: Namespace) -> None:
    if args.command == "compute":
        compute_predictions(args)
    elif args.command == "compare":
        compare_predictions(args)


def compute_predictions(args: Namespace) -> None:
    print("computing")

    diff_test_dir = ROOT / "differential_tests"
    results_dir = args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    prepared_test_dir = diff_test_dir / Path(args.tests_dir)

    for test_filename in sorted(prepared_test_dir.glob("*.json")):
        results_filename = results_dir / test_filename.name
        print(f"Computing {results_filename} from {test_filename} ... ", end="")

        with test_filename.open() as f:
            test = json.load(f)

        results = requests.post(f"{args.base_url}/v1/predictions/primary", json=test)

        with results_filename.open("w") as f:
            json.dump(results.json(), f, indent=2, sort_keys=True)

        cprint("OK", "green")


if __name__ == "__main__":
    args = parse_args()
    main(args)
