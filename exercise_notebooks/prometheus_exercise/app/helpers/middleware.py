from flask import request
from prometheus_client import Counter, Histogram
import time
import sys

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request._prometheus_metrics_request_start_time = time.time()

def stop_timer(response):
    request_latency = time.time() - request._prometheus_metrics_request_start_time
    REQUEST_LATENCY.labels('webapp', request.path).observe(request_latency)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('webapp', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)
