from flask import Blueprint, jsonify, request, session
from app.services.card_service import (
    add_card, update_card_service, retrieve_card,
    delete_card_service
)

bp = Blueprint('cards', __name__)

def get_user_id():
    user_id = session.get("user_id")
    if not user_id:
        return None, jsonify({"error": "Not logged in"}), 401
    return user_id, None, None

@bp.route('/', methods=['POST'])
def create_card():
    print("----- Add card function called -----")	
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = add_card(data, user_id)
    return jsonify(result), status

@bp.route('/', methods=['GET'])
def get_cards():
    print("----- Get cards function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    result, status = retrieve_card(user_id)
    return jsonify(result), status

@bp.route('/', methods=['DELETE'])
def delete_card():
    print("----- Delete card function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    card_number = data.get("card_number")
    if not card_number:
        return jsonify({"error": "Card number is required"}), 400

    result, status = delete_card_service(card_number, user_id)
    return jsonify(result), status

@bp.route('/', methods=['PUT'])
def update_card():
    print("----- Update card function called -----")
    user_id, error, status = get_user_id()
    if error: return error, status

    data = request.get_json()
    result, status = update_card_service(data, user_id)
    return jsonify(result), status
