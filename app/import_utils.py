import os
from datetime import datetime
from time import localtime, strftime
from xml.etree import ElementTree

import requests
from dateutil import parser
from flask import current_app

from app.email_utils import send_email
from app.utils import import_file


def import_from_api(start_date, end_date):
    headers = {
        "DO-Auth-Key": current_app.config["IMPORT_API_KEY"]
    }

    start = parser.parse(start_date).isoformat()
    end = parser.parse(end_date).isoformat()
    params = {
        "start": start,
        "end": end,
    }
    response = requests.get(current_app.config["IMPORT_URL"], headers=headers, params=params, verify=False)
    files_list = response.json()["files"]
    msg_body = []
    for item in files_list or []:
        resp = requests.get(item["xmlFile"]["url"], verify=False)
        tree = ElementTree.fromstring(resp.text)
        date_submitted = datetime.strptime(item["xmlFile"]["name"].split("DOR")[1].split("_")[0], "%Y%m%d%H%M%S")
        if "fileUploads" in item:
            uploads_list = item['fileUploads']

            for upload in uploads_list:
                r = requests.get(upload["files"][0]["url"])
                directory = os.path.join(current_app.config["NO_AMENDS_FILE_PATH"], upload["orderNo"])
                os.makedirs(directory, exist_ok=True)

                file = os.path.join(directory, upload["files"][0]["name"])

                with open(file, "wb") as f:
                    f.write(r.content)

        if import_file(tree, date_submitted):
            msg_body.append(f"Successfully imported {item['xmlFile']['name']}")
        else:
            msg_body.append(f"Failed to import {item['xmlFile']['name']}")
    send_email(
        current_app.config["IMPORT_MAIL_TO"].split(","),
        f"ePayments Import {strftime('%Y-%m-%d %H:%M:%S', localtime())}",
        "email_templates/import_status",
        msg_body=msg_body,
    )
