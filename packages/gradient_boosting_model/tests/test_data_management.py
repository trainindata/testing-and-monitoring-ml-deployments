from gradient_boosting_model.train_pipeline import run_training
from gradient_boosting_model.processing.data_management import load_pipeline
from gradient_boosting_model.config.core import config
from gradient_boosting_model import __version__ as _version

from sklearn.pipeline import Pipeline
from skl2onnx import convert_sklearn, supported_converters


def test_can_load_onnx_format():
    # Given
    from skl2onnx.common.data_types import onnx_built_with_ml

    deps_in_place = onnx_built_with_ml()

    pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.onnx"
    print(f'supported converters: {supported_converters()}')
    run_training()


    # When
    pipe = load_pipeline(file_name=pipeline_file_name)

    # Then
    assert isinstance(pipe, Pipeline)