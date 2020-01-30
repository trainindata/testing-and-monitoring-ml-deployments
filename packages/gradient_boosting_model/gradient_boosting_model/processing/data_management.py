import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from skl2onnx import convert_sklearn, supported_converters
from skl2onnx.common.data_types import FloatTensorType, Int64TensorType, StringTensorType
import onnxruntime as rt

from gradient_boosting_model.config.core import config, DATASET_DIR, TRAINED_MODEL_DIR
from gradient_boosting_model import __version__ as _version

import logging
import typing as t


_logger = logging.getLogger(__name__)


def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(f"{DATASET_DIR}/{file_name}")

    # rename variables beginning with numbers to avoid syntax errors later
    transformed = dataframe.rename(columns=config.model_config.variables_to_rename)
    return transformed


def convert_dataframe_schema(df, drop=None):
    inputs = []
    for k, v in zip(df.columns, df.dtypes):
        if drop is not None and k in drop:
            continue
        if v == "int64":
            t = Int64TensorType([1, 1])
        elif v == "float64":
            t = FloatTensorType([1, 1])
        else:
            t = StringTensorType([1, 1])
        inputs.append((k, t))
    return inputs


def save_pipeline(*, pipeline_to_persist: Pipeline, inputs) -> None:
    """Persist the pipeline.

    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.onnx"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])

    # Convert into ONNX format

    # This is going to need to match features
    # - LotArea - Integer
    # - OverallQual - Integer
    # - YearRemodAdd - Integer
    # - BsmtQual - Str
    # - BsmtFinSF1 - Float
    # - TotalBsmtSF - Float
    # - FirstFlrSF - Integer
    # - SecondFlrSF - Integer
    # - GrLivArea - Integer
    # - GarageCars - Float
    # # this one is only to calculate temporal variable:
    # - YrSold - Integer

    onx = convert_sklearn(pipeline_to_persist, initial_types=inputs)
    with open(save_path, "wb") as f:
        f.write(onx.SerializeToString())

    #joblib.dump(pipeline_to_persist, save_path)
    _logger.info(f"saved pipeline: {save_file_name}")


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    session = rt.InferenceSession(str(file_path))
    input_name = session.get_inputs()[0].name
    return session


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.

    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
