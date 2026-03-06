from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# Fake Database
books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"},
    {"id": 3, "title": "Cho toi xin mot ve di tuoi tho", "author": "Nguyen Nhat Anh"}
]

# Fake token
VALID_TOKEN = "123456"


# API lấy danh sách sách
@app.route("/books", methods=["GET"])
def get_books():

    # Stateless: client phải gửi token
    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    # Cacheable
    response = make_response(jsonify(books))
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


# API lấy sách theo id
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):

    # Stateless
    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    for book in books:
        if book["id"] == id:

            # Cacheable
            response = make_response(jsonify(book))
            response.headers["Cache-Control"] = "public, max-age=60"

            return response

    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)