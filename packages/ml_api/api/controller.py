import json
import logging
import threading

from flask import request, jsonify, Response, current_app

from gradient_boosting_model import __version__ as shadow_version
from regression_model import __version__ as live_version
from prometheus_client import Histogram, Gauge, Info
from gradient_boosting_model.predict import make_prediction
from api.persistence.data_access import PredictionPersistence, ModelType
from api.config import APP_NAME


_logger = logging.getLogger(__name__)

PREDICTION_TRACKER = Histogram(
    name='house_price_prediction_dollars',
    documentation='ML Model Prediction on House Price',
    labelnames=['app_name', 'model_name', 'model_version']
)

PREDICTION_GAUGE = Gauge(
    name='house_price_gauge_dollars',
    documentation='ML Model Prediction on House Price for min max calcs',
    labelnames=['app_name', 'model_name', 'model_version']
)

PREDICTION_GAUGE.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version)

MODEL_VERSIONS = Info(
    'model_version_details',
    'Capture model version information',
)

MODEL_VERSIONS.info({
    'live_model': ModelType.LASSO.name,
    'live_version': live_version,
    'shadow_model': ModelType.GRADIENT_BOOSTING.name,
    'shadow_version': shadow_version})


def health():
    if request.method == "GET":
        return jsonify({"status": "ok"})


def predict():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2a: Get and save live model predictions
        persistence = PredictionPersistence(db_session=current_app.db_session)
        result = persistence.make_save_predictions(
            db_model=ModelType.LASSO, input_data=json_data
        )

        # Step 2b: Get and save shadow predictions asynchronously
        if current_app.config.get("SHADOW_MODE_ACTIVE"):
            _logger.debug(
                f"Calling shadow model asynchronously: "
                f"{ModelType.GRADIENT_BOOSTING.value}"
            )
            thread = threading.Thread(
                target=persistence.make_save_predictions,
                kwargs={
                    "db_model": ModelType.GRADIENT_BOOSTING,
                    "input_data": json_data,
                },
            )
            thread.start()

        # Step 3: Handle errors
        if result.errors:
            _logger.warning(f"errors during prediction: {result.errors}")
            return Response(json.dumps(result.errors), status=400)

        # Step 4: Monitoring
        for _prediction in result.predictions:
            PREDICTION_TRACKER.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version).observe(_prediction)
            PREDICTION_GAUGE.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version).set(_prediction)

        # Step 5: Prepare prediction response
        return jsonify(
            {
                "predictions": result.predictions,
                "version": result.model_version,
                "errors": result.errors,
            }
        )


def predict_previous():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_prediction(input_data=json_data)

        # Step 3: Handle errors
        errors = result.get("errors")
        if errors:
            return Response(json.dumps(errors), status=400)

        # Step 4: Split out results
        predictions = result.get("predictions").tolist()
        version = result.get("version")

        # Step 5: Prepare prediction response
        return jsonify(
            {"predictions": predictions, "version": version, "errors": errors}
        )
