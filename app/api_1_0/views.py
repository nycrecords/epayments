from datetime import date

from flask import jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app.api_1_0 import api_1_0 as api
from app.api_1_0.utils import (
    create_new_order,
    update_status,
    _print_orders,
    _print_large_labels,
    _print_small_labels,
    update_tax_photo,
    generate_csv,
)
from app.constants import event_type
from app.constants import printing
from app.models import (
    Events,
    Suborders,
    TaxPhoto,
    Users,
)
from app.search.searchfunctions import SearchFunctions
from app.search.utils import search_queries


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

    Search functionality should be in utils.py

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
        start = json.get("start")
        size = json.get("size")

        multiple_items = ''
        if order_type == 'multiple_items':
            # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
            multiple_items = True
            order_type = 'all'

        orders = search_queries(order_number,
                                suborder_number,
                                order_type,
                                status,
                                billing_name,
                                date_received_start,
                                date_received_end,
                                date_submitted_start,
                                date_submitted_end,
                                multiple_items,
                                start,
                                size,
                                "search")

        # formatting results
        formatted_orders = SearchFunctions.format_results(orders)
        suborder_total = orders['hits']['total']
        order_total = orders['aggregations']['order_count']['value']

        return jsonify(order_count=order_total,
                       suborder_count=suborder_total,
                       all_orders=formatted_orders), 200

    else:
        orders = search_queries(date_received_start=date.today().strftime('%m/%d/%Y'))
        formatted_orders = SearchFunctions.format_results(orders)
        suborder_total = orders['hits']['total']
        order_total = orders['aggregations']['order_count']['value']

        return jsonify(order_count=order_total,
                       suborder_count=suborder_total,
                       all_orders=formatted_orders), 200


@api.route('/orders/<string:doc_type>', methods=['GET'])
@login_required
def orders_doc(doc_type: str):
    """

    :param doc_type: document type ('csv' only)
    :return:
    """
    if doc_type.lower() == 'csv':
        url = generate_csv(request.args)
        return jsonify(url=url), 200


@api.route('/orders/new', methods=['POST'])
@login_required
def new_order():
    """
    :return:
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)

        create_new_order(json['orderInfo'], json['suborderList'])

    return jsonify(), 200


@api.route('/status/<string:suborder_number>', methods=['PATCH'])
@login_required
def patch(suborder_number: str):
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
    json = request.get_json(force=True)
    comment = json.get("comment")
    new_status = json.get("new_status")

    suborder = Suborders.query.filter_by(id=suborder_number).one_or_none()
    if suborder is None:
        return jsonify(error={
            'code': 404,
            'message': 'Suborder Not Found',
        }), 404

    status_code = update_status(suborder_number, comment, new_status)
    return jsonify(status_code=status_code), status_code


# TODO: WIP, Complete this
@api.route('/statuses/', methods=['GET', 'POST'])
@login_required
def batch_status_change():
    """
    GET: returns { current_status}, 200
    POST: {queueForUpdate, queueForUpdateBoolean, new_status, comment}

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
        queue_for_update = json.get("queueForUpdate")
        queue_for_update_boolean = json.get("queueForUpdateBoolean")
        status_code = []
        for index in range(len(queue_for_update_boolean)):
            """
                POST: {queueForUpdate, queueForUpdateBoolean, new_status, comment};
                returns: {status_id, suborder_number, status, comment}, 201
            """
        status_code.append(update_status(queue_for_update[index], comment, new_status))
    return jsonify(status_code=status_code), 200


@api.route('/history/<string:suborder_number>', methods=['GET'])
@login_required
def history(suborder_number: str):
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


@api.route('/more_info/<string:suborder_number>', methods=['GET','POST'])
@login_required
def more_info(suborder_number: str):
    """
    GET: {suborder_number
    :param suborder_number:
    :return: json of all the info
    """

    if request.method == 'POST':
        order_info = SearchFunctions.format_first_result(search_queries(suborder_number=suborder_number,
                                                                        search_type="print"))

        return jsonify(order_info=order_info), 200


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
def print_order(print_type: str):
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
