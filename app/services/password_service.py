import datetime
import sqlite3
from app.config import user_id, username  # must match what's used below
from app.models.db import get_db_connection

def retrieve_webPass(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        website_name = data.get("website_name", "").strip()

        # Check if website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        row_id = cursor.fetchone()

        if not row_id:
            return {"error": "website does not exist"}, 404

        # Execute the query to retrieve the password for the given user and website
        cursor.execute("""SELECT web_pass 
            FROM web_pass, web
            WHERE user_id = ? 
            AND web_pass.website_id = web.website_id
            AND website_name = ?""", (user_id, website_name))
        web_pass = cursor.fetchone()

        # Check if a password was found
        if not web_pass:
            return {"error": "You have no saved password for " + website_name + "."}, 404
        
        return {"Website password": web_pass[0]}, 200
    except sqlite3.Error as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    finally:
        conn.close()

def retrieve_allPass():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query to retrieve all passwords for the given user
        cursor.execute("""
            SELECT web_pass.web_pass, web.website_name
            FROM web_pass
            JOIN web ON web_pass.website_id = web.website_id
            WHERE web_pass.user_id = ?
        """, (user_id,))

        web_passes = cursor.fetchall()
        web_passes_list = [dict(web_pass) for web_pass in web_passes]

        return {"Passwords": web_passes_list}, 200

    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def update_webPass_service(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        website_name = data.get("website_name", "").strip()
        new_pass = data.get("new_pass", "").strip()

        # Check if website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        row_id = cursor.fetchone()

        if not row_id:
            return {"error": "website does not exist"}, 404

        # Execute the query to check for a pass
        cursor.execute("""SELECT web_pass 
            FROM web_pass, web
            WHERE user_id = ? 
            AND web_pass.website_id = web.website_id
            AND website_name = ?""", (user_id, website_name))
        web_pass = cursor.fetchone()

        # Check if a password was found
        if not web_pass:
            return {"error": "You have no saved password for " + website_name + "."}, 404

        # Execute the query to update the password for the given user and website
        cursor.execute("""
            UPDATE web_pass
            SET web_pass = ?
            WHERE user_id = ?
            AND website_id = (
                SELECT website_id
                FROM web
                WHERE website_name = ?
            )
            """, (new_pass, user_id, website_name))

        # Add into history table
        cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Password change",
            f"Updated {website_name} password",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))

        conn.commit()
        return {"message": website_name + " password updated successfully."}, 200

    except sqlite3.Error as e:
        print("Database error: ", e)
    finally:
        conn.close()

def save_webPass(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        website_name = data.get("website_name", "").strip()
        web_pass = data.get("web_pass", "").strip()

        # Check if website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        row_id = cursor.fetchone()

        if not row_id:
            return {"error": "website does not exist"}, 404
        
        website_id = row_id[0]

        # Check for existing password entry
        cursor.execute("""
            SELECT web_pass
            FROM web_pass
            WHERE user_id = ? AND website_id = ?
        """, (user_id, website_id))

        existing_pass = cursor.fetchone()

        if existing_pass:
            return {"error": "A password for this website already exists. Use the update option to modify it."}, 404

        # Insert the password for the website
        cursor.execute("""
            INSERT INTO web_pass (user_id, website_id, web_pass)
            VALUES (?, ?, ?)
        """, (user_id, website_id, web_pass))
        conn.commit()

        # Create link for the website and user in user_web table
        cursor.execute("""
            INSERT INTO user_web (user_id, website_id)
            VALUES (?, ?)
        """, (user_id, website_id))
        conn.commit()

        # Add into history table
        cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Password added",
            f"Added password for {website_name}",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()

        return {"message": "Password saved successfully stored in History and Logs."}, 200

    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def delete_webPass_service(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get website details
        website_name = data.get("website_name", "").strip()

        # Check if the website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        result = cursor.fetchone()

        if not result:
            return {"error": "website does not exist."}, 404
        
        website_id = result[0]

        # If the website exists, delete the password
        cursor.execute("""
            DELETE FROM web_pass
            WHERE user_id = ? AND website_id = ?
        """, (user_id, website_id))
        conn.commit()

        # Delete link between user and website in user_web table
        cursor.execute("""
            DELETE FROM user_web
            WHERE user_id = ? AND website_id = ?
        """, (user_id, website_id))
        conn.commit()

        # Add into history table
        cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Password deleted",
            f"Deleted password for {website_name}",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()

        return {"message": "Password deleted successfully and stored in History and Logs."}, 200
        
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def save_website(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get website details
        website_name = data.get("website_name", "").strip()
        website_url = data.get("website_url", "").strip()

        # Check if the website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        result = cursor.fetchone()

        if result:
            return {"error": "website already exists."}, 404
        
        cursor.execute("""
                INSERT INTO web (website_name, website_url)
                VALUES (?, ?)
        """, (website_name, website_url))
        conn.commit()

        # Add into history table
        cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Website created",
            f"Created website for {website_name}",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()

        return {"message": "Website added successfully and stored in History and Logs."}, 200
        
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def delete_website_service(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get website details
        website_name = data.get("website_name", "").strip()

        # Check if the website exists
        cursor.execute("""
            SELECT website_id
            FROM web
            WHERE website_name = ?
        """, (website_name,))
        result = cursor.fetchone()

        if not result:
            return {"error": "website does not exist."}, 404
        
        website_id = result[0]
        
        # If the website exists, delete the it
        cursor.execute("""
            DELETE FROM web
            WHERE website_name = ?
        """, (website_name,))
        conn.commit()

        cursor.execute("""
            DELETE FROM user_web
            WHERE user_id = ? AND website_id = ?
        """, (user_id, website_id))
        conn.commit()

        cursor.execute("""
            DELETE FROM web_pass
            WHERE user_id = ? AND website_id = ?
        """, (user_id, website_id))
        conn.commit()

        # Add into history table
        cursor.execute("""
        INSERT INTO history (user_id, action_type, action_details, action_timestamp)
        VALUES (?, ?, ?, ?);
        """, (
            user_id,
            "Website deleted",
            f"Deleted website for {website_name}",
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()

        return {"message": "Website deleted successfully and stored in History and Logs."}, 200
        
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()