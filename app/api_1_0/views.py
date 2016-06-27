from flask import jsonify, abort, request
from . import api_1_0 as api
from ..utils import make_public_order
# from .constants import orders
from ..models import Order
from datetime import date, timedelta, datetime
from sqlalchemy import func


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['POST', 'GET'])
def get_orders():
	if request.form:
		order_number = str(request.form["order_number"])
		suborder_number = str(request.form["suborder_number"])
		order_type = request.form["order_type"]
		billing_name = str(request.form["billing_name"])
		date_received_start = request.form["date_received_start"]
		date_received_end = request.form["date_received_end"]
		# date_received_start = (datetime.strptime(str(date_received_start), '%m/%d/%Y')).strftime('%Y/%-m/%-d')
		# date_received_end = (datetime.strptime(str(date_received_end), '%m/%d/%Y')).strftime('%Y/%-m/%-d')
		orders = get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start, date_received_end)
		return jsonify(orders=orders)
	else:
		yesterday = date.today() - timedelta(11)
		orders = [order.serialize for order in Order.query.filter_by(datereceived=yesterday).all()]
		return jsonify(orders=orders)


def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start, date_received_end):
	yesterday = date.today() - timedelta(11)
	if len(date_received_start) < 1:
		date_received_start = yesterday
	if len(date_received_end) < 1:
		date_received_end = yesterday
	orders = Order.query.filter(Order.datereceived>=date_received_start, Order.datereceived<=date_received_end)
	if len(order_number) != 0:
		orders = orders.filter(Order.clientid==order_number)
	if len(suborder_number) != 0:
		orders = orders.filter(Order.suborderno==suborder_number)
	if len(order_type) != 4:
		orders = orders.filter(Order.clientagencyname==order_type)
	print billing_name
	if len(billing_name) != 0:
		orders = orders.filter(func.lower(Order.billingname).contains(func.lower(billing_name)))
	order_list = [order.serialize for order in orders]
	return order_list


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
	orders=[order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    	if len(orders) == 0:
        	abort(404)
	return jsonify(orders)
