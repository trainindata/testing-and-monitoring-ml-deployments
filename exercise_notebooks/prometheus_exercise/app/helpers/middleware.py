from flask import request, Flask
from flask.wrappers import Response
from prometheus_client import Counter, Histogram
import time


# Counter and Histogram are examples of default metrics
# available from the prometheus Python client.
REQUEST_COUNT = Counter(
    name='http_request_count',
    documentation='App Request Count',
    labelnames=['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    name='http_request_latency_seconds',
    documentation='Request latency',
    labelnames=['app_name', 'endpoint']
)


def start_timer() -> None:
    """Get start time of a request."""
    request._prometheus_metrics_request_start_time = time.time()


def stop_timer(response: Response) -> Response:
    """Get stop time of a request.."""
    request_latency = time.time() - request._prometheus_metrics_request_start_time
    REQUEST_LATENCY.labels(
        app_name='webapp',
        endpoint=request.path).observe(request_latency)
    return response


def record_request_data(response: Response) -> Response:
    """Capture request data.

    Uses the flask request object to extract information such as
    the HTTP request method, endpoint and HTTP status.
    """
    REQUEST_COUNT.labels(
        app_name='webapp',
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code).inc()
    return response


def setup_metrics(app: Flask) -> None:
    """Setup Prometheus metrics.

    This function uses the flask before_request
    and after_request hooks to capture metrics
    with each HTTP request to the application.
    """
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
