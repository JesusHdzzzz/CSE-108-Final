import bcrypt
import re
from app.models.db import get_db_connection
from flask import session

def register_user(username, email, password):
    # Email format validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Invalid email format"}, 400

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters long."}, 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return {"error": "Email already exists"}, 409

        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return {"error": "Username already exists"}, 409

        # Insert user
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        user_id = cursor.lastrowid

        # Hash and store password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO pass (user_id, m_pass) VALUES (?, ?)", (user_id, hashed_pw))

        conn.commit()
        return {"message": "Account created successfully", "user_id": user_id}, 201

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        conn.close()


def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT pass.m_pass, users.user_id
            FROM users
            JOIN pass ON users.user_id = pass.user_id
            WHERE users.username = ?
        """, (username,))
        user = cursor.fetchone()

        if not user:
            return {"error": "Username not found"}, 404

        stored_hash = user["m_pass"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            session['user_id'] = user['user_id']
            session['username'] = username
            return {"message": "Login successful", "user_id": user["user_id"]}, 200
        else:
            return {"error": "Incorrect password"}, 401

    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        conn.close()
