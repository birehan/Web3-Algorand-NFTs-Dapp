from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from challenge_api import challenge_bp
from certificate_api import certificate_bp
from models import db
from user_api import register_user, login_user, logout_user

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_strong_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost/tenx_db'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SECRET_KEY'] = 'your_secret_key_here'

jwt = JWTManager(app)  # Initialize JWTManager
db.init_app(app)  # Initialize SQLAlchemy for the app
CORS(app)



# Create tables
with app.app_context():
    db.create_all()

# User-related routes
app.route('/api/v1/register', methods=['POST'])(register_user)
app.route('/api/v1/login', methods=['POST'])(login_user)
app.route('/api/v1/logout', methods=['GET'])(logout_user)

app.register_blueprint(challenge_bp, url_prefix='/api/v1')  # Register the challenge_bp Blueprint
app.register_blueprint(certificate_bp, url_prefix='/api/v1')  # Register the challenge_bp Blueprint

if __name__ == '__main__':
    app.run()