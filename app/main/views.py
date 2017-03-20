from flask import render_template, make_response, jsonify, redirect, url_for, request, current_app
from werkzeug.utils import secure_filename
from app.main import main
from app.main.utils import allowed_file, import_xml as import_file
import os
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    return render_template('index.html')


@main.route('/import', methods=['GET', 'POST'])
def import_xml():
    """Import Orders into the database."""
    if request.method == 'POST':
        file_ = request.files['file']
        if file_ and allowed_file(file_.filename):
            actual_filename = secure_filename(
                file_.filename.replace('.', '-' + datetime.now().strftime('%Y-%m-%d') + '.'))
            filename = os.path.join(current_app.config['LOCAL_FILE_PATH'], actual_filename)
            file_.save(filename)
            import_file(filename)
            return redirect(url_for('main.index'))
    return render_template('main/import.html')
