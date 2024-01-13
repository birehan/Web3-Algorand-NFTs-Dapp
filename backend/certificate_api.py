from datetime import datetime
from flask import jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Certificate, ApprovalStatus, UserRole
from flask import Blueprint
from models import db
from models import User, Challenge
from certificate_utils import customize_certificate
from algorand_utils import Algorand
import json
import pickle

algorand = Algorand()

certificate_bp = Blueprint('certificate', __name__)

def generate_response(is_success, value=None, error=None):
    response = {
        "isSuccess": is_success,
        "value": value,
        "error": error
    }
    return jsonify(response)

@certificate_bp.route('/certificates', methods=['POST'])
@jwt_required()
def create_certificate():
    try:
        current_user_id = get_jwt_identity()
        title = request.json.get('title')
        score = request.json.get('score')
        challenge_id = request.json.get('challenge_id')
        user_id = request.json.get('user_id')

        if not title or score is None or challenge_id is None or not user_id:
            return generate_response(False, None, "Missing required fields"), 400
        
        sender_user = User.query.filter_by(id=current_user_id).first()
        if not sender_user:
            return generate_response(False, None, "Sender User does not exist"), 400
        
        receiving_user = User.query.filter_by(id=user_id).first()
        if not receiving_user:
            return generate_response(False, None, "Receiving User does not exist"), 400
        
        challenge = Challenge.query.filter_by(id=challenge_id).first()
        if not challenge:
            return generate_response(False, None, "Challenge does not exist"), 400
        
        ipfs_hash = customize_certificate(
            username=receiving_user.username,
            title=title,
            issued_date=datetime.utcnow().strftime("%B %d, %Y"),
            week_number=challenge.week_number
        )
        
        stored_wallet_str = session.get('wallet', None)

        if stored_wallet_str:
            wallet = pickle.loads(stored_wallet_str)
        else:
            return generate_response(False, None, "Wallet information not found in the session.")
        
        nft_id = algorand.create_asset(
            sender_address=sender_user.account_address,
            sender_private_key=algorand.get_private_key(wallet, sender_user.account_address),
            asset_url=ipfs_hash,
            asset_name=title
        )

        new_certificate = Certificate(
            title=title,
            score=score,
            staff_id=current_user_id,
            user_id=user_id,
            challenge_id=challenge_id,
            ipfs_hash=ipfs_hash,
            nft_id=nft_id
        )

        db.session.add(new_certificate)
        db.session.commit()

        certificate_info = {
            'id': new_certificate.id,
            'title': new_certificate.title,
            'score': new_certificate.score,
            'issued_date': new_certificate.issued_date,
            'staff_id': new_certificate.staff_id,
            'user_id': new_certificate.user_id,
            'nft_id': new_certificate.nft_id,
            'challenge_id': new_certificate.challenge_id,
            'is_approved': new_certificate.is_approved.value,
            'ipfs_hash': new_certificate.ipfs_hash
        }

        return generate_response(True, certificate_info, "Certificate created successfully"), 201

    except Exception as e:
        return generate_response(False, None, f"Error creating certificate: {e}"), 500

@certificate_bp.route('/certificates/optin/<int:certificate_id>', methods=['PUT'])
@jwt_required()
def request_optin(certificate_id):
    try:
        password = request.json.get('password')

        if not password:
            return generate_response(False, None, "Missing required fields"), 400
        
        current_user_id = get_jwt_identity()
        certificate = Certificate.query.get(certificate_id)

        if not certificate:
            return generate_response(False, None, "Certificate not found"), 404

        # Check if the current user is the certificate owner
        if current_user_id != certificate.user_id:
            return generate_response(False, None, "Unauthorized to request opt-in for the certificate"), 403

        sender_user = User.query.filter_by(id=current_user_id).first()
        if not sender_user:
            return generate_response(False, None, "Sender User does not exist"), 400
        
        results = algorand.opt_in_asset(
            sender_address=sender_user.account_address,
            password=password,
            username=sender_user.username,
            nft_id=certificate.nft_id
        )

        if results is None:
            return generate_response(False, None, "Error optin for asset"), 500
        
        # Update certificate status to "Pending"
        certificate.is_approved = ApprovalStatus.PENDING
        db.session.commit()
        
        certificate_info = {
            'id': certificate.id,
            'title': certificate.title,
            'score': certificate.score,
            'issued_date': certificate.issued_date,
            'staff_id': certificate.staff_id,
            'user_id': certificate.user_id,
            'nft_id': certificate.nft_id,
            'challenge_id': certificate.challenge_id,
            'is_approved': certificate.is_approved.value,
            'ipfs_hash': certificate.ipfs_hash
        }

        return generate_response(True, certificate_info, "Opt-in request sent successfully"), 200

    except Exception as e:
        return generate_response(False, None, f"Error sending opt-in request: {e}"), 500

