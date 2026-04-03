from flask import Blueprint, request, jsonify, make_response
from services import user_service
from authorization.auth import auth_required
import jwt
import datetime


SECRET_KEY = "bc123xyz456"


user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    email = data.get("email")
    password = data.get("password")

    user = user_service.login(email, password)

    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({"token": token})


@user_bp.route("/users", methods=["GET"])
@auth_required
def get_users():
    # Lấy query params page và size, mặc định page=0, size=10
    page = request.args.get("page", default=0, type=int)
    size = request.args.get("size", default=10, type=int)

    # Gọi service với page và size
    result = user_service.get_users(page=page, size=size)

    # Trả về danh sách user + metadata tổng số
    response_data = {
        "users": [u.to_dict() for u in result["users"]],
        "page": result["page"],
        "size": result["size"],
        "total": result["total"],
    }

    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


@user_bp.route("/users", methods=["POST"])
@auth_required
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    user = user_service.create_user(data)

    # nếu id đã tồn tại
    if user is None:
        return jsonify({"error": "User ID already exists"}), 400

    return jsonify(user.to_dict()), 201


@user_bp.route("/users/<id>", methods=["PUT"])
@auth_required
def update_user(id):

    data = request.get_json()

    user = user_service.update_user(id, data)

    if user is None:
        return "", 404

    return jsonify(user.to_dict())


@user_bp.route("/users/<id>", methods=["DELETE"])
@auth_required
def delete_user(id):

    result = user_service.delete_user(id)

    if not result:
        return "", 404

    return "", 204


# CODE ON DEMAND
@user_bp.route("/client-script", methods=["GET"])
@auth_required
def get_script():

    script = """
    console.log("Code on demand from server!");

    function hello(){
        alert("Hello Postmain!");
    }
    """

    response = make_response(script)
    response.headers["Content-Type"] = "application/javascript"

    return response
