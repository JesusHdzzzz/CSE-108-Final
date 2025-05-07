from flask import Blueprint, request, jsonify

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    passoword = data.get("password")

    # TODO: Replace with actual DB check
    if username == "admin" and passoword == "admin":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


"""
    TODO: Add user registration, password hashing/salting
"""