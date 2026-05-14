import pybreaker
import random

# 1. Khởi tạo Circuit Breaker
# fail_max=5: Sau 5 lần lỗi liên tiếp, mạch sẽ "Mở" (Ngắt kết nối)
# reset_timeout=30: Sau 30 giây mạch sẽ chuyển sang "Half-open" để thử kết nối lại
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5, 
    reset_timeout=30
)

@db_breaker
def fetch_external_data():
    """
    Hàm giả lập việc gọi một API bên ngoài hoặc truy vấn Database.
    Chúng ta dùng random để mô phỏng sự không ổn định của môi trường Production.
    """
    # Mô phỏng tỷ lệ lỗi 30%
    if random.random() > 0.7:
        print("--- Lỗi hệ thống phát sinh! ---")
        raise Exception("Kết nối tới dịch vụ bên ngoài bị lỗi!")
        
    return {"status": "success", "data": "Dữ liệu quan trọng từ Production Database"}

def get_data_with_fallback():
    """
    Hàm bọc (Wrapper) có cơ chế dự phòng (Fallback).
    Đây là hàm mà file app.py sẽ gọi.
    """
    try:
        # Thực hiện gọi hàm thông qua Circuit Breaker
        return fetch_external_data()
        
    except pybreaker.CircuitOpenError:
        # Trường hợp mạch đang ngắt (Open) để bảo vệ hệ thống
        return {
            "status": "circuit_open",
            "message": "Hệ thống đang tạm ngắt kết nối để tự bảo vệ. Vui lòng quay lại sau 30s.",
            "fallback_data": "Dữ liệu cũ lưu trong Cache"
        }
        
    except Exception as e:
        # Trường hợp lỗi phát sinh nhưng mạch chưa ngắt
        return {
            "status": "error",
            "message": f"Phát hiện lỗi: {str(e)}",
            "fallback_data": "Dữ liệu mặc định (Default)"
        }