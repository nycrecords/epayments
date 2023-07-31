import os
from datetime import date
from flask import current_app, jsonify, render_template, request, Response, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app import db
from app.api.v1 import api_v1 as api
from app.api.v1.utils import (
    create_new_order,
    update_status,
    _print_orders,
    _print_large_labels,
    _print_small_labels,
    update_tax_photo,
    generate_csv,
    update_check_mo_number,
)
from app.constants import event_type
from app.constants import printing
from app.models import (
    Events,
    NoAmends,
    Suborders,
    TaxPhoto,
    Users,
    Orders,
)
from app.search.searchfunctions import SearchFunctions
from app.search.utils import search_queries


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/orders', methods=['GET', 'POST'])
@login_required
def get_orders() -> Response:
    """
    Retrieves the data for orders to be displayed.

    If a form is submitted, the parameters including order_number, suborder_number,
    order_type, billing_name, date_received_start, and date_received_end will be retrieved
    from the form data and used in a function called get_orders_by_fields to filter orders.

    Else, orders are filtered with today's date.

    As a user, I want to be able to search for specific orders.

    GET {order_number, suborder_number, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in utils.py

    :return {orders, 200}
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        order_number = json.get('order_number')
        suborder_number = json.get('suborder_number')
        order_type = json.get('order_type')
        delivery_method = json.get('delivery_method')
        status = json.get('status')
        billing_name = json.get('billing_name')
        date_received_start = json.get('date_received_start')
        date_received_end = json.get('date_received_end')
        date_submitted_start = json.get('date_submitted_start')
        date_submitted_end = json.get('date_submitted_end')
        start = json.get('start')
        size = json.get('size')
        email = json.get('email')

        multiple_items = ''
        if order_type == 'multiple_items':
            multiple_items = True
            order_type = 'all'  # Overwrite order_type value from 'multiple_items' to 'all' for search

        orders = search_queries(order_number,
                                suborder_number,
                                order_type,
                                delivery_method,
                                status,
                                billing_name,
                                email,
                                date_received_start,
                                date_received_end,
                                date_submitted_start,
                                date_submitted_end,
                                multiple_items,
                                start,
                                size)

        # formatting results
        formatted_orders = SearchFunctions.format_results(orders)
        suborder_total = orders['hits']['total']["value"]
        order_total = orders['aggregations']['order_count']['value']

        return jsonify(
            order_count=order_total,
            suborder_count=suborder_total,
            all_orders=formatted_orders,
            order_rows=render_template('order_table.html', orders=formatted_orders)
        ), 200

    else:
        orders = search_queries(date_received_start=date.today().strftime('%m/%d/%Y'))
        formatted_orders = SearchFunctions.format_results(orders)
        suborder_total = orders['hits']['total']["value"]
        order_total = orders['aggregations']['order_count']['value']

        return jsonify(
            order_count=order_total,
            suborder_count=suborder_total,
            all_orders=formatted_orders,
            order_rows=render_template('order_table.html', orders=formatted_orders),
        ), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/orders/<string:doc_type>', methods=['GET'])
@login_required
def orders_doc(doc_type: str) -> Response:
    """Handles the export of data given the doc_type. Currently only supports 'csv'.

    Args:
        doc_type: The type of document to export data into.

    Returns:
        JSON response containing the URL of the generated CSV if successful.
    """
    if doc_type.lower() == 'csv':
        url = generate_csv(request.args)
        return jsonify(url=url), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/orders/new', methods=['POST'])
@login_required
def new_order() -> Response:
    """
    :return:
    """
    json = request.get_json(force=True)
    create_new_order(json['order_info'], json['suborders'])
    return jsonify(), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/status/<string:suborder_number>', methods=['PATCH'])
@login_required
def patch(suborder_number: str) -> Response:
    """Updates a suborder.

    Args:
        suborder_number: Primary key ID of the suborder.

    Returns:
        JSON response.
    """
    json = request.get_json(force=True)
    comment = json.get('comment')
    new_status = json.get('status')

    suborder = Suborders.query.filter_by(id=suborder_number).one_or_none()
    if suborder is None:
        return jsonify(error={
            'code': 404,
            'message': 'Suborder Not Found',
        }), 404

    if suborder.status != new_status:
        update_status(suborder, comment, new_status)
        return jsonify(), 200

    return jsonify(error={
        'code': 404,
        'message': 'Bad Request',
    }), 400


# TODO (@gzhou): WIP, Complete this
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
        comment = json.get('comment')
        new_status = json.get('new_status')
        queue_for_update = json.get('queueForUpdate')
        queue_for_update_boolean = json.get('queueForUpdateBoolean')
        status_code = []
        for index in range(len(queue_for_update_boolean)):
            """
                POST: {queueForUpdate, queueForUpdateBoolean, new_status, comment};
                returns: {status_id, suborder_number, status, comment}, 201
            """
        status_code.append(update_status(queue_for_update[index], comment, new_status))
    return jsonify(status_code=status_code), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/history/<string:suborder_number>', methods=['GET'])
@login_required
def history(suborder_number: str) -> Response:
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

    return jsonify(
        history=status_history,
        history_tab=render_template('history_row.html', history=status_history)
    ), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/more_info/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def more_info(suborder_number: str) -> Response:
    """
    GET: {suborder_number
    :param suborder_number:
    :return: json of all the info
    """

    if request.method == 'POST':
        order_info = SearchFunctions.format_first_result(search_queries(suborder_number=suborder_number,
                                                                        search_type='print'))
        order_type = order_info['order_type']
        order_type_template_handler = {
            'Birth Search': 'birth_search.html',
            'Birth Cert': 'birth_cert.html',
            'Marriage Search': 'marriage_search.html',
            'Marriage Cert': 'marriage_cert.html',
            'Death Search': 'death_search.html',
            'Death Cert': 'death_cert.html',
            'Tax Photo': 'tax_photo.html',
            'Photo Gallery': 'photo_gallery.html',
            'Property Card': 'property_card.html',
            'OCME': 'ocme.html',
            'HVR': 'hvr.html',
            'No Amends': 'no_amends.html'
        }

        info_tab = render_template('orders/{}'.format(order_type_template_handler[order_type]),
                                   order_info=order_info)

        return jsonify(
            order_info=order_info,
            info_tab=info_tab
        ), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/tax_photo/<string:suborder_number>', methods=['GET', 'POST'])
@login_required
def tax_photo(suborder_number) -> Response:
    """TODO (@gzhou): docstring
    """
    if request.method == 'GET':
        t_photo = TaxPhoto.query.filter_by(suborder_number=suborder_number).one()
        return jsonify(
            block_no=t_photo.block,
            lot_no=t_photo.lot,
            roll_no=t_photo.roll,
        ), 200
    else:
        json = request.get_json(force=True)
        block_no = json.get('block_no')
        lot_no = json.get('lot_no')
        roll_no = json.get('roll_no')

        message = update_tax_photo(suborder_number, block_no, lot_no, roll_no)
        return jsonify(message=message), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/check_mo_number/<string:order_number>', methods=['GET', 'POST'])
@login_required
def check_mo_number(order_number) -> Response:
    """
    Retrieve or update the Check/Money Order number associated with an order.

    - GET: Returns the Check/Money Order number of the specified order.
        Returns:
        - JSON response containing the Check/Money Order number.
        - HTTP status code 200 (OK).

    - POST: Updates the Check/Money Order number of the specified order with new information.
        Request Payload (JSON):
        - check_mo_number: The new Check/Money Order number to be updated.

        Returns:
        - JSON response containing a message indicating the outcome of the update and the count of suborders within the order.
        - HTTP status code 200 (OK).

    :param order_number: The unique identifier of the order.
    :type order_number: str

    :return: JSON response containing relevant information based on the operation performed.
    :rtype: Response
    """
    order = Orders.query.get(order_number)

    if request.method == 'GET':
        return jsonify(
            check_mo_number=order.check_mo_number
        ), 200
    else:
        json = request.get_json(force=True)
        check_mo_number = json.get('check_mo_number')
        message = update_check_mo_number(order, check_mo_number)
        return jsonify(message=message, suborder_count=len(order.orders)), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/print/<string:print_type>', methods=['POST'])
@login_required
def print_order(print_type: str) -> Response:
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
    return jsonify({'url': url}), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/login', methods=['POST'])
def login() -> Response:
    """
    Login a user through the API.

    :return: {user_id}, 200
    """
    user_info = request.get_json(force=True)

    user = Users.query.filter_by(email=user_info['email']).one_or_none()

    if user is None:
        return jsonify(
            {
                'authenticated': False,
                'message': 'Invalid username or password entered'
            }
        ), 401

    valid_password = user.verify_password(user_info['password'])

    if not valid_password:
        return jsonify(
            {
                'authenticated': False,
                'message': 'Invalid username or password entered'
            }
        ), 401

    login_user(user)

    return jsonify(
        {
            'authenticated': True,
            'email': current_user.email
        }
    ), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/logout', methods=['DELETE'])
@login_required
def logout() -> Response:
    logout_user()
    return jsonify({'authenticated': False}), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/password', methods=['PATCH'])
@login_required
def change_password() -> Response:
    password_data = request.get_json(force=True)

    if password_data['password'] != password_data['confirm_password']:
        return jsonify(
            error={
                'message': 'Passwords do not match.'
            }), 400

    for key, value in password_data.items():
        if not value:
            return jsonify(
                error={
                    'code': 400,
                    'message': 'Passwords cannot be empty.',
                }), 400
        if len(value) < 6:
            return jsonify(
                error={
                    'code': 400,
                    'message': 'Password must contain at least 6 characters.',
                }), 400
        if len(value) > 12:
            return jsonify(
                error={
                    'code': 400,
                    'message': 'Password must contain less than 12 characters.',
                }), 400

    user = Users.query.filter_by(email=current_user.email).one_or_none()
    user.password = password_data['password']
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            'message': 'Password successfully changed.'
        }
    ), 200


# noinspection PyTypeChecker,PyTypeChecker
@api.route('/uploads/<string:suborder_number>', methods=['GET', 'POST'])
def download(suborder_number):
    no_amends = NoAmends.query.filter_by(suborder_number=suborder_number).one()
    directory = os.path.join(current_app.config["NO_AMENDS_FILE_PATH"], no_amends.suborder_number)
    return send_from_directory(directory, no_amends.filename, as_attachment=True)
