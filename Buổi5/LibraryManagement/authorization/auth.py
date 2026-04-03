import jwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "manhtran111"


def auth_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

       
        if auth_header:

            try:

                token = auth_header.split(" ")[1]

                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

                return f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401

            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

        #Không JWT
        return (
            jsonify(
                {"error": "Authentication required", "message": "Please login first"}
            ),
            401,
        )

    return decorated
