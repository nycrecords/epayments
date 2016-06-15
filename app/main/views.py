from flask import render_template, redirect, request, url_for
from . import main
from .. import db
from ..models import Order


@main.route('/')
def index():
    """Default route for the application."""
    return render_template('index.html')

@main.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
