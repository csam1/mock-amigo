from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db
from app.routes import user_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(user_routes.bp)
    
    return app
