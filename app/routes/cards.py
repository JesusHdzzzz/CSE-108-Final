from flask import Blueprint, jsonify, request
from app.services.card_service import add_card, update_card_service, retrieve_card, delete_card_service

bp = Blueprint('cards', __name__)

@bp.route('/', methods=['POST'])
def create_card():
    print("----- Add card function called -----")	
    data = request.get_json()
    result, status = add_card(data)
    return jsonify(result), status

@bp.route('/', methods=['GET'])
def get_cards():
    print("----- Get cards function called -----")
    result, status = retrieve_card()
    return jsonify(result), status

@bp.route('/', methods=['DELETE'])
def delete_card():
    print("----- Delete card function called -----")
    data = request.get_json()
    card_number = data.get("card_number")

    if not card_number:
        return jsonify({"error": "Card number is required"}), 400

    result, status = delete_card_service(card_number)
    return jsonify(result), status

@bp.route('/', methods=['PUT'])
def update_card():
    print("----- Update card function called -----")
    data = request.get_json()
    result, status = update_card_service(data)
    return jsonify(result), status