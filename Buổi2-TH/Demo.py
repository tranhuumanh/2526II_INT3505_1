from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# =========================
# Fake Database (Data Layer)
# =========================

books_db = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"},
    {"id": 3, "title": "Cho toi xin mot ve di tuoi tho", "author": "Nguyen Nhat Anh"}
]

VALID_TOKEN = "123456"


# =========================
# Service Layer
# =========================

def get_all_books():
    return books_db


def get_book_by_id(book_id):
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None


# =========================
# API Layer (Controller)
# =========================

# Client-Server
@app.route("/")
def home():
    return {"message": "Library REST API running"}


# Stateless + Uniform Interface
@app.route("/books", methods=["GET"])
def get_books():

    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    books = get_all_books()

    # Cacheable
    response = make_response(jsonify(books))
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):

    token = request.headers.get("Authorization")

    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    book = get_book_by_id(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    response = make_response(jsonify(book))
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


# Code on Demand
@app.route("/script")
def send_script():

    js_code = """
    console.log("Hello from Library REST API");
    alert("Code on Demand example");
    """

    response = make_response(js_code)
    response.headers["Content-Type"] = "application/javascript"

    return response


# =========================

if __name__ == "__main__":
    app.run(debug=True)