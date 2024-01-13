from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import Challenge
from flask import Blueprint
from models import db

challenge_bp = Blueprint('challenge', __name__)

def generate_response(is_success, value=None, error=None):
    response = {
        "isSuccess": is_success,
        "value": value,
        "error": error
    }
    return jsonify(response)

@challenge_bp.route('/challenges', methods=['GET'])
def get_challenges():
    try:
        challenges = Challenge.query.all()
        challenge_list = []

        for challenge in challenges:
            challenge_info = {
                'id': challenge.id,
                'title': challenge.title,
                'description': challenge.description,
                'week_number': challenge.week_number,
                'batch_number': challenge.batch_number,
                'certificates': [certificate.id for certificate in challenge.certificates]
            }
            challenge_list.append(challenge_info)

        return generate_response(True, challenge_list, None), 200

    except Exception as e:
        return generate_response(False, None, f"Error retrieving challenges: {e}"), 500

@challenge_bp.route('/challenges/<int:challenge_id>', methods=['GET'])
def get_challenge_by_id(challenge_id):
    try:
        challenge = Challenge.query.get(challenge_id)

        if not challenge:
            return generate_response(False, None, "Challenge not found"), 404

        challenge_info = {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'week_number': challenge.week_number,
            "batch_number": challenge.batch_number,
            'certificates': [certificate.id for certificate in challenge.certificates]
        }

        return generate_response(True, challenge_info, None), 200

    except Exception as e:
        return generate_response(False, None, f"Error retrieving challenge: {e}"), 500
    
@challenge_bp.route('/challenges', methods=['POST'])
@jwt_required()
def create_challenge():
    try:
        title = request.json.get('title')
        description = request.json.get('description')
        week_number = request.json.get('week_number')
        batch_number = request.json.get('batch_number')
        if not title or not description or week_number  < 0:
            return generate_response(False, None, "Missing required fields"), 400

        new_challenge = Challenge(
            title=title,
            description=description,
            week_number=week_number,
            batch_number=batch_number
        )

        db.session.add(new_challenge)
        db.session.commit()

        # Fetch the details of the newly created challenge
        created_challenge = Challenge.query.get(new_challenge.id)

        if not created_challenge:
            return generate_response(False, None, "Error fetching created challenge"), 500

        challenge_info = {
            'id': created_challenge.id,
            'title': created_challenge.title,
            'description': created_challenge.description,
            'week_number': created_challenge.week_number,
            'batch_number': created_challenge.batch_number,
            'certificates': [certificate.id for certificate in created_challenge.certificates]
        }

        return generate_response(True, challenge_info, None), 201

    except Exception as e:
        return generate_response(False, None, f"Error creating challenge: {e}"), 500

@challenge_bp.route('/challenges/<int:challenge_id>', methods=['PUT'])
@jwt_required()
def update_challenge(challenge_id):
    try:
        title = request.json.get('title')
        description = request.json.get('description')
        week_number = request.json.get('week_number')
        batch_number = request.json.get("batch_number")

        challenge = Challenge.query.get(challenge_id)

        if not challenge:
            return generate_response(False, None, "Challenge not found"), 404

        challenge.title = title if title else challenge.title
        challenge.description = description if description else challenge.description
        challenge.week_number = week_number if week_number else challenge.week_number
        challenge.batch_number = batch_number if batch_number else challenge.batch_number

        db.session.commit()

        challenge_info = {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'week_number': challenge.week_number,
            "batch_number": challenge.batch_number,
            'certificates': [certificate.id for certificate in challenge.certificates]
        }

        return generate_response(True, challenge_info, None), 200

    except Exception as e:
        return generate_response(False, None, f"Error updating challenge: {e}"), 500

@challenge_bp.route('/challenges/<int:challenge_id>', methods=['DELETE'])
@jwt_required()
def delete_challenge(challenge_id):
    try:
        challenge = Challenge.query.get(challenge_id)

        if not challenge:
            return generate_response(False, None, "Challenge not found"), 404

        # Optionally, you can add additional checks here (e.g., user permission)

        db.session.delete(challenge)
        db.session.commit()

        challenge_info = {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'week_number': challenge.week_number,
            "batch_number": challenge.batch_number,
            'certificates': [certificate.id for certificate in challenge.certificates]
        }

        return generate_response(True, challenge_info, None), 200

    except Exception as e:
        return generate_response(False, None, f"Error deleting challenge: {e}"), 500
