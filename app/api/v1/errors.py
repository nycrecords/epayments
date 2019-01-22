from flask import make_response, jsonify

from app.api.v1 import api_v1 as api


@api.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@api.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)
