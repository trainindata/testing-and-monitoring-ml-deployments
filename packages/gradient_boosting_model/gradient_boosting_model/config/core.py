import pathlib

import gradient_boosting_model
from strictyaml import load, Map, Str, Seq


CONFIG_SCHEMA = Map(
    {"package_name": Str(),
     "training_data_file": Str(),
     "drop_features": Str(),
     "pipeline_name": Str(),
     "pipeline_save_file": Str(),
     "target": Str(),
     "features": Seq(Str()),
     "numerical_vars": Seq(Str()),
     "categorical_vars": Seq(Str()),
     "temporal_vars": Seq(Str()),
     "numerical_vars_with_na": Seq(Str()),
     'numerical_na_not_allowed': Seq(Str())
     }
)


# Key Directories
ROOT = pathlib.Path(gradient_boosting_model.__file__).resolve().parent.parent
PACKAGE_ROOT = pathlib.Path(gradient_boosting_model.__file__).resolve().parent
CONFIG_FILE_PATH = ROOT / "config.yml"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
DATASET_DIR = PACKAGE_ROOT / "datasets"


def find_config_file():
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f'Config not found at {CONFIG_FILE_PATH!r}')


def fetch_config_from_yaml():
    """Parse YAML containing the package configuration."""
    cfg_path = find_config_file()
    if cfg_path:
        with open(cfg_path, 'r') as conf_file:
            cfg_dict = load(
                conf_file.read(),
                CONFIG_SCHEMA)
        return cfg_dict
    return False


config = fetch_config_from_yaml()
