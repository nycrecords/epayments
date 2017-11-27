from datetime import date, timedelta, datetime, time

from flask import jsonify, abort, request, send_file, redirect, url_for
from flask_login import login_user, logout_user, current_user
from sqlalchemy import desc
from app.api_1_0 import api_1_0 as api

from app.api_1_0.utils import (
    update_status,
    get_orders_by_fields,
    _print_orders,
    _print_large_labels,
    _print_small_labels,
    update_tax_photo
)
from app.constants import (
    event_type
)
from app.constants import printing
from app.models import (
    Order,
    PhotoTax,
    Users,
    Event
)


@api.route('/', methods=['GET'])
def info():
    return jsonify({'version': 'v1.0'})


@api.route('/orders', methods=['GET', 'POST'])
def get_orders():
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_receieved_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with today's date.

    As a user, I want to be able to search for specific orders.

    GET {order_number, suborder_number, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in utils.py

    :return {orders, 200}
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        order_number = json.get("order_number")
        suborder_number = json.get("suborder_number")
        order_type = json.get("order_type")
        billing_name = json.get("billing_name")
        user = ''
        date_submitted_start = json.get("date_submitted_start")
        date_submitted_end = json.get("date_submitted_end")

        order_count, suborder_count, orders = get_orders_by_fields(order_number,
                                                                   suborder_number,
                                                                   order_type,
                                                                   billing_name,
                                                                   user,
                                                                   date_submitted_start,
                                                                   date_submitted_end)
        return jsonify(order_count=order_count,
                       suborder_count=suborder_count,
                       all_orders=orders)

    else:
        yesterday = date.today() - timedelta(1)
        # Add time to date object
        yesterday_dt = datetime.combine(yesterday, time.min)

        orders = []
        order_count = 0
        for order in Order.query.filter(Order.date_submitted >= yesterday_dt):
            order_count += 1
            for suborder in order.suborder:
                orders.append(suborder.serialize)
        return jsonify(order_count=order_count, suborder_count=len(orders), all_orders=orders)


@api.route('/status/<string:suborder_number>', methods=['GET', 'POST'])
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
        return jsonify(status_code=status_code)

    # return jsonify(current_status=curr_status, suborder_number=suborder_number, comment=comment, status_id=status_id)
    status = [status.serialize for status in Event.query.filter_by(suborder_number=int(suborder_number)).all()]
    return jsonify(status=status)


@api.route('/history/<string:suborder_number>', methods=['GET'])
def history(suborder_number):
    """
    GET: {suborder_number};
    :param suborder_number:
    :return: {suborder_number, previous value, new value, comment, date}, 200

    Look for all the rows with this suborder_number and list out the history for each one in Descending order
     also get the comment and date with these to send to the front
    """
    status_history = [event.status_history for event in
                      Event.query.filter(Event.suborder_number == suborder_number,
                                         Event.type.in_(
                                             [event_type.UPDATE_STATUS, event_type.INITIAL_IMPORT])
                                         ).order_by(desc(Event.timestamp)).all()]

    history = [status.serialize for status in
               Event.query.filter_by(suborder_number=int(suborder_number)).order_by(
                   desc(Event.timestamp)).all()]

    return jsonify(history=status_history)


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    """
    :param order_id:
    :return: the orders with that specific client id that was passed
    """
    orders = [order.serialize for order in Order.query.filter_by(client_id=order_id).all()]

    if len(orders) == 0:
        abort(404)

    return jsonify(orders=orders)


@api.route('/photo_tax/<string:suborder_number>', methods=['GET', 'POST'])
def photo_tax(suborder_number):
    if request.method == 'GET':
        p_tax = PhotoTax.query.filter_by(suborder_number=suborder_number).one()
        return jsonify(block_no=p_tax.block,
                       lot_no=p_tax.lot,
                       roll_no=p_tax.roll)

    else:
        json = request.get_json(force=True)
        block_no = json.get("block_no")
        lot_no = json.get("lot_no")
        roll_no = json.get("roll_no")

        updated_p_tax = update_tax_photo(suborder_number, block_no, lot_no, roll_no)
        return jsonify(updated_p_tax=updated_p_tax)


@api.route('/print/<string:print_type>', methods=['POST'])
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
    return jsonify({"url": url_for("main.import_xml", _external=True)})
    # return send_file(handler_for_type[print_type](search_params), as_attachment=True,
    #                  attachment_filename='order.pdf'), 200


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
def logout():
    logout_user()
    return jsonify({"authenticated": False}), 200
