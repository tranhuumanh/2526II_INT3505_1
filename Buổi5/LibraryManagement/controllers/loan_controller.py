from flask import Blueprint, request, jsonify
from services import loan_service
from authorization.auth import auth_required

loan_bp = Blueprint("loan_bp", __name__)


@loan_bp.route("/loans", methods=["GET"])
@auth_required
def get_loans():
    page = request.args.get("page", type=int)
    size = request.args.get("size", type=int)

    loans = loan_service.get_loans(page=page, size=size)
    return jsonify([l.to_dict() for l in loans])


@loan_bp.route("/loans", methods=["POST"])
@auth_required
def create_loan():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    loan = loan_service.create_loan(data)
    if loan is None:
        return jsonify({"error": "Loan ID already exists"}), 400

    return jsonify(loan.to_dict()), 201


@loan_bp.route("/loans/<id>", methods=["PUT"])
@auth_required
def update_loan(id):
    data = request.get_json()
    loan = loan_service.update_loan(id, data)
    if loan is None:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify(loan.to_dict())


@loan_bp.route("/loans/<id>", methods=["DELETE"])
@auth_required
def delete_loan(id):
    result = loan_service.delete_loan(id)
    if not result:
        return jsonify({"error": "Loan not found"}), 404
    return "", 204
