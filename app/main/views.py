from flask import render_template, redirect, request, url_for
from . import main
from .. import db
from ..models import Order


@main.route('/')
def index():
    """Default route for the application."""
    return render_template('index.html')
