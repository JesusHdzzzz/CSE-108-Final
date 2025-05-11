from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import config
import datetime
from create_tables import createTable

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)  # Enable cross-origin requests

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def initialize_db():
    conn = get_db_connection()
    createTable(conn)
    conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Email already exists'}), 409

        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()

        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()['user_id']

        cursor.execute("INSERT INTO pass (user_id, m_pass) VALUES (?, ?)", (user_id, password))
        conn.commit()

        return jsonify({'success': True, 'message': 'Account created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password_input = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT pass.m_pass, users.user_id
        FROM users 
        JOIN pass ON users.user_id = pass.user_id 
        WHERE users.username = ?
    """
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and password_input == user['m_pass']:
        session['username'] = username
        session['user_id'] = user['user_id']
        return jsonify({'success': True, 'message': 'Login successful', 'user_id': user['user_id']}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'}), 200

@app.route('/passwords/web', methods=['GET'])
def retrieve_web_pass():
    website_name = request.args.get('website_name', '').strip().lower()
    user_id = config.user_id

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT wp.web_pass 
            FROM web_pass wp
            JOIN web w ON wp.website_id = w.website_id
            WHERE wp.user_id = ? AND w.website_name = ?
        """, (user_id, website_name))

        web_pass = cursor.fetchone()

        if web_pass:
            return jsonify({
                "username": config.username,
                "website": website_name,
                "password": web_pass["web_pass"]
            })
        else:
            return jsonify({"error": "No password found."}), 404

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return redirect(url_for('view_cards'))

@app.route('/cards')
def view_cards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cardholder_name, card_number, card_type, expiration_date, billing_address
        FROM cards
        WHERE user_id = ?;
    """, (config.user_id,))
    cards = cursor.fetchall()
    conn.close()
    return render_template('cards.html', cards=cards)

@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        cardholder_name = request.form['cardholder_name'].strip()
        card_number = request.form['card_number'].strip()
        card_type = request.form['card_type'].strip()
        expiration_date = request.form['expiration_date'].strip()
        billing_address = request.form['billing_address'].strip()

        if not card_number.isdigit() or len(card_number) != 16:
            flash('Invalid card number.')
            return redirect(url_for('add_card'))

        if card_type not in ['Visa', 'MasterCard', 'American Express']:
            flash('Invalid card type.')
            return redirect(url_for('add_card'))

        try:
            year, month = map(int, expiration_date.split('-'))
            now = datetime.datetime.now()
            if year < now.year or (year == now.year and month < now.month):
                flash('Card has expired.')
                return redirect(url_for('add_card'))
        except:
            flash('Invalid expiration date format. Use YYYY-MM.')
            return redirect(url_for('add_card'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT card_number FROM cards WHERE card_number = ?", (card_number,))
        if cursor.fetchone():
            flash('Card number already exists.')
            conn.close()
            return redirect(url_for('add_card'))

        cursor.execute("""
            INSERT INTO cards (cardholder_name, card_number, card_type, expiration_date, billing_address, user_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (cardholder_name, card_number, card_type, expiration_date, billing_address, config.user_id))

        cursor.execute("""
            INSERT INTO history (user_id, action_type, action_details, action_timestamp)
            VALUES (?, 'Card added', ?, ?);
        """, (config.user_id, f"Added {card_type} card", datetime.datetime.now().strftime('%Y-%m-%d')))

        conn.commit()
        conn.close()
        flash('Card added successfully.')
        return redirect(url_for('view_cards'))

    return render_template('add_card.html')

@app.route('/delete_card/<card_number>')
def delete_card(card_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cards WHERE card_number = ? AND user_id = ?", (card_number, config.user_id))
    cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, 'Card deleted', ?, ?);
    """, (config.user_id, f"Deleted card ****{card_number[-4:]}", datetime.datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    flash('Card deleted successfully.')
    return redirect(url_for('view_cards'))

@app.route('/update_card/<card_number>', methods=['GET', 'POST'])
def update_card(card_number):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cardholder_name = request.form['cardholder_name'].strip()
        card_type = request.form['card_type'].strip()
        expiration_date = request.form['expiration_date'].strip()
        billing_address = request.form['billing_address'].strip()

        if card_type not in ['Visa', 'MasterCard', 'American Express']:
            flash('Invalid card type.')
            return redirect(url_for('update_card', card_number=card_number))

        cursor.execute("""
            UPDATE cards
            SET cardholder_name = ?, card_type = ?, expiration_date = ?, billing_address = ?
            WHERE card_number = ? AND user_id = ?;
        """, (cardholder_name, card_type, expiration_date, billing_address, card_number, config.user_id))

        cursor.execute("""
            INSERT INTO history (user_id, action_type, action_details, action_timestamp)
            VALUES (?, 'Card updated', ?, ?);
        """, (config.user_id, f"Updated card ****{card_number[-4:]}", datetime.datetime.now().strftime('%Y-%m-%d')))

        conn.commit()
        conn.close()
        flash('Card updated successfully.')
        return redirect(url_for('view_cards'))

    cursor.execute("SELECT * FROM cards WHERE card_number = ? AND user_id = ?", (card_number, config.user_id))
    card = cursor.fetchone()
    conn.close()
    return render_template('update_card.html', card=card)

if __name__ == '__main__':
    app.run(debug=True)