from flask_cors import CORS
from flask import Flask
from app.routes import auth, cards, passwords

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret-key"
    
    app.config.update(
    SESSION_COOKIE_SECURE=True,     # Only send cookies over HTTPS
    SESSION_COOKIE_SAMESITE='None', # Allow cross-site cookies (for Vercel <-> Render)
    )

    CORS(app, supports_credentials=True)

    app.register_blueprint(auth.bp, url_prefix='/auth')	
    app.register_blueprint(cards.bp, url_prefix='/cards')
    app.register_blueprint(passwords.bp, url_prefix='/passwords')
    
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app