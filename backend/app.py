from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from flask_bcrypt import Bcrypt
from algosdk import account, mnemonic, transaction
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from algosdk.v2client import algod


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_strong_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost/ikram_db'

jwt = JWTManager(app)  # Initialize JWTManager
db = SQLAlchemy(app)
CORS(app)


# Specify the node address and token.

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Issuer' or 'Trainee'
    wallet_address = db.Column(db.String(255), nullable=False)
    wallet_mnemonic = db.Column(db.String(255), nullable=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nft_asset_id = db.Column(db.Integer, nullable=False)  # Algorand NFT asset ID
    issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID of the issuer
    issued_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ipfs_hash = db.Column(db.String(255), nullable=True)  # IPFS hash of certificate data (optional)


# Create tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')  # 'Issuer' or 'Trainee'

    # Check for existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Create Algorand wallet
    private_key, address = account.generate_account()
    mnemonic_phrase = mnemonic.from_private_key(private_key)

    # Hash password
    hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')

    # Create user object
    user = User(
        username=username,
        password_hash=hashed_password,
        role=role,
        wallet_address=address,
        wallet_mnemonic=mnemonic_phrase  # Securely store the mnemonic
    )

    # Add user to database
    db.session.add(user)
    db.session.commit()

    # Return success message (optionally with wallet information)
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Find user by username
    user = User.query.filter_by(username=username).first()

    if user and Bcrypt().check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)  # Generate access token
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/issue_certificate/<trainee_id>', methods=['POST'])
@jwt_required()
def issue_certificate(trainee_id):
    user_id = get_jwt_identity()  # Get current user from JWT
    current_user = User.query.filter_by(id=user_id).first()
    print(f"current_user: {current_user.role}")

    # Authorization check
    if current_user.role != 'Issuer':
        return jsonify({"message": "Unauthorized"}), 401

    # ... (Code for generating certificate data and storing on IPFS)
    ipfs_hash = "https://ibb.co/PFCbvS3"  # IPFS hash of certificate data

    # Create Algorand NFT
    params = algod_client.suggested_params()
    params.flat_fee = 0  # Set flat fee to 1000 microAlgos
    params.fee=0
    txn = transaction.AssetConfigTxn(
        sender=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Use issuer's mnemonic
        sp=params,
        total=1,
        default_frozen=False,
        asset_name="Certificate",
        unit_name="Cert",
        url=ipfs_hash,
        decimals=0,
        manager=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
        freeze=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
        reserve=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
        clawback=account.address_from_private_key(mnemonic.to_private_key(current_user.wallet_mnemonic)),  # Or any appropriate address
    )
    signed_txn = txn.sign(mnemonic.to_private_key(current_user.wallet_mnemonic))
    tx_id = algod_client.send_transaction(signed_txn)
    nft_asset_id = signed_txn.get_asset_index()

    # Create Certificate object in database
    certificate = Certificate(
        user_id=trainee_id,
        nft_asset_id=nft_asset_id,
        issuer_id=current_user.id,
        title="Certificate of Completion",  # Example title
        description="Congratulations on completing the course!",  # Example description
        ipfs_hash=ipfs_hash
    )
    db.session.add(certificate)
    db.session.commit()

    return jsonify({"message": "NFT certificate issued successfully"}), 201


if __name__ == '__main__':
    app.run()