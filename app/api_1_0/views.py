import six
from flask import jsonify, abort
from flask.ext.sqlalchemy import SQLAlchemy
from . import api_1_0 as api
from .. import db


@api.route('/orders', methods=['GET'])
def get_orders():
	return jsonify({'orders': [make_public_order(order) for order in orders]})


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order():
	order = [order for order in orders if order['SubOrderNo'] == order_id]
	if len(order) == 0:
		abort(404)
	return jsonify({'order': make_public_order(order[0])})