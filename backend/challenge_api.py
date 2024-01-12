from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models import Challenge, Certificate
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from models import db

challenge_bp = Blueprint('challenge', __name__)

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

        return jsonify({'data': challenge_list, "message": "get all challenges successfully."}), 200

    except Exception as e:
        return jsonify({"message": f"Error retrieving challenges: {e}", "data": ""}), 500


@challenge_bp.route('/challenges/<int:challenge_id>', methods=['GET'])
def get_challenge_by_id(challenge_id):
    try:
        challenge = Challenge.query.get(challenge_id)

        if not challenge:
            return jsonify({"message": "Challenge not found", "data": ""}), 404

        challenge_info = {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'week_number': challenge.week_number,
            "batch_number": challenge.batch_number,
            'certificates': [certificate.id for certificate in challenge.certificates]
        }

        return jsonify(challenge_info), 200

    except Exception as e:
        return jsonify({"message": f"Error retrieving challenge: {e}", "data": ""}), 500
    
@challenge_bp.route('/challenges', methods=['POST'])
@jwt_required()
def create_challenge():
    try:
        title = request.json.get('title')
        description = request.json.get('description')
        week_number = request.json.get('week_number')
        batch_number = request.json.get('batch_number')
        if not title or not description or week_number  < 0:
            return jsonify({"message": "Missing required fields", "data": ""}), 400

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
            return jsonify({"message": "Error fetching created challenge", "data": ""}), 500

        challenge_info = {
            'id': created_challenge.id,
            'title': created_challenge.title,
            'description': created_challenge.description,
            'week_number': created_challenge.week_number,
            'batch_number': created_challenge.batch_number,
            'certificates': [certificate.id for certificate in created_challenge.certificates]
        }


        return jsonify({"message": "Challenge created successfully", "data": challenge_info}), 201

    except Exception as e:
        return jsonify({"message": f"Error creating challenge: {e}", "data": ""}), 500

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
            return jsonify({"message": "Challenge not found", "data": ""}), 404

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

        return jsonify({"message": "Challenge updated successfully", "data": challenge_info}), 200

    except Exception as e:
        return jsonify({"message": f"Error updating challenge: {e}", "data": ""}), 500



@challenge_bp.route('/challenges/<int:challenge_id>', methods=['DELETE'])
@jwt_required()
def delete_challenge(challenge_id):
    try:
        challenge = Challenge.query.get(challenge_id)

        if not challenge:
            return jsonify({"message": "Challenge not found"}), 404

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


        return jsonify({"message": "Challenge deleted successfully", "data": challenge_info}), 200

    except Exception as e:
        return jsonify({"message": f"Error deleting challenge: {e}", "data": ""}), 500