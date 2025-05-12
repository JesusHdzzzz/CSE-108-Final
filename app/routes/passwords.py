from flask import Blueprint, jsonify, request, session
from app.services.password_service import (
    retrieve_webPass, retrieve_allPass, update_webPass_service,
    save_webPass, delete_webPass_service, save_website, delete_website_service
)

bp = Blueprint('passwords', __name__)

def get_user_id():
    user_id = session.get("user_id")
    if not user_id:
        return None, jsonify({"error": "Not logged in"}), 401
    return user_id, None, None

@bp.route('/website/view', methods=['POST'])
def get_webPass():
    print("----- Get web password function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = retrieve_webPass(data, user_id)
    return jsonify(result), status

@bp.route('/all', methods=['GET'])
def get_allPass():
    print("----- Get group password function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    result, status = retrieve_allPass(user_id)
    return jsonify(result), status

@bp.route('/website', methods=['PUT'])
def update_webPass():
    print("----- Update web password function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = update_webPass_service(data, user_id)
    return jsonify(result), status

@bp.route('/website', methods=['POST'])
def create_webPass():
    print("----- Create web password function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = save_webPass(data, user_id)
    return jsonify(result), status

@bp.route('/website', methods=['DELETE'])
def delete_webPass():
    print("----- Delete web password function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = delete_webPass_service(data, user_id)
    return jsonify(result), status

@bp.route('/websites', methods=['POST'])
def create_website():
    print("----- Create website function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = save_website(data, user_id)
    return jsonify(result), status

@bp.route('/websites', methods=['DELETE'])
def delete_website():
    print("----- Delete website function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = delete_website_service(data, user_id)
    return jsonify(result), status