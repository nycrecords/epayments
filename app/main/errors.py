from flask import make_response
from . import main

@main.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
