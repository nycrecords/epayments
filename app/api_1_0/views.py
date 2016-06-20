from flask import jsonify, abort, request
from . import api_1_0 as api
from ..utils import make_public_order
# from .constants import orders
from ..models import Order
from datetime import date, timedelta, datetime


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['POST', 'GET'])
def get_orders():
	if request.form:
		date_received_start = request.form["date_received_start"]
		date_received_end = request.form["date_received_end"]
		if (len(date_received_start) > 0) or (len(date_received_end.length) > 0):
			orders = [order.serialize for order in Order.query.filter(Order.datereceived>=date_received_start, Order.datereceived<=date_received_end).all()]
			print orders
			return jsonify(orders=orders)
	else:
		yesterday = (date.today() - timedelta(6)).strftime('%-m/%-d/%Y') + " 0:00:00" #6/14/2016 0:00:00
		orders = [order.serialize for order in Order.query.filter(Order.datereceived==yesterday).all()]
		print orders
		return jsonify(orders=orders)


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
	orders=[order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    	if len(orders) == 0:
        	abort(404)
	return jsonify(orders)
