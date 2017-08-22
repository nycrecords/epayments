from flask import jsonify, abort, request
import datetime
from datetime import date, datetime, timedelta
from sqlalchemy import func, databases, update, desc
from .import api_1_0 as api
from app.constants.client_agency_names import CLIENT_AGENCY_NAMES
from ..models import Orders, Customer, BirthSearch, BirthCertificate, MarriageSearch, MarriageCertificate, \
                     DeathSearch, DeathCertificate, PhotoGallery, PhotoTax, PropertyCard, StatusTracker
from sqlalchemy.orm import sessionmaker, Query
from app import db
import json
from .utils import update_status, get_orders_by_fields


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

    Else, orders are filtered with the previous day's date.

    As a user, I want to be able to search for specific orders.

    GET {order_no, suborder_no, order_type, billing_name, user, date_received_start, date_received_end},

    Search functionality should be in utils.py

    :return {orders, 200}

        "billingname": "Jeffrey Kobacker",
        "clientagencyname": "Death Search",
        "clientdata": "ClientID|10000103|ClientAgencyName|Department of Record|OrderNo|9127848504|LASTNAME|Bloch|FIRSTNAME|Isaac|MIDDLENAME|S|RELATIONSHIP|Great Grandson|PURPOSE|Genealogical/Historical|COPY_REQ|1|MONTH|December|DAY|7|DEATH_PLACE|Manhattan, New York|AGEOFDEATH|78|YEAR_|1918,|BOROUGH|MANHATTAN,|",
        "clientid": 10000103,
        "confirmationmessage": "\nLast name:               Bloch\nFirst name:              Isaac\nMiddle name:             S\n\nMonth:                   December\nDay:                     7\nYear:                    1918\n\n--------------------------------------------------------------------------------\nCemetery:                (Left Blank)\nPlace of Death:          Manhattan, New York\nAge at Death:            78\n\nAdditional Comments:     (Left Blank)\n\nBorough(s):              MANHATTAN\n\n--------------------------------------------------------------------------------\nRelationship to person:  Great Grandson\nPurpose:                 Genealogical/Historical\nLetter:                  (Left Blank)\nNumber of Copies:        1\n\n--------------------------------------------------------------------------------\n\n",
        "customeremail": "jkobacker@gmail.com",
        "datereceived": "2017-04-04 04:06:15",
        "datesubmitted": "Wed, 14 Jun 2017 00:00:00 GMT",
        "orderno": "000592000",
        "suborderno": 9127848504

    """
    # get_json()

    order_number = request.args.get('ordernumber', '')
    print(order_number)
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
    # if request.form:
    #     order_number = str(request.args.get('ordernumber', ''))
        json = request.get_json(force=True)
        order_number = json.get("order_no")
        suborder_number = json.get("suborder_no")
        print('hellodsds')
        order_type = json.get("order_type")
        billing_name = json.get("billing_name")
        # user = str(request.form["user"])
        user = ''
        date_received = json.get("date_deceived")
        date_submitted = json.get("date_submitted")

        orders = get_orders_by_fields(order_number, suborder_number, order_type, billing_name, user, date_received,
                                      date_submitted)
        print("hello")
        print(orders)
        return jsonify(orders=orders)
    else:
        yesterday = datetime.strptime(date.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        # orders = [order.serialize for order in Orders.query.filter_by(date_received=yesterday).all()]
        orders = [order.serialize for order in Orders.query.filter_by().all()]
        return jsonify(all_orders=orders)


@api.route('/status/<int:sub_order_no>', methods=['GET'])
def status_lookup(sub_order_no):
    """
    :param sub_order_no:
    :return: the status of all records with this sub_order_no that was passed in
    """
    status = [status.serialize for status in StatusTracker.query.filter_by(sub_order_no=sub_order_no).all()]

    return jsonify(status=status)


@api.route('/status/<int:sub_order_no>/update', methods=['GET', 'POST'])
def status_change(sub_order_no):
    """
        GET: {sub_order_no}; returns {sub_order_no, current_status}, 200
        POST: {sub_order_no, new_status, comment}

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
        :return: {status_id, sub_order_no, status, comment}, 201
    """

    # session = StatusTracker.query.filter_by(sub_order_no=sub_order_no).first_or_404()
    session = StatusTracker.query.order_by(StatusTracker.sub_order_no.desc()).first()
    curr_status = session.current_status
    status_id = session.id

    # This will update the status of the sub_order_no
    # session.current_status = 'Processing'
    # db.session.commit()

    # status = {'Received', 'Processing', 'Found', 'Printed' 'Mailed/Pickup', 'Not_Found', 'Letter_generated',
    #           'Undeliverable', 'Done'}

    comment = "The Record is Done."
    new_status = 'Done'
    # sub_order_no = 9128144811

    if request.form:  # Means that something was passed from the front
        curr_status = str(request.form["status"])

        """ 
            POST: {sub_order_no, new_status, comment}; 
            returns: {status_id, sub_order_no, status, comment}, 201 
        """

    update_status(sub_order_no, comment, new_status)

    return jsonify(current_status=curr_status, sub_order_no=sub_order_no, comment=comment, status_id=status_id)


@api.route('/history/<int:sub_order_no>', methods=['GET'])
def history(sub_order_no):
    """
    GET: {sub_order_no};
    :param sub_order_no:
    :return: {sub_order_no, previous value, new value, comment, date}, 200

    Look for all the rows with this sub_order_no and list out the history for each one in Descending order
     also get the comment and date with these to send to the front
    """

    # history = StatusTracker.query.order_by(StatusTracker.timestamp.desc())
    # history_list = [i.serialize for i in history]  # loop through and use the serialize function
    # print(history)
    # print(history_list)

    history = [status.serialize for status in StatusTracker.query.filter_by(sub_order_no=sub_order_no).all()]

    return jsonify(history=history)


@api.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    """
    :param order_id:
    :return: the orders with that specific client id that was passed
    """
    orders = [order.serialize for order in Orders.query.filter_by(client_id=order_id).all()]

    if len(orders) == 0:
        abort(404)

    return jsonify(orders=orders)
