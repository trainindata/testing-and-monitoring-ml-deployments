import json
import logging
import threading

from flask import request, jsonify, Response, current_app
from gradient_boosting_model.predict import make_prediction as make_secondary_prediction

from api.persistence.data_access import PredictionPersistence, ModelType


def health():
    if request.method == "GET":
        current_app.logger.info('health endpoint')
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

        current_app.logger.debug(f'PREDICTION: '
                                 f'model version: {result.model_version} '
                                 f'Inputs: {json_data} '
                                 f'Predictions: {result.predictions}')

        # Step 2b: Get and save shadow predictions asynchronously
        if current_app.config.get("SHADOW_MODE_ACTIVE"):
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
            return Response(json.dumps(result.errors), status=400)

        # Step 4: Prepare prediction response
        return jsonify(
            {
                "predictions": result.predictions,
                "version": result.model_version,
                "errors": result.errors,
            }
        )


def predict_secondary():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_secondary_prediction(input_data=json_data)

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
