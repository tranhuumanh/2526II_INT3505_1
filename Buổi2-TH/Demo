from flask import Flask, jsonify

app = Flask(__name__)

# Fake database
books = [
    {"id": 1, "title": "Harry Potter", "author": "J.K. Rowling"},
    {"id": 2, "title": "Norwegian Wood", "author": "Haruki Murakami"}
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    for book in books:
        if book["id"] == id:
            return jsonify(book)
    return {"error": "Book not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)