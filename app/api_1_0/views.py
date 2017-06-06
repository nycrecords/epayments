from flask import jsonify, abort, request
import datetime
from datetime import date, datetime, timedelta
from sqlalchemy import func
from .import api_1_0 as api
from ..models import Orders, Customer, BirthSearch, BirthCertificate, MarriageSearch, MarriageCertificate, \
                     DeathSearch, DeathCertificate, PhotoGallery, PhotoTax, PropertyCard, StatusTracker


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})