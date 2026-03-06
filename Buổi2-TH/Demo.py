from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake database
books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"},
    {"id": 3, "title": "Cho toi xin mot ve di tuoi tho", "author": "Nguyen Nhat Anh"}
]

# Fake token
VALID_TOKEN = "123456"


# API lấy danh sách sách (cần token)
@app.route("/books", methods=["GET"])
def get_books():

    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(books)


# API lấy sách theo id
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):

    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    for book in books:
        if book["id"] == id:
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)