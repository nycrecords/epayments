import six
from flask import Flask, jsonify, abort, request, make_response, url_for, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from crossdomain import crossdomain

import os
from ..app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.sqlalchemy import SQLAlchemy

# app = Flask(__name__, static_url_path="/build")

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/brandontang/doris-epayments/epayments/testepayments.db'
db = SQLAlchemy(app)
manager = Manager(app)

# Connecting to DB
# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/brandontang/doris-epayments/epayments/testepayments.db'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)


# app/main directory
# class Orders(db.Model):
#     __tablename__ = 'orders'
#     SubOrderNo = db.Column(db.Integer, primary_key=True)

# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

# def make_public_order(order):
# 	new_order = {}
# 	for field in order:
# 		if field == 'SubOrderNo':
# 			new_order['uri'] = url_for('get_order', order_id=order['SubOrderNo'], _external=True)
# 		else:
# 			new_order[field] = order[field]

# 	return new_order

# @app.route('/epayments/api/v1.0/orders', methods=['GET'])
# @crossdomain(origin='*')
# def get_orders():
# 	# ordernumber = request.form['ordernumber']
# 	# subordernumber = request.form['subordernumber']
# 	# ordertype = request.form['ordertype']
# 	# name = request.form['name']
# 	# date = request.form['date']
# 	return jsonify({'orders': [make_public_order(order) for order in orders]})

# @app.route('/epayments/api/v1.0/orders/<int:order_id>', methods=['GET'])
# @crossdomain(origin='*')
# def get_order():
# 	order = [order for order in orders if order['SubOrderNo'] == order_id]
# 	if len(order) == 0:
# 		abort(404)
# 	return jsonify({'order': make_public_order(order[0])})

# orders = Orders.query.all()

orders = [
  {
    "OrderNo": 9046420448,
    "ClientAgencyName": "Death Cert",
    "ShipToName": "Mark Reichard",
    "ShipToStreetAdd": "23307 Los Codona Ave.",
    "ShipToStreetAdd2": "",
    "ShipToCity": "Torrance",
    "ShipToState": "CA",
    "ShipToZipCode": "90505",
    "ShipToCountry": "USA",
    "ShipToPhone": "310-710-0413",
    "CustomerEmail": "mreichard@socal.rr.com",
    "ShippingInstructions": "",
    "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046401977|LASTNAME|Reichard|FIRSTNAME|Sarah|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|September|DAY|16|YEAR|1899|ADD_COMMENT| Born abt. 1899.  Trying to establish relationship|CERTIFICATE_NUMBER|26473|BOROUGH|MANHATTAN,",
    "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    "DateReceived": "2014-01-24 00:00:00",
    "BillingName": "Mark Reichard",
    "DateLastModified": "1/23/2014 3:10:21 AM",
    "SubOrderNo": 9046401977,
    "ClientID": "10000182"
  },
  {
    "OrderNo": 9046420448,
    "ClientAgencyName": "Birth Cert",
    "ShipToName": "Mark Reichard",
    "ShipToStreetAdd": "23307 Los Codona Ave.",
    "ShipToStreetAdd2": "",
    "ShipToCity": "Torrance",
    "ShipToState": "CA",
    "ShipToZipCode": "90505",
    "ShipToCountry": "USA",
    "ShipToPhone": "310-710-0413",
    "CustomerEmail": "mreichard@socal.rr.com",
    "ShippingInstructions": "",
    "ClientsData": "ClientID|10000182|ClientAgencyName|Department of Record|OrderNo|9046415827|LASTNAME|Reichard|FIRSTNAME|Hugo|MIDDLENAME|G.|RELATIONSHIP|grand nephew|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|31|YEAR|1898|ADD_COMMENT| born abt. 1898.  Trying to establish relationship.|CERTIFICATE_NUMBER|25|BOROUGH|BROOKLYN,|",
    "ConfirmationMessage": "ClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046365465\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sigmond\nMiddle name:             (Left Blank)\n\nMonth:                   March\nDay:                     26\nYear:                    1905\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born 11-13-1904 in Manhattan, Cert. #53632\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      10272\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046386371\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Morveve\nMiddle name:             (Left Blank)\n\nMonth:                   June\nDay:                     22\nYear:                    1902\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born in 1901.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      18654\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046401977\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Sarah\nMiddle name:             (Left Blank)\n\nMonth:                   September\nDay:                     16\nYear:                    1899\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      Born abt. 1899.  Trying to establish relationship\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      26473\n\n--------------------------------------------------------------------------------\n\n\nClientID:                10000182\nClientAgencyName:        Department of Record\nOrder Number:            9046415827\nItems:                   DOR202      \n\nLast name:               Reichard\nFirst name:              Hugo\nMiddle name:             G.\n\nMonth:                   December\nDay:                     31\nYear:                    1898\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          (Left Blank)\n\nAge at Death:            (Left Blank)\n\nAdditional Comments:      born abt. 1898.  Trying to establish relationship.\n\nBorough(s):              BROOKLYN\n\n--------------------------------------------------------------------------------\nRelationship to person:  grand nephew\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\nCertificate Number:      25\n\n--------------------------------------------------------------------------------",
    "DateReceived": "2014-01-24 00:00:00",
    "BillingName": "Mark Reichard",
    "DateLastModified": "1/23/2014 3:10:21 AM",
    "SubOrderNo": 9046415827,
    "ClientID": "10000182"
  }
]

if __name__ == '__main__':
    manager.run()

# if __name__ == '__main__':
#     app.run(debug=True)
