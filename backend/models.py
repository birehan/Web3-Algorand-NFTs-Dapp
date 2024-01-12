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

# Bridge table for the many-to-many relationship between User and Challenge
user_challenge_association = db.Table(
    'user_challenge_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    account_address = db.Column(db.String(255), nullable=False)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    challenges = db.relationship('Challenge', secondary=user_challenge_association, backref=db.backref('users', lazy=True))
    opt_in_requests = db.relationship('OptInRequest', backref='trainee', lazy=True, foreign_keys='OptInRequest.trainee_id')


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nft_id = db.Column(db.String(255), unique=True, nullable=False)  # Assuming you have an NFT identifier
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)

class OptInRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'), nullable=False)
    is_approved = db.Column(db.Enum(ApprovalStatus), default=ApprovalStatus.NO_REQUEST)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Staff member who approves/denies the request
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    batch_number = db.Column(db.Integer, nullable=False)
    certificates = db.relationship('Certificate', backref='challenge', lazy=True)