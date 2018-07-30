from datetime import date
from flask import jsonify, abort, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from app.api_1_0 import api_1_0 as api

from app.api_1_0.utils import (
    update_status,
    get_orders_by_fields,
    _print_orders,
    _print_large_labels,
    _print_small_labels,
    update_tax_photo,
    generate_csv
)
from app.constants import (
    event_type
)
from app.constants import printing
from app.models import (
    Orders,
    TaxPhoto,
    Users,
    Events
)
from app.search import search_queries


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['GET', 'POST'])
@login_required
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with today's date.

    As a user, I want to be able to search for specific orders.

    GET {order_number, suborder_number, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in search.py

    :return {orders, 200}
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        order_number = json.get("order_number")
        suborder_number = json.get("suborder_number")
        order_type = json.get("order_type")
        status = json.get("status")
        billing_name = json.get("billing_name")
        user = ''
        date_received_start = json.get("date_received_start")
        date_received_end = json.get("date_received_end")
        date_submitted_start = json.get("date_submitted_start")
        date_submitted_end = json.get("date_submitted_end")

        orders = search_queries(order_number,
                                suborder_number,
                                order_type,
                                status,
                                billing_name,
                                date_received_start,
                                date_received_end,
                                date_submitted_start,
                                date_submitted_end,
                                0,
                                100)

        # formatting results
        formatted_orders = []
        suborder_total = len(orders['hits']['hits'])
        order_total_list = [orders['hits']['hits'][i]['_source']['order_number'] for i in range(suborder_total)]
        order_total = len(set(order_total_list))

        if order_total != 0:
            for i in range(suborder_total):
                formatted_orders.append(orders['hits']['hits'][i]['_source'])

        return jsonify(order_count=order_total,
                       suborder_count=suborder_total,
                       all_orders=formatted_orders), 200

    else:
        orders = []
        order_count = 0
        for order in Orders.query.filter(Orders.date_received == date.today()):
            order_count += 1
            for suborder in order.suborder:
                orders.append(suborder.serialize)
        return jsonify(order_count=order_count, suborder_count=len(orders), all_orders=orders), 200


@api.route('/orders/<doc_type>', methods=['GET'])
@login_required
def orders_doc(doc_type):
    """

    :param doc_type: document type ('csv' only)
    :return:
    """
    if doc_type.lower() == 'csv':
        url = generate_csv(request.args)
        return jsonify(url=url), 200


@api.route('/status/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def status_change(suborder_number):
    """
    GET: {suborder_number}; returns {suborder_number, current_status}, 200
    POST: {suborder_number, new_status, comment}

    Status Table
    - ID - Integer
    - Status - ENUM
        1. Received || Set to this by default
        2. Processing
            a)Found
            b)Printed
        3. Mailed/Pickup
        4. Not_Found
           a)Letter_generated
           b)Undeliverable - Cant move down the line
        5. Done - End of status changes
    :return: {status_id, suborder_number, status, comment}, 201
    """
    if request.method == 'POST':
        json = request.get_json(force=True)
        comment = json.get("comment")
        new_status = json.get("new_status")

        """
            POST: {suborder_number, new_status, comment};
            returns: {status_id, suborder_number, status, comment}, 201
        """
        status_code = update_status(suborder_number, comment, new_status)
        return jsonify(status_code=status_code), 200


@api.route('/history/<string:suborder_number>', methods=['GET'])
@login_required
def history(suborder_number):
    """
    GET: {suborder_number};
    :param suborder_number:
    :return: {suborder_number, previous value, new value, comment, date}, 200

    Look for all the rows with this suborder_number and list out the history for each one in Descending order
     also get the comment and date with these to send to the front
    """
    # TODO: Events.type.in(..., event_type.UPDATE_TAX_PHOTO)
    status_history = [event.status_history for event in
                      Events.query.filter(Events.suborder_number == suborder_number,
                                          Events.type.in_(
                                              [event_type.UPDATE_STATUS, event_type.INITIAL_IMPORT])
                                          ).order_by(desc(Events.timestamp)).all()]

    return jsonify(history=status_history), 200


@api.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_single_order(order_id):
    """
    :param order_id:
    :return: the orders with that specific client id that was passed
    """
    orders = [order.serialize for order in Orders.query.filter_by(client_id=order_id).all()]

    if len(orders) == 0:
        abort(404)

    return jsonify(orders=orders), 200


@api.route('/tax_photo/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def tax_photo(suborder_number):
    if request.method == 'GET':
        t_photo = TaxPhoto.query.filter_by(suborder_number=suborder_number).one()
        return jsonify(block_no=t_photo.block,
                       lot_no=t_photo.lot,
                       roll_no=t_photo.roll), 200

    else:
        json = request.get_json(force=True)
        block_no = json.get("block_no")
        lot_no = json.get("lot_no")
        roll_no = json.get("roll_no")

        message = update_tax_photo(suborder_number, block_no, lot_no, roll_no)
        return jsonify(message=message), 200


@api.route('/print/<string:print_type>', methods=['POST'])
@login_required
def print_order(print_type):
    """
    Generate a PDF for a print operation.

    :param print_type: ('orders', 'small_labels', 'large_labels')
    """
    search_params = request.get_json(force=True)

    handler_for_type = {
        printing.ORDERS: _print_orders,
        printing.SMALL_LABELS: _print_small_labels,
        printing.LARGE_LABELS: _print_large_labels
    }

    url = handler_for_type[print_type](search_params)

    return jsonify({"url": url}), 200


@api.route('/login', methods=['POST'])
def login():
    """
    Login a user through the API.

    :return: {user_id}, 200
    """
    user_info = request.get_json(force=True)

    user = Users.query.filter_by(email=user_info['email']).one_or_none()

    if user is None:
        return jsonify(
            {
                "authenticated": False,
                "message": "Invalid username or password entered"
            }
        ), 401

    valid_password = user.verify_password(user_info['password'])

    if not valid_password:
        return jsonify(
            {
                "authenticated": False,
                "message": "Invalid username or password entered"
            }
        ), 401

    login_user(user)

    return jsonify(
        {
            "authenticated": True,
            "email": current_user.email
        }
    ), 200


@api.route('/logout', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    return jsonify({"authenticated": False}), 200
