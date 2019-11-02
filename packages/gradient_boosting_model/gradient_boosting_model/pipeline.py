from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from feature_engine.categorical_encoders import RareLabelCategoricalEncoder

from gradient_boosting_model.processing import preprocessors as pp
from gradient_boosting_model.config.core import config

import logging


_logger = logging.getLogger(__name__)


price_pipe = Pipeline(
    [
        (
            "numerical_imputer",
            pp.SklearnTransformerWrapper(
                variables=config['numerical_vars'].data,
                transformer=SimpleImputer(strategy="most_frequent"),
            ),
        ),
        (
            "categorical_inputer",
            pp.SklearnTransformerWrapper(
                variables=config['categorical_vars'].data,
                transformer=SimpleImputer(strategy="constant", fill_value="missing"),
            ),
        ),
        (
            "temporal_variable",
            pp.TemporalVariableEstimator(
                variables=config['temporal_vars'].data,
                reference_variable=config['drop_features'].data
            ),
        ),
        (
            "rare_label_encoder",
            RareLabelCategoricalEncoder(
                tol=0.01,
                n_categories=5,
                variables=config['categorical_vars'].data
            ),
        ),
        (
            "categorical_encoder",
            pp.SklearnTransformerWrapper(
                variables=config['categorical_vars'].data,
                transformer=OrdinalEncoder()
            ),
        ),
        (
            "drop_features",
            pp.DropUnecessaryFeatures(
                variables_to_drop=config['drop_features'].data),
        ),
        ("gb_model", GradientBoostingRegressor(random_state=0, n_estimators=50)),
    ]
)
