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
		date_received_start = (datetime.strptime(str(date_received_start), '%m/%d/%Y')).strftime('%Y/%-m/%-d')
		date_received_end = (datetime.strptime(str(date_received_end), '%m/%d/%Y')).strftime('%Y/%-m/%-d')
		if (len(str(date_received_start)) > 0) or (len(str(date_received_end.length)) > 0):
			orders = get_orders_by_date_range(date_received_start, date_received_end)
			return jsonify(orders=orders)
	else:
		yesterday = date.today() - timedelta(8)
		orders = [order.serialize for order in Order.query.filter_by(datereceived=yesterday).all()]
		return jsonify(orders=orders)


def get_orders_by_date_range(date_received_start, date_received_end):
	orders = Order.query.filter(Order.datereceived>=date_received_start, Order.datereceived<=date_received_end)
	order_list = [order.serialize for order in orders]
	return order_list


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
	orders=[order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    	if len(orders) == 0:
        	abort(404)
	return jsonify(orders)
