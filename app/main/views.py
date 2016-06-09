import six
from flask import Flask, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
from crossdomain import crossdomain
from . import main
from .. import db

@main.route('/epayments/api/v1.0/orders', methods=['GET'])
@crossdomain(origin='*')
def get_orders():
	# ordernumber = request.form['ordernumber']
	# subordernumber = request.form['subordernumber']
	# ordertype = request.form['ordertype']
	# name = request.form['name']
	# date = request.form['date']
	return jsonify({'orders': [make_public_order(order) for order in orders]})

@main.route('/epayments/api/v1.0/orders/<int:order_id>', methods=['GET'])
@crossdomain(origin='*')
def get_order():
	order = [order for order in orders if order['SubOrderNo'] == order_id]
	if len(order) == 0:
		abort(404)
	return jsonify({'order': make_public_order(order[0])})
