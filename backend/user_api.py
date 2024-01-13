from flask import jsonify, request, session
from flask_jwt_extended import create_access_token
from algorand_utils import Algorand
import logging
import json
from models import User, UserRole
from flask_bcrypt import Bcrypt
from models import db
import pickle

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

algorand = Algorand()

def generate_response(is_success, value=None, error=None):
    response = {
        "isSuccess": is_success,
        "value": value,
        "error": error
    }
    return jsonify(response)

def register_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role_str = request.json.get('role')  # 'Issuer' or 'Trainee'

        # Check for existing user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return generate_response(False, None, "Username already exists"), 400

        if role_str not in ['Issuer', 'Trainee']:
            return generate_response(False, None, "Invalid role value"), 400

        role = UserRole.ISSUER if role_str == "Issuer" else UserRole.TRAINEE

        account_address = algorand.create_user(username, password)

        # Hash password
        hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')

        # Create user object
        user = User(
            username=username,
            password_hash=hashed_password,
            role=role,
            account_address=account_address
        )

        # Add user to the database
        db.session.add(user)
        db.session.commit()

        # Return success message (optionally with wallet information)
        return generate_response(True, None, None), 201

    except Exception as e:
        logging.error(f"Registration failed: {e}")
        return generate_response(False, None, f"Registration failed: {e}"), 500

def login_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        wallet = algorand.login_user(username, password)

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if user and Bcrypt().check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)  # Generate access token

            # Convert Wallet object to a serialized string
            wallet_str = pickle.dumps(wallet)

            # Store the serialized wallet in the session
            session['wallet'] = wallet_str

            # Return additional information with the access token
            response_data = {
                "id": user.id,
                "access_token": access_token,
                "username": user.username,
                "account_address": user.account_address,
                "role": user.role.value
            }
            return generate_response(True, response_data, None), 200
        else:
            return generate_response(False, None, "Invalid username or password"), 401

    except Exception as e:
        logging.error(f"Login failed: {e}")
        return generate_response(False, None, f"Login failed: {e}"), 500

def logout_user():
    try:
        # Clear user-specific information from the session
        session.pop('wallet', None)
        return generate_response(True, None, None), 200

    except Exception as e:
        logging.error(f"Logout failed: {e}")
        return generate_response(False, None, "Logout failed"), 500
