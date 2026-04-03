from flask import Blueprint, request, jsonify, make_response
from services import book_service
from authorization.auth import auth_required

book_bp = Blueprint("book_bp", __name__)


@book_bp.route("/books", methods=["GET"])
@auth_required
def get_books():
    page = request.args.get("page", type=int)
    size = request.args.get("size", type=int)

    books = book_service.get_books(page=page, size=size)
    return jsonify([b.to_dict() for b in books])


@book_bp.route("/books", methods=["POST"])
@auth_required
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    book = book_service.create_book(data)
    if book is None:
        return jsonify({"error": "Book ID already exists"}), 400

    return jsonify(book.to_dict()), 201


@book_bp.route("/books/<id>", methods=["PUT"])
@auth_required
def update_book(id):
    data = request.get_json()
    book = book_service.update_book(id, data)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())


@book_bp.route("/books/<id>", methods=["DELETE"])
@auth_required
def delete_book(id):
    result = book_service.delete_book(id)
    if not result:
        return jsonify({"error": "Book not found"}), 404
    return "", 204
