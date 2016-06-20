from flask import jsonify, abort, request
from . import api_1_0 as api
from ..utils import make_public_order
# from .constants import orders
from ..models import Order
from datetime import date, timedelta


@api.route('/orders', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/', methods=['GET'])
def get_orders():
	# datereceivedstart = request.form['datereceivedstart']
	# datereceivedend = request.form['datereceivedend']
	# print 'datereceivedstart:', datereceivedstart
	# if (datereceivedstart.length > 0) or (datereceivedend.length) > 0:
	# 	return jsonify(orders=[order.serialize for order in Order.query.filter_by(datereceived>=datereceivedstart, datereceived<=datereceivedend).all()])
	# else:
	yesterday = (date.today() - timedelta(6)).strftime('%-m/%-d/%Y') + " 0:00:00"
    	return jsonify(orders=[order.serialize for order in Order.query.filter(Order.datereceived==yesterday).all()])


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
	orders=[order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    	if len(orders) == 0:
        	abort(404)
    	return jsonify(orders)
