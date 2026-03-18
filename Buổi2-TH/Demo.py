import jwt
import datetime
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)


app.config['SECRET_KEY'] = 'KTHDV_2026'

# Dữ liệu giả lập
books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"},
]

# --- 1. MIDDLEWARE: KIỂM TRA BEARER TOKEN ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Lấy giá trị từ Header 'Authorization'
        auth_header = request.headers.get('Authorization')
        token = None

        # Kiểm tra định dạng: Bearer <token>
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            # Giải mã token bằng Secret Key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Lưu user_id vào request để các hàm bên dưới có thể sử dụng
            request.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    
    return decorated

# --- 2. API ĐĂNG NHẬP (TẠO TOKEN) ---
@app.route('/login', methods=['POST'])
def login():
    # Tạo Payload (Nội dung bên trong token)    
    payload = {
        'user_id': 99,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # Hết hạn sau 30p
    }
    # Ký tên và tạo chuỗi JWT
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'access_token': token})

# --- 3. CÁC API BẢO MẬT ---
@app.route("/books", methods=["GET"])
@token_required # Chỉ ai có token hợp lệ mới vào được đây
def get_books():
    return jsonify({
        "data": books,
        "request_by_user_id": request.user_id
    })

if __name__ == "__main__":
    app.run(debug=True)