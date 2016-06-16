from flask import jsonify, abort
from . import api_1_0 as api
from ..utils import make_public_order
# from .constants import orders
from ..models import Order
from .. import db
from . import api_1_0


@api.route('/orders', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/', methods=['GET'])
def get_orders():
    return jsonify(orders=[order.serialize for order in Order.query.all()])


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = [order for order in orders if order['SubOrderNo'] == order_id]
    if len(order) == 0:
        abort(404)
    return jsonify({'order': make_public_order(order[0])})
