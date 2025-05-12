from flask import Blueprint, jsonify, request
from app.services.password_service import retrieve_webPass, retrieve_allPass, update_webPass_service, save_webPass, delete_webPass_service, save_website, delete_website_service

bp = Blueprint('passwords', __name__)

@bp.route('/website', methods=['GET'])
def get_webPass():
    print("----- Get web password function called -----")
    data = request.get_json()
    result, status = retrieve_webPass(data)
    return jsonify(result), status

@bp.route('/all', methods=['GET'])
def get_allPass():
    print("----- Get group password function called -----")
    result, status = retrieve_allPass()
    return jsonify(result), status

@bp.route('/website', methods=['PUT'])
def update_webPass():
    print("----- Update web password function called -----")
    data = request.get_json()
    result, status = update_webPass_service(data)
    return jsonify(result), status

@bp.route('/website', methods=['POST'])
def create_webPass():
    print("----- Create web password function called -----")
    data = request.get_json()
    result, status = save_webPass(data)
    return jsonify(result), status

@bp.route('/website', methods=['DELETE'])
def delete_webPass():
    print("----- Create web password function called -----")
    data = request.get_json()
    result, status = delete_webPass_service(data)
    return jsonify(result), status

@bp.route('/websites', methods=['POST'])
def create_website():
    print("----- Create website function called -----")
    data = request.get_json()
    result, status = save_website(data)
    return jsonify(result), status

@bp.route('/websites', methods=['DELETE'])
def delete_website():
    print("----- Delete website function called -----")
    data = request.get_json()
    result, status = delete_website_service(data)
    return jsonify(result), status