from flask import Blueprint, request, jsonify, session
from app.services.auth_service import register_user, login_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    result, status = register_user(username, email, password)
    return jsonify(result), status


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result, status = login_user(username, password)
    
    if status == 200:
        session['user_id'] = result['user_id'] 
        session['username'] = username
    return jsonify(result), status

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200
