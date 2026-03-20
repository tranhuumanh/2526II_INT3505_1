from flask import Flask, jsonify, request, Response
from flask_swagger_ui import get_swaggerui_blueprint
import os


app = Flask(__name__)

# =========================
# Fake database
# =========================
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "publishedYear": 2008},
    {"id": 2, "title": "Atomic Habits", "author": "James Clear", "publishedYear": 2018}
]

# =========================
# Swagger UI config
# =========================
SWAGGER_URL = '/api-docs'
API_URL = '/swagger/DemoOpenAPI.yaml'   # ✅ sửa đúng tên file của bạn

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Book API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve YAML file
@app.route("/swagger/DemoOpenAPI.yaml")
def swagger_yaml():
    file_path = os.path.join(os.path.dirname(__file__), "DemoOpenAPI.yaml")
    with open(file_path, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype="text/yaml")

# =========================
# API endpoints
# =========================

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    for book in books:
        if book["id"] == id:
            return jsonify(book)
    return jsonify({"error": "Not found"}), 404

@app.route("/books", methods=["POST"])
def create_book():
    data = request.json
    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
        "publishedYear": data.get("publishedYear")
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    for book in books:
        if book["id"] == id:
            data = request.json
            book["title"] = data["title"]
            book["author"] = data["author"]
            book["publishedYear"] = data.get("publishedYear")
            return jsonify(book)
    return jsonify({"error": "Not found"}), 404

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    global books
    books = [b for b in books if b["id"] != id]
    return "", 204

# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)