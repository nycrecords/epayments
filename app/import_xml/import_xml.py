
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


import_xml = Blueprint('import', __name__,
                       template_folder='templates')


@import_xml.route('/', defaults={'page': 'index'})
@import_xml.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)
