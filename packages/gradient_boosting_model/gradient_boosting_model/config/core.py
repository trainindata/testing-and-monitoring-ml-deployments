import pathlib
import typing as t

import gradient_boosting_model
from strictyaml import load, Map, Str, Seq, Int, Float
from pydantic import BaseModel, validator

# Key Directories
ROOT = pathlib.Path(gradient_boosting_model.__file__).resolve().parent.parent
PACKAGE_ROOT = pathlib.Path(gradient_boosting_model.__file__).resolve().parent
CONFIG_FILE_PATH = ROOT / "config.yml"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
DATASET_DIR = PACKAGE_ROOT / "datasets"


CONFIG_SCHEMA = Map(
    {"package_name": Str(),
     "training_data_file": Str(),
     "drop_features": Seq(Str()),
     "pipeline_name": Str(),
     "pipeline_save_file": Str(),
     "target": Str(),
     "features": Seq(Str()),
     "numerical_vars": Seq(Str()),
     "categorical_vars": Seq(Str()),
     "temporal_vars": Seq(Str()),
     "numerical_vars_with_na": Seq(Str()),
     'numerical_na_not_allowed': Seq(Str()),
     'random_state': Int(),
     'n_estimators': Int(),
     'rare_label_n_categories': Int(),
     'rare_label_tol': Float(),
     'allowed_loss_functions': Seq(Str()),
     'loss': Str(),
     }
)


class AppConfig(BaseModel):
    """
    Application-level config.
    """
    package_name: str
    pipeline_name: str
    pipeline_save_file: str
    training_data_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    drop_features: t.Sequence[str]
    target: str
    features: t.Sequence[str]
    numerical_vars: t.Sequence[str]
    categorical_vars: t.Sequence[str]
    temporal_vars: t.Sequence[str]
    numerical_vars_with_na: t.Sequence[str]
    numerical_na_not_allowed: t.Sequence[str]
    random_state: int
    n_estimators: int
    rare_label_n_categories: int
    rare_label_tol: float

    # the order is necessary for validation
    allowed_loss_functions: t.Tuple[str, ...]
    loss: str

    @validator('loss')
    def allowed_loss_function(cls, value, values):
        """
        Loss function to be optimized.

        `ls` refers to least squares regression.
        `lad` (least absolute deviation)
        `huber` is a combination of the two.
        `quantile` allows quantile regression.

        Following the research phase, loss is restricted to
        `ls` and `huber` for this model.
        """

        allowed_loss_functions = values.get("allowed_loss_functions")
        if value in allowed_loss_functions:
            return value
        raise ValueError(
            f'the loss parameter specified: {value}, '
            f'is not in the allowed set: {allowed_loss_functions}')


class Config(BaseModel):
    """Master config object."""
    app_config: AppConfig
    model_config: ModelConfig


def find_config_file():
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f'Config not found at {CONFIG_FILE_PATH!r}')


def fetch_config_from_yaml(cfg_path: pathlib.Path = None):
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, 'r') as conf_file:
            cfg_dict = load(
                conf_file.read(), CONFIG_SCHEMA)
            return cfg_dict
    return False


def create_and_validate_config(config_dict: dict = None) -> Config:
    """Run validation on config values."""
    if config_dict is None:
        config_dict = fetch_config_from_yaml()

    # specify the data attribute created by the strictyaml parser
    _config = Config(app_config=AppConfig(**config_dict.data),
                    model_config=ModelConfig(**config_dict.data))

    return _config


config = create_and_validate_config()
