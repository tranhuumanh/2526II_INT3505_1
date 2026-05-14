import logging
import time
from flask import request
from prometheus_client import Counter, Histogram

# 1. Cấu hình Logging (Winston-like)
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    handlers=[
        logging.FileHandler("logs/audit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 2. Cấu hình Metrics (Prometheus)
REQUEST_COUNT = Counter(
    'api_requests_total', 'Tổng số requests',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds', 'Thời gian phản hồi',
    ['endpoint']
)

def setup_observability(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_and_metrics(response):
        # Tính toán Latency (Tracing cơ bản)
        latency = time.time() - request.start_time
        
        # Ghi Log cho mọi request (Audit Log)
        logger.info(f"{request.method} {request.path} {response.status_code} {latency:.4f}s")
        
        # Cập nhật Metrics
        REQUEST_COUNT.labels(
            method=request.method, 
            endpoint=request.path, 
            http_status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        
        return response