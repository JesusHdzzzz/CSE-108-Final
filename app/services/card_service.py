import datetime
import sqlite3
from app.config import user_id, username
from app.models.db import get_db_connection
from flask import session

def add_card(data, user_id):
    cardholder_name = data.get("cardholder_name")
    card_number = data.get("card_number")
    card_type = data.get("card_type")
    expiration_date = data.get("expiration_date")
    billing_address = data.get("billing_address")
    cvv = data.get("cvv")

    if not all([cardholder_name, card_number, card_type, expiration_date, billing_address, cvv]):
        return {"error": "All fields are required."}, 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if card already exists for this user
        cursor.execute("SELECT * FROM cards WHERE card_number = ? AND user_id = ?", (card_number, user_id))
        if cursor.fetchone():
            return {"error": "Card already exists"}, 400

        cursor.execute("""
                INSERT INTO cards (cardholder_name, card_number, card_type, expiration_date, cvv, billing_address, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (cardholder_name, card_number, card_type, expiration_date, cvv, billing_address, user_id))

        conn.commit()
        return {"message": "Card added successfully"}, 200

    except sqlite3.Error as e:
        return {"error": str(e)}, 500

    finally:
        conn.close()


def retrieve_card(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cardholder_name, card_number, card_type, expiration_date, billing_address
            FROM cards
            WHERE user_id = ?;
        """, (user_id,))

        cards = cursor.fetchall()

        if not cards:
            return {"error": "You have no saved cards."}, 404

        card_list = [dict(card) for card in cards]
        return {"cards": card_list}, 200

    except sqlite3.Error as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
    finally:
        conn.close()

def delete_card_service(card_number, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the card from the database
        cursor.execute("""
            DELETE FROM cards
            WHERE card_number = ? 
            AND user_id = ?;
        """, (card_number, user_id))

        # Commit the transaction
        conn.commit()

        return {"message": "Card deleted successfully"}, 200

    except sqlite3.Error as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
    finally:
        conn.close()

def update_card_service(data, user_id):
    try:
        card_number = data.get("card_number", "").strip()
        cardholder_name = data.get("cardholder_name", "").strip()
        card_type = data.get("card_type", "").strip()
        expiration_date = data.get("expiration_date", "").strip()
        cvv = data.get("cvv", "").strip()
        billing_address = data.get("billing_address", "").strip()

        if not card_number or not card_number.isdigit() or len(card_number) != 16:
            return {"error": "Invalid or missing card number."}, 400

        if card_type not in ['Visa', 'MasterCard', 'American Express']:
            return {"error": "Invalid card type."}, 400

        # Validate expiration date
        try:
            exp_year, exp_month = map(int, expiration_date.split("-"))
            now = datetime.datetime.now()
            if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
                return {"error": "Card is expired."}, 400
        except Exception:
            return {"error": "Invalid expiration date format (use YYYY-MM)."}, 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT card_number FROM cards WHERE card_number = ? AND user_id = ?", (card_number, user_id))
        existing_card = cursor.fetchone()
        if not existing_card:
            return {"error": "Card does not exist."}, 404

        # Perform update
        cursor.execute("""
            UPDATE cards
            SET cardholder_name = ?, card_type = ?, expiration_date = ?, cvv = ?, billing_address = ?
            WHERE card_number = ? AND user_id = ?;
        """, (cardholder_name, card_type, expiration_date, cvv, billing_address, card_number, user_id))

        # Log it into history
        cursor.execute("""
            INSERT INTO history (user_id, action_type, action_details, action_timestamp)
            VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Card updated",
            f"Updated card ************{card_number[-4:]} for {username}",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))

        # Commit the transaction
        conn.commit()
        return {"message": "Card updated successfully"}, 200

    except Exception as e:
        conn.rollback()
        print("Database error:", e)
        return {"error": str(e)}, 500

    finally:
        conn.close()