# from app.constants import ALLOWED_EXTENSIONS
from flask import current_app
import os
from app.utils import import_xml_folder
import tarfile
from datetime import datetime
from shutil import rmtree


ALLOWED_EXTENSIONS = frozenset(['tar', 'xml'])


def allowed_file(filename):
    """
    Determine if files is allowed to be uploaded.

    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def import_xml(filename, sftp=False):
    """ 
    Import XML File(s).
    :param filename: File to import
    :return: Bool
    """
    data_path = current_app.config['TAR_DATA_PATH'] + 'temp' if sftp else current_app.config['TAR_DATA_PATH']

    directory_name = make_directory(filename, data_path)

    import_xml_folder(path=os.path.join(directory_name, data_path))

    rmtree(os.path.join(directory_name))


def make_directory(filename, data_path):
    """
    Create the directory to hold the XML files      
    :param filename: 
    :return: the directory name 
    """
    directory_name = os.path.join(current_app.config['LOCAL_FILE_PATH'], datetime.now().strftime('%Y-%m-%d_%H-%M'))
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    with tarfile.open(filename) as tar:
        subdir_and_files = [
            tarinfo for tarinfo in tar.getmembers()
            if tarinfo.name.startswith(data_path)
        ]
        tar.extractall(path=directory_name, members=subdir_and_files)

    return directory_name
