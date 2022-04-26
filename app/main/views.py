import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app

from app.main import main
from app.main.utils import allowed_file, import_xml
from app.import_utils import import_from_api


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    return render_template('index.html')


@main.route('/import', methods=['GET', 'POST'])
def import_tar():
    """Import Orders into the database from the tar file."""
    if request.method == 'POST':
        file_ = request.files['file']
        if file_ and allowed_file(file_.filename):
            actual_filename = 'DOR-{date}.tar'.format(date=datetime.now().strftime('%Y-%m-%d'))
            filename = os.path.join(current_app.config['LOCAL_FILE_PATH'], actual_filename)
            file_.save(filename)
            import_xml(filename)
            return redirect(url_for('main.index'))

        start_date = request.form["start-date"]
        end_date = request.form["end-date"]
        if start_date and end_date:
            import_from_api(start_date, end_date)
    return render_template('main/import.html')
