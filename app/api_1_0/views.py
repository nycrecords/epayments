import six
from flask import jsonify, abort
from flask.ext.sqlalchemy import SQLAlchemy
from ..utils.crossdomain import crossdomain
from . import api_1_0 as api
from .. import db

@api.route('/orders', methods=['GET'])
@crossdomain(origin='*')
def get_orders():
	return jsonify({'orders': [make_public_order(order) for order in orders]})

@api.route('/epayments/api/v1.0/orders/<int:order_id>', methods=['GET'])
@crossdomain(origin='*')
def get_order():
	order = [order for order in orders if order['SubOrderNo'] == order_id]
	if len(order) == 0:
		abort(404)
	return jsonify({'order': make_public_order(order[0])})
