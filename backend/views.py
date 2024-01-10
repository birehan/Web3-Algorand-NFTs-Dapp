from flask import Blueprint, jsonify, request
import json
import logging

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@main_bp.route('/api/v1', methods=['POST'])
def index():
    data = request.json
    response = {
        "data" : None,
        "error" : None
    }
    statusCode = 404
    try:
        logging.info(f"data: {data}")
        answer = "sucess"

        logging.info(f"response: {answer}")
        response["data"] = answer
        statusCode = 200
    except Exception as error:
        logging.error(error)
        response['error'] = {
        'message': f"{error}"
        }
        statusCode = 404
    return jsonify(response), statusCode

@main_bp.route('/', methods=['GET'])
def another_route():
    response = {
        "data": None,
        "error": None
    }
    statusCode = 404
    try:      
        response["data"] = "server working success"
        statusCode = 200
    except Exception as error:
        response['error'] = {'message': f"{error}"}
        statusCode = 404
    return jsonify(response), statusCode