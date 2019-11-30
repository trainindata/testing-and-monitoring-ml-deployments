from flask import request, jsonify
from gradient_boosting_model.predict import make_prediction


def health():
    if request.method == 'GET':
        return jsonify({'status': 'ok'})


def version():
    if request.method == 'GET':
        return jsonify({'api_version': 'ok'})


def predict():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_prediction(input_data=json_data)

        # Step 3: Split out results
        predictions = result.get('predictions').tolist()
        version = result.get('version')
        errors = result.get('errors')

        # Step 4: Return the response as JSON
        return jsonify({'predictions': predictions,
                        'version': version,
                        'errors': errors})