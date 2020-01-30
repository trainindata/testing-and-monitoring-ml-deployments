from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from feature_engine.categorical_encoders import RareLabelCategoricalEncoder

from gradient_boosting_model.processing import preprocessors as pp
from gradient_boosting_model.config.core import config

import logging


_logger = logging.getLogger(__name__)

numeric_features = [
    'LotArea',
    'OverallQual',
    'YearRemodAdd',
    'BsmtFinSF1',
    'TotalBsmtSF',
    'FirstFlrSF',
    'SecondFlrSF',
    'GrLivArea',
    'GarageCars',
    # this one is only to calculate temporal variable:
    'YrSold',
]
#numeric_features = [0, 1, 2, 4, 5, 6, 7, 8, 9]
categorical_features = ['BsmtQual'] # BsmtQual


numeric_transformer = Pipeline(steps=[
    ('numerical_imputer', SimpleImputer(strategy='most_frequent')),
])

categorical_transformer = Pipeline(steps=[
    ('categorical_encoder', OrdinalEncoder()),
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num_input', numeric_transformer, numeric_features),
        ('cat_input', categorical_transformer, categorical_features)
    ])

classifier = GradientBoostingRegressor(
                loss=config.model_config.loss,
                random_state=config.model_config.random_state,
                n_estimators=config.model_config.n_estimators)

price_pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', classifier)
])


# price_pipe = Pipeline(
#     [
#         # SimpleImputer included in sklearn-onnx
#         (
#             "numerical_imputer",
#             pp.SklearnTransformerWrapper(
#                 variables=config.model_config.numerical_vars,
#                 transformer=SimpleImputer(strategy="most_frequent"),
#             ),
#         ),
#         # SimpleImputer included in sklearn-onnx
#         # (
#         #     "categorical_imputer",
#         #     pp.SklearnTransformerWrapper(
#         #         variables=config.model_config.categorical_vars,
#         #         transformer=SimpleImputer(strategy="constant", fill_value="missing"),
#         #     ),
#         # ),
#         # TODO: TemporalVariableEstimator not supported
#         # (
#         #     "temporal_variable",
#         #     pp.TemporalVariableEstimator(
#         #         variables=config.model_config.temporal_vars,
#         #         reference_variable=config.model_config.drop_features,
#         #     ),
#         # ),
#         # TODO: RareLabelCategoricalEncoder not supported
#         # (
#         #     "rare_label_encoder",
#         #     RareLabelCategoricalEncoder(
#         #         tol=config.model_config.rare_label_tol,
#         #         n_categories=config.model_config.rare_label_n_categories,
#         #         variables=config.model_config.categorical_vars,
#         #     ),
#         # ),
#         # OrdinalEncoder is supported
#         (
#             "categorical_encoder",
#             pp.SklearnTransformerWrapper(
#                 variables=config.model_config.categorical_vars,
#                 transformer=OrdinalEncoder(),
#             ),
#         ),
#         # TODO: RareLabelCategoricalEncoder not supported
#         (
#             "drop_features",
#             pp.DropUnecessaryFeatures(
#                 variables_to_drop=config.model_config.drop_features,
#             ),
#         ),
#         # GradientBoostingRegressor is supported
#         (
#             "gb_model",
#             GradientBoostingRegressor(
#                 loss=config.model_config.loss,
#                 random_state=config.model_config.random_state,
#                 n_estimators=config.model_config.n_estimators,
#             ),
#         ),
#     ]
# )
