import json

from flask import request, jsonify, Response, current_app
from gradient_boosting_model.predict import make_prediction
from regression_model.predict import make_prediction as make_regression_prediction

from api.persistence.data_access import PredictionPersistence, ModelType


def health():
    if request.method == "GET":
        return jsonify({"status": "ok"})


def predict():
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

        # Step 5: Save predictions
        persistence = PredictionPersistence(db_session=current_app.db_session)
        persistence.save_predictions(
            inputs=json_data,
            model_version=version,
            predictions=predictions,
            db_model=ModelType.GRADIENT_BOOSTING,
        )

        # Step 6: Prepare prediction response
        return jsonify(
            {"predictions": predictions, "version": version, "errors": errors}
        )


def predict_previous():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_regression_prediction(input_data=json_data)

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
