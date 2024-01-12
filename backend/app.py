from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from algorand_utils import Algorand
from flask import session
import logging
import json


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

algorand  = Algorand()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_strong_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost/tenx_db'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SECRET_KEY'] = 'your_secret_key_here'

jwt = JWTManager(app)  # Initialize JWTManager
db = SQLAlchemy(app)
CORS(app)

class UserRole(Enum):
    ISSUER = 'Issuer'
    TRAINEE = 'Trainee'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    account_address = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()


@app.route('/api/v1/register', methods=['POST'])
def register():
    """
    Registers a new user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        role_str (str): The role of the user ('Issuer' or 'Trainee').

    Returns:
        JSON: A response indicating the success or failure of the registration.
    """
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role_str = request.json.get('role')  # 'Issuer' or 'Trainee'

        # Check for existing user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Username already exists"}), 400


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
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        logging.error(f"Registration failed: {e}")
        return jsonify({"message": f"Registration failed: {e}"}), 500


@app.route('/api/v1/login', methods=['POST'])
def login():
    """
    Logs in a user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        JSON: A response containing the access token, username, account_address, and role if login is successful.
    """
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
                "access_token": access_token,
                "username": user.username,
                "account_address": user.account_address,
                "role": user.role.value
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        logging.error(f"Login failed: {e}")
        return jsonify({"message": f"Login failed: {e}"}), 500


@app.route('/api/v1/logout', methods=['GET'])
def logout():
    """
    Logs out the current user.

    Returns:
        JSON: A response indicating the success of the logout.
    """
    try:
        # Clear user-specific information from the session
        session.pop('wallet', None)
        return jsonify({"message": "Logout success"}), 200

    except Exception as e:
        logging.error(f"Logout failed: {e}")
        return jsonify({"message": "Logout failed"}), 500

if __name__ == '__main__':
    app.run()

# @app.route('/issue_certificate/<trainee_id>', methods=['POST'])
# @jwt_required()
# def issue_certificate(trainee_id):
#     user_id = get_jwt_identity()  # Get current user from JWT
#     current_user = User.query.filter_by(id=user_id).first()
#     print(f"current_user: {current_user.role}")

#     # Authorization check
#     if current_user.role != 'Issuer':
#         return jsonify({"message": "Unauthorized"}), 401

#     # ... (Code for generating certificate data and storing on IPFS)
#     ipfs_hash = "https://ibb.co/PFCbvS3"  # IPFS hash of certificate data

#     # Create Algorand NFT
#     params = algod_client.suggested_params()
#     params.flat_fee = 0  # Set flat fee to 1000 microAlgos
#     params.fee=0
#     txn = transaction.AssetConfigTxn(
#         sender=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Use issuer's mnemonic
#         sp=params,
#         total=1,
#         default_frozen=False,
#         asset_name="Certificate",
#         unit_name="Cert",
#         url=ipfs_hash,
#         decimals=0,
#         manager=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
#         freeze=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
#         reserve=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
#         clawback=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
#     )
#     signed_txn = txn.sign(mnemonic.to_private_key(current_user.wallet_mnemonic))
#     tx_id = algod_client.send_transaction(signed_txn)
#     nft_asset_id = signed_txn.get_asset_index()

#     # Create Certificate object in database
#     certificate = Certificate(
#         user_id=trainee_id,
#         nft_asset_id=nft_asset_id,
#         issuer_id=current_user.id,
#         title="Certificate of Completion",  # Example title
#         description="Congratulations on completing the course!",  # Example description
#         ipfs_hash=ipfs_hash
#     )
#     db.session.add(certificate)
#     db.session.commit()

#     return jsonify({"message": "NFT certificate issued successfully"}), 201




# class Certificate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     nft_asset_id = db.Column(db.Integer, nullable=False)  # Algorand NFT asset ID
#     issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID of the issuer
#     issued_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     ipfs_hash = db.Column(db.String(255), nullable=True)  # IPFS hash of certificate data (optional)
