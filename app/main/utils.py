from app.constants import ALLOWED_EXTENSIONS
from flask import current_app
import os
from app.utils import import_xml_folder
import tarfile
from datetime import datetime


def allowed_file(filename):
    """
    Determine if file is allowed to be uploaded.

    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def import_xml(filename):
    """
    Import XML File(s).
    :param filename: File to import
    :return: Bool
    """
    directory_name = os.path.join(current_app.config['LOCAL_FILE_PATH'], datetime.now().strftime('%Y-%m-%d_%H-%M'))
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    with tarfile.open(filename) as tar:
        subdir_and_files = [
            tarinfo for tarinfo in tar.getmembers()
            if tarinfo.name.startswith("data/files/DOR/")
            ]
        tar.extractall(path=directory_name, members=subdir_and_files)

    import_xml_folder(path=os.path.join(directory_name, 'data/files/DOR/'))

