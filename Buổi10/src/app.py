import sys
import os
# Thêm đường dẫn để Python tìm thấy các module trong src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from middlewares.observability import setup_observability, logger
from services.data_service import get_data_with_fallback

app = Flask(__name__)

# 1. Thiết lập Security: Rate Limiting (Chặn Spam/DDoS)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://",
)

# 2. Kích hoạt hệ thống Quan sát (Observability)
setup_observability(app)

@app.route('/api/ping')
@limiter.limit("3 per 10 seconds") # Thực hành Rate Limit
def ping():
    return {"message": "Pong! API đang hoạt động ổn định."}

@app.route('/api/unstable')
def unstable():
    # Thực hành Circuit Breaker
    return get_data_with_fallback()

@app.route('/metrics')
def metrics():
    # Endpoint dành cho hệ thống Monitoring (Prometheus)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    # Tạo thư mục log nếu chưa có
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logger.info("🚀 Production API khởi động thành công trên cổng 5000")
    app.run(host='0.0.0.0', port=5000)