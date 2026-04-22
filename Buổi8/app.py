from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu giả lập danh mục sách trong thư viện
books = [
    {"id": 1, "title": "Dế Mèn Phiêu Lưu Ký", "author": "Tô Hoài", "available": True},
    {"id": 2, "title": "Số Đỏ", "author": "Vũ Trọng Phụng", "available": False}
]

# 1. GET: Lấy danh sách toàn bộ sách (Integration Test)
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books}), 200

# 2. GET: Tìm một cuốn sách theo ID (Validation Test)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Không tìm thấy sách"}), 404

# 3. POST: Thêm sách mới vào thư viện (Functional Test)
@app.route('/books', methods=['POST'])
def add_book():
    # Kiểm tra dữ liệu đầu vào và Header Content-Type: application/json
    data = request.get_json(silent=True)
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({"error": "Dữ liệu không hợp lệ. Cần có title và author"}), 400
    
    new_book = {
        "id": books[-1]['id'] + 1 if books else 1,
        "title": data['title'],
        "author": data['author'],
        "available": data.get('available', True)
    }
    books.append(new_book)
    return jsonify(new_book), 201

# 4. PUT: Cập nhật thông tin sách hoặc trạng thái mượn
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Không tìm thấy sách để cập nhật"}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Thiếu dữ liệu cập nhật"}), 400

    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    book['available'] = data.get('available', book['available'])
    
    return jsonify(book), 200

# 5. DELETE: Xóa sách khỏi hệ thống
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_length = len(books)
    books = [b for b in books if b['id'] != book_id]
    
    if len(books) < initial_length:
        return jsonify({"message": "Xóa sách thành công", "result": True}), 200
    return jsonify({"error": "Không tìm thấy sách để xóa"}), 404

if __name__ == '__main__':
    # Chạy server tại port 5000
    app.run(debug=True, port=5000)