import json


def test_health_endpoint(client):
    # When
    response = client.get('/')

    # Then
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'ok'}


def test_prediction_endpoint(client):
    # Given

    # When
    response = client.post('/v1/predictions')

    # Then
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'ok'}