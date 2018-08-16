from datetime import date
from flask import jsonify, abort, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from app.api_1_0 import api_1_0 as api
from app import db
from app.models.order_number_counter import OrderNumberCounter
from app.models.orders import Orders, Suborders
from app.models.customers import Customers
from app import db_utils
from sqlalchemy import *
from sqlalchemy.orm import *

import datetime
import json
from app.db_utils import (create_object)
from app.constants import order_types
from app.models.photo import TaxPhoto, PhotoGallery
from app.models.property_card import PropertyCard
from app.models.death import DeathCertificate, DeathSearch
from app.models.marriage import MarriageCertificate, MarriageSearch
from app.models.birth import BirthCertificate, BirthSearch
from app.constants import order_types

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

        if not (order_number or suborder_number or billing_name) and not date_received_start:
            date_received_start = date.today()
        order_count, suborder_count, orders = get_orders_by_fields(order_number,
                                                                   suborder_number,
                                                                   order_type,
                                                                   status,
                                                                   billing_name,
                                                                   user,
                                                                   date_received_start,
                                                                   date_received_end)
        return jsonify(order_count=order_count,
                       suborder_count=suborder_count,
                       all_orders=orders), 200

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


@api.route('/orders/new', methods=['POST'])
@login_required
def new_order():
    """
    :return:
    """
    if request.method == 'POST':  # makes it so we get a post method to receive the info put in on the form
        json = request.get_json(force=True)
        add_description = json.get("addDescription")
        address_line_1 = json.get("addressLine1")
        address_line_2 = json.get("addressLine2")
        billing_name = json.get("billingName")
        birth_place = json.get("birthPlace")
        block = json.get("block")
        borough = json.get("borough")
        bride_last_name = json.get("brideLastName")
        bride_first_name = json.get("brideFirstName")
        building_number = json.get("buildingNum")
        cemetery = json.get("cemetery")
        certificate_num = json.get("certificateNum")
        certified = json.get("certified")
        collection = json.get("collection")
        comment = json.get("comment")
        contact_number = json.get("contactNum")
        city = json.get("city")
        day = json.get("day")
        death_place = json.get("deathPlace")
        email = json.get("email")
        father_name = json.get("fatherName")
        first_name = json.get("firstName")
        gender = json.get("gender")
        groom_last_name = json.get("groomLastName")
        groom_first_name = json.get("groomFirstName")
        instruction = json.get("instructions")
        img_id = json.get("imgId")
        img_title = json.get("imgTitle")
        last_name = json.get("lastName")
        letter = json.get("letter")
        lot = json.get("lot")
        mail = json.get("mail")
        marriage_place = json.get("marriagePlace")
        middle_name = json.get("middleName")
        month = json.get("month")
        mother_name = json.get("motherName")
        num_copies = json.get("numCopies")
        order_type = json.get("orderType")
        personal_use_agreement = json.get("personalUseAgreement")
        phone = json.get("phone")
        print_size = json.get("printSize")
        roll = json.get("roll")
        state = json.get("state")
        status = json.get("status")
        street = json.get("street")
        years = json.get("year")
        zip_code = json.get("zipCode")
        today = datetime.datetime.today().strftime("%m/%d/%y")
        year = datetime.datetime.now().strftime("%Y")

        next_order_number = OrderNumberCounter.query.filter_by(year=year).one().next_order_number
        order_id = "EPAY-" + year + "-" + str(next_order_number)
        main_order = Orders(id=order_id,
                            date_submitted=today,
                            date_received=today,
                            confirmation_message="",
                            client_data="",
                            order_types=order_type,
                            multiple_items=True)
        create_object(main_order)
        customer = Customers(billing_name=billing_name,
                             email=email,
                             shipping_name=billing_name,
                             address_line_1=address_line_1,
                             address_line_2=address_line_2,
                             city=city,
                             state=state,
                             zip_code=zip_code,
                             phone=phone,
                             instructions=instruction,
                             order_number=main_order.id,
                             )
        create_object(customer)
        for index in range(len(order_type)):
            sub_order_number = Orders.query.filter_by(id=main_order.id).one().next_suborder_number
            sub_order_id = main_order.id + "-" + str(sub_order_number)
            sub_order = Suborders(id=sub_order_id,
                                  client_id=customer.id,
                                  order_type=order_type[index],
                                  order_number=main_order.id,
                                  _status=status[index]
                                  )
            create_object(sub_order)

            handler_for_order_type = {
                order_types.TAX_PHOTO: TaxPhoto(borough=None,
                                                collection=collection[index],
                                                roll=roll[index],
                                                block=block[index],
                                                lot=lot[index],
                                                building_number=building_number[index],
                                                street=street[index],
                                                description=add_description[index],
                                                mail=mail[index],
                                                contact_number=contact_number[index],
                                                size=print_size[index],
                                                num_copies=num_copies[index],
                                                suborder_number=sub_order.id),
                order_types.PHOTO_GALLERY: PhotoGallery(image_id=img_id[index],
                                                        description=img_title[index],
                                                        additional_description=add_description[index],
                                                        size=print_size[index],
                                                        num_copies=num_copies[index],
                                                        mail=mail[index],
                                                        contact_number=contact_number[index],
                                                        personal_use_agreement=personal_use_agreement[index],
                                                        comment=comment[index],
                                                        suborder_number=sub_order.id),
                order_types.PROPERTY_CARD: PropertyCard(borough=borough[index],
                                                        block=block[index],
                                                        lot=lot[index],
                                                        building_number=building_number[index],
                                                        street=street[index],
                                                        description=add_description[index],
                                                        certified=certified[index],
                                                        mail=mail[index],
                                                        contact_info=contact_number[index],
                                                        suborder_number=sub_order.id
                                                        ),
                order_types.DEATH_SEARCH: DeathSearch(last_name=last_name[index],
                                                      first_name=first_name[index],
                                                      middle_name=middle_name[index],
                                                      num_copies=num_copies[index],
                                                      cemetery=cemetery[index],
                                                      month=month[index],
                                                      day=day[index],
                                                      years=years[index],
                                                      death_place=death_place[index],
                                                      borough=borough[index],
                                                      letter=letter[index],
                                                      comment=comment[index],
                                                      suborder_number=sub_order.id),
                order_types.DEATH_CERT: DeathCertificate(certificate_number=certificate_num[index],
                                                         last_name=last_name[index],
                                                         first_name=first_name[index],
                                                         middle_name=middle_name[index],
                                                         num_copies=num_copies[index],
                                                         cemetery=cemetery[index],
                                                         month=month[index],
                                                         day=day[index],
                                                         years=years[index],
                                                         death_place=death_place[index],
                                                         borough=borough[index],
                                                         letter=letter[index],
                                                         comment=comment[index],
                                                         suborder_number=sub_order.id),
                order_types.MARRIAGE_SEARCH: MarriageSearch(groom_last_name=groom_last_name[index],
                                                            groom_first_name=groom_first_name[index],
                                                            bride_last_name=bride_last_name[index],
                                                            bride_first_name=bride_first_name[index],
                                                            num_copies=num_copies[index],
                                                            month=month[index],
                                                            day=day[index],
                                                            years=years[index],
                                                            marriage_place=marriage_place[index],
                                                            borough=borough[index],
                                                            letter=letter[index],
                                                            comment=comment[index],
                                                            suborder_number=sub_order.id),
                order_types.MARRIAGE_CERT: MarriageCertificate(certificate_number=certificate_num[index],
                                                               groom_last_name=groom_last_name[index],
                                                               groom_first_name=groom_first_name[index],
                                                               bride_last_name=bride_last_name[index],
                                                               bride_first_name=bride_last_name[index],
                                                               num_copies=num_copies[index],
                                                               month=month[index],
                                                               day=day[index],
                                                               years=years[index],
                                                               marriage_place=marriage_place[index],
                                                               borough=borough[index],
                                                               letter=letter[index],
                                                               comment=comment[index],
                                                               suborder_number=sub_order.id),
                order_types.BIRTH_SEARCH: BirthSearch(first_name=first_name[index],
                                                      last_name=last_name[index],
                                                      middle_name=middle_name[index],
                                                      gender=gender[index],
                                                      father_name=father_name[index],
                                                      mother_name=mother_name[index],
                                                      num_copies=num_copies[index],
                                                      month=month[index],
                                                      day=day[index],
                                                      years=years[index],
                                                      birth_place=birth_place[index],
                                                      borough=borough[index],
                                                      letter=letter[index],
                                                      comment=comment[index],
                                                      suborder_number=sub_order.id),
                order_types.BIRTH_CERT: BirthCertificate(certificate_number=certificate_num[index],
                                                         last_name=last_name[index],
                                                         first_name=first_name[index],
                                                         middle_name=middle_name[index],
                                                         gender=gender[index],
                                                         father_name=father_name[index],
                                                         mother_name=mother_name[index],
                                                         num_copies=num_copies[index],
                                                         month=month[index],
                                                         day=day[index],
                                                         years=years[index],
                                                         birth_place=birth_place[index],
                                                         borough=borough[index],
                                                         letter=letter[index],
                                                         comment=comment[index],
                                                         suborder_number=sub_order.id)
            }
            create_object(handler_for_order_type[order_type[index]])
            user_email = Users.query.filter_by(email=current_user.email).one_or_none().get_id()
            new_value = {"status": status[index]}

            event = Events(suborder_number=sub_order.id, user_email=user_email,
                           type_=event_type.ORDER_CREATED,
                           timestamp=datetime.datetime.now(),
                           previous_value=None, new_value=new_value)
            create_object(event)

    return jsonify(), 200


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


@api.route('/statuses/new', methods=['GET', 'POST'])
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
        # print(queue_for_update_boolean)
        # print(comment)
        # print(new_status)
        for index in range(len(queue_for_update_boolean)):
            """
                POST: {queueForUpdate, queueForUpdateBoolean, new_status, comment};
                returns: {status_id, suborder_number, status, comment}, 201
            """
            if queue_for_update_boolean[index]:
                update_status(queue_for_update[index], comment, new_status)
    return jsonify(), 200


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
