from flask import jsonify, abort
from . import api_1_0 as api
from ..utils import make_public_order
from .constants import orders
# from ..models import Order


@api.route('/orders', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/', methods=['GET'])
def get_orders():
	# allOrders = Order.query.all()
	# print allOrders
    return jsonify({'orders': [make_public_order(order) for order in orders]})


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = [order for order in orders if order['SubOrderNo'] == order_id]
    if len(order) == 0:
        abort(404)
    return jsonify({'order': make_public_order(order[0])})
