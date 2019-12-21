import enum
import json
import logging
import typing as t

import numpy as np
import pandas as pd
from gradient_boosting_model.predict import make_prediction as make_shadow_prediction
from regression_model.predict import make_prediction as make_live_prediction
from sqlalchemy.orm.session import Session

from api.persistence.models import (
    LassoModelPredictions,
    GradientBoostingModelPredictions,
)

SECONDARY_VARIABLES_TO_RENAME = {
    "FirstFlrSF": "1stFlrSF",
    "SecondFlrSF": "2ndFlrSF",
    "ThreeSsnPortch": "3SsnPorch",
}

_logger = logging.getLogger(__name__)


class ModelType(enum.Enum):
    LASSO = "lasso"
    GRADIENT_BOOSTING = "gradient_boosting"


class PredictionResult(t.NamedTuple):
    errors: t.Any
    predictions: np.array
    model_version: str


MODEL_PREDICTION_MAP = {
    ModelType.GRADIENT_BOOSTING: make_shadow_prediction,
    ModelType.LASSO: make_live_prediction,
}


class PredictionPersistence:
    def __init__(self, *, db_session: Session, user_id: str = None) -> None:
        self.db_session = db_session
        if not user_id:
            # in reality, here we would use something like a UUID for anonymous users
            # and if we had user logins, we would record the user ID.
            self.user_id = "007"

    def make_save_predictions(
        self, *, db_model: ModelType, input_data: t.List
    ) -> PredictionResult:
        """Get the prediction from a given model and persist it."""
        # Access the model prediction function via mapping
        if db_model == ModelType.LASSO:
            # we have to rename a few of the columns for backwards
            # compatibility with the regression model package.
            live_frame = pd.DataFrame(input_data)
            input_data = live_frame.rename(
                columns=SECONDARY_VARIABLES_TO_RENAME
            ).to_dict(orient="records")

        result = MODEL_PREDICTION_MAP[db_model](input_data=input_data)
        errors = None
        try:
            errors = result["errors"]
        except KeyError:
            # regression model `make_prediction` does not include errors
            pass

        prediction_result = PredictionResult(
            errors=errors,
            predictions=result.get("predictions").tolist() if not errors else None,
            model_version=result.get("version"),
        )

        if prediction_result.errors:
            return prediction_result

        self.save_predictions(
            inputs=input_data, prediction_result=prediction_result, db_model=db_model
        )

        return prediction_result

    def save_predictions(
        self,
        *,
        inputs: t.List,
        prediction_result: PredictionResult,
        db_model: ModelType,
    ) -> None:
        """Persist model predictions to storage."""
        if db_model == db_model.LASSO:
            prediction_data = LassoModelPredictions(
                user_id=self.user_id,
                model_version=prediction_result.model_version,
                inputs=json.dumps(inputs),
                outputs=json.dumps(prediction_result.predictions),
            )
        else:
            prediction_data = GradientBoostingModelPredictions(
                user_id=self.user_id,
                model_version=prediction_result.model_version,
                inputs=json.dumps(inputs),
                outputs=json.dumps(prediction_result.predictions),
            )

        self.db_session.add(prediction_data)
        self.db_session.commit()
        _logger.debug(f"saved data for model: {db_model}")
