from flask import jsonify, abort, request
from datetime import date, timedelta, datetime
from sqlalchemy import func
from . import api_1_0 as api
from ..models import Order
from ..utils import make_public_order


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['POST', 'GET'])
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with the previous day's date.
    """
    if request.form:
        order_number = str(request.form["order_number"])
        suborder_number = str(request.form["suborder_number"])
        order_type = request.form["order_type"]
        billing_name = str(request.form["billing_name"])
        date_received_start = request.form["date_received_start"]
        date_received_end = request.form["date_received_end"]
        orders = get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start,
                                      date_received_end)
        return jsonify(orders=orders)
    else:
        yesterday = date.today() - timedelta(33)
        orders = [order.serialize for order in Order.query.filter_by(datereceived=yesterday).all()]
        return jsonify(orders=orders)


def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start,
                         date_received_end):
    """Filters orders by fields received."""
    yesterday = date.today() - timedelta(33)
    if len(date_received_start) < 1:
        date_received_start = yesterday
    if len(date_received_end) < 1:
        date_received_end = yesterday
    orders = Order.query.filter(Order.datereceived >= date_received_start, Order.datereceived <= date_received_end)
    if len(order_number) != 0:
        orders = orders.filter(Order.clientid == order_number)
    if len(suborder_number) != 0:
        orders = orders.filter(Order.suborderno == suborder_number)
    if len(order_type) != 4 and order_type != 'All' and order_type != 'multitems':
        orders = orders.filter(Order.clientagencyname == order_type)
    if len(billing_name) != 0:
        orders = orders.filter(func.lower(Order.billingname).contains(func.lower(billing_name)))
    order_list = [order.serialize for order in orders]
    return order_list


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    orders = [order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    if len(orders) == 0:
        abort(404)
    return jsonify(orders)