@certificate_bp.route('/certificates/optin/approve/<int:certificate_id>', methods=['PUT'])
@jwt_required()
def approve_optin(certificate_id):
    try:
        password = request.json.get('password')

        if not password:
            return generate_response(False, None, "Missing required fields"), 400
        

        current_user_id = get_jwt_identity()
        certificate = Certificate.query.get(certificate_id)

        if not certificate:
            return generate_response(False, None, "Certificate not found"), 404

        # Check if the current user is the issuer
        if current_user_id != certificate.staff_id:
            return generate_response(False, None, "Unauthorized to approve opt-in for the certificate"), 403

        sender_user = User.query.filter_by(id=current_user_id).first()
        if not sender_user:
            return generate_response(False, None, "Sender User does not exist"), 400

        receiving_user = User.query.filter_by(id=certificate.user_id).first()
        if not receiving_user:
            return generate_response(False, None, "Receiving User does not exist"), 400

     
        # Perform opt-in for the asset
        results = algorand.transfer_asset(
            sender_address=sender_user.account_address,
            password=password,
            username=sender_user.username,
            nft_id=certificate.nft_id,
            receiver_address=receiving_user.account_address
        )

        if results is None:
            return generate_response(False, None, "Error transfering asset for asset"), 500
        
        # Update certificate status to "Pending"
        certificate.is_approved = ApprovalStatus.APPROVED
        db.session.commit()

        certificate_info = {
            'id': certificate.id,
            'title': certificate.title,
            'score': certificate.score,
            'issued_date': certificate.issued_date,
            'staff_id': certificate.staff_id,
            'user_id': certificate.user_id,
            'nft_id': certificate.nft_id,
            'challenge_id': certificate.challenge_id,
            'is_approved': certificate.is_approved.value,
            'ipfs_hash': certificate.ipfs_hash
        }

        return generate_response(True, certificate_info, "Transfer asset request approved successfully"), 200

    except Exception as e:
        return generate_response(False, None, f"Error approving asset request: {e}"), 500



@certificate_bp.route('/certificates', methods=['GET'])
@jwt_required()
def get_certificates():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return generate_response(False, None, "User not found"), 404
        if current_user.role == UserRole.ISSUER:
            # If the user is an Issuer, get all certificates with staff_id
            certificates = Certificate.query.filter_by(staff_id=current_user_id).all()
        else:
            # If the user is not an Issuer, get all certificates with user_id
            certificates = Certificate.query.filter_by(user_id=current_user_id).all()


        certificate_list = []

        for certificate in certificates:
            certificate_info = {
                'id': certificate.id,
                'title': certificate.title,
                'score': certificate.score,
                'issued_date': certificate.issued_date,
                'staff_id': certificate.staff_id,
                'user_id': certificate.user_id,
                'nft_id': certificate.nft_id,
                'challenge_id': certificate.challenge_id,
                'is_approved': certificate.is_approved.value,
                'ipfs_hash': certificate.ipfs_hash
            }
            certificate_list.append(certificate_info)

        return generate_response(True, certificate_list, "Get certificates successfully"), 200

    except Exception as e:
        return generate_response(False, None, f"Error retrieving certificates: {e}"), 500
    

# @certificate_bp.route('/certificates/optin/reject/<int:certificate_id>', methods=['PUT'])
# @jwt_required()
# def reject_optin(certificate_id):
#     try:
#         current_user_id = get_jwt_identity()
#         certificate = Certificate.query.get(certificate_id)

#         if not certificate:
#             return jsonify({"message": "Certificate not found"}), 404

#         # Check if the current user is the issuer
#         if current_user_id != certificate.staff_id:
#             return jsonify({"message": "Unauthorized to reject opt-in for the certificate"}), 403

#         # Update the certificate status or perform any other desired actions
#         # For example, you may want to set the status to rejected and notify the trainee

#         return jsonify({"message": "Opt-in request rejected successfully"}), 200

#     except Exception as e:
#         return jsonify({"message": f"Error rejecting opt-in request: {e}"}), 500

# @certificate_bp.route('/certificates/optout/<int:certificate_id>', methods=['PUT'])
# @jwt_required()
# def opt_out_certificate(certificate_id):
#     try:
#         current_user_id = get_jwt_identity()
#         certificate = Certificate.query.get(certificate_id)

#         if not certificate:
#             return jsonify({"message": "Certificate not found"}), 404

#         # Check if the current user is the certificate owner
#         if current_user_id != certificate.user_id:
#             return jsonify({"message": "Unauthorized to opt-out of the certificate"}), 403

#         # Update the certificate status or perform any other desired actions
#         # For example, you may want to set the status to revoked and notify the issuer

#         return jsonify({"message": "Opt-out successful"}), 200

#     except Exception as e:
#         return jsonify({"message": f"Error opting out of the certificate: {e}"}), 500
