from flask import Flask
from import.import_xml import import_xml

app = Flask(__name__)
app.register_blueprint(import_xml)
