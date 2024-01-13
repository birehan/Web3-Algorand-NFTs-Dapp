from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

class UserRole(Enum):
    ISSUER = 'Issuer'
    TRAINEE = 'Trainee'

class ApprovalStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DENIED = 'Denied'
    NO_REQUEST = 'NoRequest'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    account_address = db.Column(db.String(255), nullable=False)
    certificates = db.relationship('Certificate', backref='user', lazy=True, foreign_keys='Certificate.user_id')


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Staff member who approves/denies the request
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nft_id = db.Column(db.String(255), unique=True, nullable=False)  # Assuming you have an NFT identifier
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    is_approved = db.Column(db.Enum(ApprovalStatus), default=ApprovalStatus.NO_REQUEST)
    ipfs_hash = db.Column(db.String(255), nullable=False)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    batch_number = db.Column(db.Integer, nullable=False)
    certificates = db.relationship('Certificate', backref='challenge', lazy=True)