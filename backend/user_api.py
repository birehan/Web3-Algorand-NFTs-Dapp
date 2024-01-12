from flask import jsonify, request, session
from flask_jwt_extended import create_access_token
from algorand_utils import Algorand
import logging
import json
from models import User, UserRole
from flask_bcrypt import Bcrypt
from models import db


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

algorand = Algorand()

def register_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role_str = request.json.get('role')  # 'Issuer' or 'Trainee'

        # Check for existing user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Username already exists", "data": ""}), 400

        if role_str not in ['Issuer', 'Trainee']:
            return jsonify({"message": "Invalid role value"}), 400

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

        # Add user to database
        db.session.add(user)
        db.session.commit()

        # Return success message (optionally with wallet information)
        return jsonify({"message": "User registered successfully", "data": ""}), 201

    except Exception as e:
        logging.error(f"Registration failed: {e}")
        return jsonify({"message": f"Registration failed: {e}"}), 500


def login_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        wallet = algorand.logi_user(username, password)

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if user and Bcrypt().check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)  # Generate access token

            # Convert Wallet object to a JSON serializable string
            wallet_str = json.dumps(wallet, default=lambda o: o.__dict__)

            # Store the serialized wallet in the session
            session['wallet'] = wallet_str

            # Return additional information with the access token
            return jsonify({
               "message": "user login success",
               "data": {
                "access_token": access_token,
                "username": user.username,
                "account_address": user.account_address,
                "role": user.role.value
               }
            }), 200
        else:
            return jsonify({"message": "Invalid username or password", "data": ""}), 401

    except Exception as e:
        logging.error(f"Login failed: {e}")
        return jsonify({"message": f"Login failed: {e}", "data": ""}), 500


def logout_user():
    try:
        # Clear user-specific information from the session
        session.pop('wallet', None)
        return jsonify({"message": "Logout success", "data": ""}), 200

    except Exception as e:
        logging.error(f"Logout failed: {e}")
        return jsonify({"message": "Logout failed", "data": ""}), 500
