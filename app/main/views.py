from flask import render_template, make_response, jsonify
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    return render_template('index.html')


@main.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
