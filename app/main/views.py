from flask import render_template, make_response, jsonify, redirect, url_for, request, current_app
from werkzeug.utils import secure_filename
from app.main import main
from app.main.utils import allowed_file, import_xml
import os
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    # curl -k 'https://dorisorders-stg.csc.nycnet/dorisorders/api/system/dorfiles?start=2022-02-24T00:00:00&end=2022-02-25T00:00:00' --header 'DO-Auth-Key: 4a51fbce615443edb6ca4e3f2c3622ad'

    import requests
    from app.utils import import_file
    from xml.etree import ElementTree
    headers = {
        "DO-Auth-Key": "4a51fbce615443edb6ca4e3f2c3622ad"
    }
    params = {
        "start": "2022-02-24T00:00:00",
        "end": "2022-02-25T00:00:00"
        # "start": "2022-03-28T00:00:00",
        # "end": "2022-03-29T00:00:00"
    }
    response = requests.get("https://dorisorders-stg.csc.nycnet/dorisorders/api/system/dorfiles", headers=headers, params=params, verify=False)
    files_list = response.json()["files"]
    for item in files_list or []:
        resp = requests.get(item["xmlFile"]["url"], verify=False)
        tree = ElementTree.fromstring(resp.text)
        date_submitted = datetime.strptime(item["xmlFile"]["name"].split("DOR")[1].split("_")[0], "%Y%m%d%H%M%S")
        # import_file(tree, date_submitted)
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
    return render_template('main/import.html')
