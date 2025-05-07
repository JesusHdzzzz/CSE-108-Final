from flask import Flask
from app.routes import auth, cards

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret-key" # Replace with enviroment variable later
    
    app.register_blueprint(auth.bp, url_prefix='/auth')	
    app.register_blueprint(cards.bp, url_prefix='/cards')
    
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app