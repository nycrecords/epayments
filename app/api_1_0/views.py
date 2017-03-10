from flask import jsonify, abort, request
from datetime import datetime, timedelta, date
from sqlalchemy import func
from app.api_1_0 import api_1_0 as api
from app.models import Order
from app.constants import (
    VITAL_RECORDS_ORDERS,
    PHOTO_ORDERS,
    MULTIPLE_ORDERS,
    VITAL_RECORDS_PHOTOS_ORDER,
    MULTIPLE_ITEMS_IN_CART
)


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
        today = date.today()
        orders = [order.serialize for order in Order.query.filter_by(date_received=today).all()]
        return jsonify(orders=orders)


def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, date_received_start,
                         date_received_end):
    """
    Search for orders based on provided filter categories
    :param order_number: Order Number from CityPay
    :param suborder_number: Sub Order Number from DOITT EPayments
    :param order_type: Must be in list of
    :param billing_name: Name of Customer
    :param date_received_start: Start for Date Range of Orders Received
    :param date_received_end: End for Date Range of Orders Received
    :return: List of orders
    """
    today = date.today()
    if len(date_received_start) < 1:
        date_received_start = today
    if len(date_received_end) < 1:
        date_received_end = today
    orders = Order.query.filter(Order.date_received >= date_received_start, Order.date_received <= date_received_end)
    if len(order_number) != 0:
        orders = orders.filter(Order.order_no == order_number)
    if len(suborder_number) != 0:
        orders = orders.filter(Order.sub_order_no == suborder_number)
    if len(billing_name) != 0:
        orders = orders.filter(func.lower(Order.billing_name).contains(func.lower(billing_name)))
    if len(order_type) != 4 and order_type != 'Order Type' and order_type not in MULTIPLE_ORDERS:
        orders = orders.filter(Order.client_agency_name == order_type)
    elif order_type == MULTIPLE_ITEMS_IN_CART:
        orders = [order for order in orders if len(order.order_types.split(',')) > 1]
    elif order_type == VITAL_RECORDS_PHOTOS_ORDER:
        orders = [order for order in orders if
                  not set(order.order_types.split(',')).isdisjoint(VITAL_RECORDS_ORDERS) and not set(
                      order.order_types.split(
                          ',')).isdisjoint(PHOTO_ORDERS)]
    order_list = [order.serialize for order in orders]
    return order_list


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    orders = [order.serialize for order in Order.query.filter_by(clientid=order_id).all()]
    if len(orders) == 0:
        abort(404)
    return jsonify(orders)
