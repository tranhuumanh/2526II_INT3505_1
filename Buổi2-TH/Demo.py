<<<<<<< Updated upstream
from flask import Flask, jsonify, request

app = Flask(__name__)

=======
import jwt
import datetime
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)


app.config['SECRET_KEY'] = 'KTHDV_2026'

>>>>>>> Stashed changes
# Fake database
books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"},
]

# --- 1. MIDDLEWARE: KIỂM TRA BEARER TOKEN ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        # Kiểm tra xem có header Authorization và bắt đầu bằng "Bearer " không
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            # Giải mã và xác thực token với Secret Key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Bạn có thể lưu thông tin user vào request context nếu cần
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
    # Giả định user/pass đã đúng sau khi kiểm tra Database
    # Chúng ta tạo Token chứa ID người dùng và thời gian hết hạn
    payload = {
        'user_id': 99,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'access_token': token})

# --- 3. CÁC API CẦN BẢO VỆ ---

<<<<<<< Updated upstream
# API lấy danh sách sách (cần token)
=======
>>>>>>> Stashed changes
@app.route("/books", methods=["GET"])
@token_required
def get_books():
    return jsonify({
        "data": books,
        "request_by_user_id": request.user_id # Lấy từ token đã decode
    })

<<<<<<< Updated upstream
    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(books)


# API lấy sách theo id
=======
>>>>>>> Stashed changes
@app.route("/books/<int:id>", methods=["GET"])
@token_required
def get_book(id):
<<<<<<< Updated upstream

    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    for book in books:
        if book["id"] == id:
            return jsonify(book)

=======
    book = next((b for b in books if b["id"] == id), None)
    if book:
        return jsonify(book)
>>>>>>> Stashed changes
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)