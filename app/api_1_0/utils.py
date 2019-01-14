import csv
from datetime import date, datetime
from typing import Dict, List, Union

from flask import render_template, current_app, url_for
from flask_login import current_user
from os.path import join
from xhtml2pdf.pisa import CreatePDF

from app import db
from app.constants import (
    collection,
    event_type,
    printing
)
from app.constants import order_types
from app.constants.customer import EMPTY_CUSTOMER
from app.constants.search import ELASTICSEARCH_MAX_SIZE
from app.db_utils import create_object, update_object
from app.models import (
    BirthCertificate,
    BirthSearch,
    DeathCertificate,
    DeathSearch,
    MarriageCertificate,
    MarriageSearch,
    Orders,
    OrderNumberCounter,
    Suborders,
    Customers,
    TaxPhoto,
    Events,
    PhotoGallery
)
from app.search.searchfunctions import SearchFunctions
from app.search.utils import search_queries


def update_status(suborder: Suborders, comment: str, new_status: str) -> int:
    """Updates the status of a row from the Suborders table.

    Args:
        suborder: A Suborders instance.
        comment: Any additional information about the updating of the status.
        new_status: The value of the status to be updated to.

    Returns:
        An integer of the status code.
    """
    if new_status != suborder.status:
        prev_event = Events.query.filter(Events.suborder_number == suborder.id,
                                         Events.new_value['status'].astext == suborder.status).order_by(
            Events.timestamp.desc()).first()

        previous_value = {}
        new_value = {}

        previous_value['status'] = suborder.status
        if 'comment' in prev_event.new_value:
            previous_value['comment'] = prev_event.new_value['comment']

        update_object({'status': new_status}, Suborders, suborder.id)

        new_value['status'] = new_status
        if comment:
            new_value['comment'] = comment

        event = Events(suborder.id,
                       event_type.UPDATE_STATUS,
                       current_user.email,
                       previous_value,
                       new_value)

        create_object(event)
        suborder.es_update()

        return 200
    else:
        return 400
        # TODO: Raise error because new_status can't be the current status


def update_tax_photo(suborder_number: str, block_no: str, lot_no: str, roll_no: str) -> str:
    """
    This function is used for the Tax Photo API POST method,
    will update these fields from JSON sent back

    :param suborder_number:
    :param block_no:
    :param lot_no:
    :param roll_no:
    :return: {}
    """
    tax_photo = TaxPhoto.query.filter_by(suborder_number=suborder_number).one()

    message = "No changes were made"
    new_value = {}
    previous_value = {}

    for name, value, col_value in [
        ('block', block_no, tax_photo.block),
        ('lot', lot_no, tax_photo.lot),
        ('roll', roll_no, tax_photo.roll)
    ]:
        if value and value != col_value:
            setattr(tax_photo, name, value)
            new_value[name] = value
            previous_value[name] = col_value

    if new_value:
        db.session.add(tax_photo)

        event = Events(suborder_number,
                       event_type.UPDATE_TAX_PHOTO,
                       current_user.email,
                       previous_value,
                       new_value)

        db.session.add(event)
        db.session.commit()
        message = "Tax Photo Info Updated"
    return message


def _print_orders(search_params: Dict[str, str]) -> str:
    """
    Generate PDF order sheets.

    :param search_params: JSON Fields from the search form
    :type search_params: JSON

    :return: PDF
    """
    order_number = search_params.get("order_number")
    suborder_number = search_params.get("suborder_number")
    order_type = search_params.get("order_type")
    status = search_params.get("status")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_received_start = search_params.get("date_received_start")
    date_received_end = search_params.get("date_received_end")
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborders = search_queries(order_number,
                               suborder_number,
                               order_type,
                               status,
                               billing_name,
                               date_received_start,
                               date_received_end,
                               date_submitted_start,
                               date_submitted_end,
                               multiple_items,
                               0,
                               ELASTICSEARCH_MAX_SIZE,
                               "print")

    suborder = SearchFunctions.format_results(suborders)

    order_type_template_handler = {
        "Birth Search": 'birth_search.html',
        "Birth Cert": 'birth_cert.html',
        "Marriage Search": 'marriage_search.html',
        "Marriage Cert": 'marriage_cert.html',
        "Death Search": 'death_search.html',
        "Death Cert": 'death_cert.html',
        "Tax Photo": 'tax_photo.html',
        "Photo Gallery": 'photo_gallery.html',
        "Property Card": 'property_card.html',
    }

    html = ''

    for item in suborder:
        html += render_template("orders/{}".format(order_type_template_handler[item['order_type']]),
                                order_info=item, customer_info=item['customer'])

    filename = 'order_sheets_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_small_labels(search_params: Dict[str, str]) -> str:
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get("order_number")
    suborder_number = search_params.get("suborder_number")
    order_type = search_params.get("order_type")
    status = search_params.get("status")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_received_start = search_params.get("date_received_start")
    date_received_end = search_params.get("date_received_end")
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborder_results = search_queries(order_number,
                                      suborder_number,
                                      order_type,
                                      status,
                                      billing_name,
                                      date_received_start,
                                      date_received_end,
                                      date_submitted_start,
                                      date_submitted_end,
                                      multiple_items,
                                      0,
                                      ELASTICSEARCH_MAX_SIZE,
                                      "search")

    # Only want suborder_number, and order type
    suborders = SearchFunctions.format_results(suborder_results)

    customers = []

    for item in suborders:
        customers.append(item['customer'])

    labels = [customers[i:i + printing.SMALL_LABEL_COUNT] for i in range(0, len(customers), printing.SMALL_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.SMALL_LABEL_COUNT:
            for i in range(printing.SMALL_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/small_labels.html', labels=page)

    filename = 'small_labels_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_large_labels(search_params: Dict[str, str]) -> str:
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get("order_number")
    suborder_number = search_params.get("suborder_number")
    order_type = search_params.get("order_type")
    status = search_params.get("status")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_received_start = search_params.get("date_received_start")
    date_received_end = search_params.get("date_received_end")
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    multiple_items = ''
    if order_type == 'multiple_items':
        # Since multiple_items is parsed from the order_type field, we must overwrite the order_type field
        multiple_items = True
        order_type = 'all'

    suborder_results = search_queries(order_number,
                                      suborder_number,
                                      order_type,
                                      status,
                                      billing_name,
                                      date_received_start,
                                      date_received_end,
                                      date_submitted_start,
                                      date_submitted_end,
                                      multiple_items,
                                      0,
                                      ELASTICSEARCH_MAX_SIZE,
                                      "search")

    # Only want suborder_number, and order type
    suborders = SearchFunctions.format_results(suborder_results)

    customers = []

    for item in suborders:
        customers.append(item['customer'])

    customers = sorted(customers, key=lambda customer: customer['billing_name'])

    labels = [customers[i:i + printing.LARGE_LABEL_COUNT] for i in range(0, len(customers), printing.LARGE_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.LARGE_LABEL_COUNT:
            for i in range(printing.LARGE_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/large_labels.html', labels=page)

    filename = 'large_labels_{username}_{time}.pdf'.format(username=current_user.email,
                                                           time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def generate_csv(search_params: Dict[str, str]) -> str:
    order_type = search_params.get('order_type')

    suborders = search_queries(
        order_number=search_params.get('order_number'),
        suborder_number=search_params.get('suborder_number'),
        order_type=order_type,
        status=search_params.get('status'),
        billing_name=search_params.get('billing_name'),
        date_received_start=search_params.get('date_received_start'),
        date_received_end=search_params.get('date_received_end'),
        date_submitted_start=search_params.get('date_submitted_start'),
        date_submitted_end=search_params.get('date_submitted_end'),
        search_type='csv'
    )

    formatted_suborder_list = SearchFunctions.format_results(suborders)

    filename = "orders_{}.csv".format(datetime.now().strftime("%m_%d_%Y_at_%I_%M_%p"))
    file = open(join(current_app.static_folder, 'files', filename), 'w')
    writer = csv.writer(file)

    if order_type == 'photos':
        writer.writerow([
            "Order Number",
            "Suborder Number",
            "Date Received",
            "Customer Name",
            "Phone",
            "Email",
            "Customer Address",
            "Delivery Method",
            "Size",
            "Copy",
            "Image Identifier",
            "Building Number",
            "Street",
            "Collection",
            "Borough",
            "Block",
            "Lot",
            "Roll",
            "Comment",
            "Description"
        ])

        for suborder in formatted_suborder_list:
            writer.writerow([
                "=\"" + suborder.get('order_number') + "\"",
                suborder.get('suborder_number'),
                suborder.get('date_received')[:8],
                suborder.get('customer')['billing_name'],
                suborder.get('customer').get('phone'),
                suborder.get('customer').get('email'),
                suborder.get('customer').get('address'),
                suborder.get('metadata').get('delivery_method'),
                suborder.get('metadata').get('size'),
                suborder.get('metadata').get('num_copies'),
                suborder.get('metadata').get('image_id', ''),
                suborder.get('metadata').get('building_number', ''),
                suborder.get('metadata').get('street', ''),
                suborder.get('metadata').get('collection', ''),
                suborder.get('metadata').get('borough', ''),
                suborder.get('metadata').get('block', ''),
                suborder.get('metadata').get('lot', ''),
                suborder.get('metadata').get('roll', ''),
                'Yes' if suborder.get('metadata').get('comment') else '',
                suborder.get('metadata').get('description', '')
            ])

    elif order_type == 'vital_records':
        writer.writerow([
            "Order Number",
            "Suborder Number",
            "Date Received",
            "Customer Name",
            "Email",
            "Certificate Type",
            "Certificate Number"
        ])

        for suborder in formatted_suborder_list:
            writer.writerow([
                "=\"" + suborder.get('order_number') + "\"",
                suborder.get('suborder_number'),
                suborder.get('date_received')[:8],
                suborder.get('customer')['billing_name'],
                suborder.get('customer').get('email'),
                suborder.get('order_type'),
                suborder.get('metadata').get('certificate_number')
            ])

    file.close()

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def create_new_order(order_info_dict: Dict[str, str], suborder_list: List[Dict]):
    """

    :param order_info_dict:
    :param suborder_list:
    :return:
    """
    order_types_list = [suborder['orderType'] for suborder in suborder_list]

    year = str(date.today().year)
    next_order_number = OrderNumberCounter.query.filter_by(year=year).one().next_order_number
    order_id = "EPAY-{0:s}-{1:03d}".format(year, next_order_number)

    order = Orders(id=order_id,
                   date_submitted=date.today(),
                   date_received=date.today(),
                   order_types=order_types_list,
                   multiple_items=True if len(suborder_list) > 1 else False)
    db.session.add(order)

    customer = Customers(billing_name=order_info_dict['name'],
                         shipping_name=order_info_dict['name'],
                         email=order_info_dict.get('email'),
                         address_line_1=order_info_dict.get('addressLine1'),
                         address_line_2=order_info_dict.get('addressLine2'),
                         city=order_info_dict.get('city'),
                         state=order_info_dict.get('NY'),
                         zip_code=order_info_dict.get('zipCode'),
                         phone=order_info_dict.get('phone'),
                         order_number=order.id)
    db.session.add(customer)
    db.session.commit()

    for suborder in suborder_list:
        next_suborder_number = order.next_suborder_number
        suborder_id = order.id + '-' + str(next_suborder_number)

        order_type = suborder['orderType']
        if not suborder.get('certificateNum'):
            if order_type == order_types.BIRTH_CERT:
                order_type = order_types.BIRTH_SEARCH
            elif order_type == order_types.DEATH_CERT:
                order_type = order_types.DEATH_SEARCH
            elif order_type == order_types.MARRIAGE_CERT:
                order_type = order_types.MARRIAGE_SEARCH

        new_suborder = Suborders(id=suborder_id,
                                 order_type=order_type,
                                 order_number=order.id,
                                 _status=suborder['status'])
        db.session.add(new_suborder)
        db.session.commit()

        new_suborder.es_create()

        event = Events(suborder_number=new_suborder.id,
                       type_=event_type.INITIAL_IMPORT,
                       user_email=current_user.email,
                       previous_value=None,
                       new_value={
                           'status': new_suborder.status,
                       })

        db.session.add(event)
        db.session.commit()

        handler_for_order_type = {
            order_types.BIRTH_CERT: _create_new_birth_object,
            order_types.DEATH_CERT: _create_new_death_object,
            order_types.MARRIAGE_CERT: _create_new_marriage_object,
            order_types.TAX_PHOTO: _create_new_tax_photo,
            order_types.PHOTO_GALLERY: _create_new_photo_gallery
        }

        handler_for_order_type[suborder['orderType']](suborder, new_suborder)


def _create_new_birth_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificateNum')

    if certificate_number:
        birth_object = BirthCertificate(certificate_number=certificate_number,
                                        first_name=suborder.get('firstName'),
                                        last_name=suborder['lastName'],
                                        middle_name=suborder.get('middleName'),
                                        gender=suborder.get('gender'),
                                        father_name=suborder.get('fatherName'),
                                        mother_name=suborder.get('motherName'),
                                        num_copies=suborder['numCopies'],
                                        month=suborder.get('month'),
                                        day=suborder.get('day'),
                                        years=[y['value'] for y in suborder.get('years') if y['value']],
                                        birth_place=suborder.get('birthPlace'),
                                        borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                        letter=suborder.get('letter'),
                                        comment=suborder.get('comment'),
                                        _delivery_method=suborder['deliveryMethod'],
                                        suborder_number=new_suborder_obj.id)
    else:
        birth_object = BirthSearch(first_name=suborder.get('firstName'),
                                   last_name=suborder['lastName'],
                                   middle_name=suborder.get('middleName'),
                                   gender=suborder.get('gender'),
                                   father_name=suborder.get('fatherName'),
                                   mother_name=suborder.get('motherName'),
                                   num_copies=suborder['numCopies'],
                                   month=suborder.get('month'),
                                   day=suborder.get('day'),
                                   years=[y['value'] for y in suborder.get('years') if y['value']],
                                   birth_place=suborder.get('birthPlace'),
                                   borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                   letter=suborder.get('letter'),
                                   comment=suborder.get('comment'),
                                   _delivery_method=suborder['deliveryMethod'],
                                   suborder_number=new_suborder_obj.id)
    db.session.add(birth_object)
    db.session.commit()

    new_suborder_obj.es_update(birth_object.serialize)


def _create_new_death_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificateNum')

    if certificate_number:
        death_object = DeathCertificate(certificate_number=certificate_number,
                                        last_name=suborder['lastName'],
                                        first_name=suborder.get('firstName'),
                                        middle_name=suborder.get('middleName'),
                                        num_copies=suborder['numCopies'],
                                        cemetery=suborder.get('cemetery'),
                                        month=suborder.get('month'),
                                        day=suborder.get('day'),
                                        years=[y['value'] for y in suborder.get('years') if y['value']],
                                        death_place=suborder.get('deathPlace'),
                                        borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                        letter=suborder.get('letter'),
                                        comment=suborder.get('comment'),
                                        _delivery_method=suborder['deliveryMethod'],
                                        suborder_number=new_suborder_obj.id)
    else:
        death_object = DeathSearch(last_name=suborder['lastName'],
                                   first_name=suborder.get('firstName'),
                                   middle_name=suborder.get('middleName'),
                                   num_copies=suborder['numCopies'],
                                   cemetery=suborder.get('cemetery'),
                                   month=suborder.get('month'),
                                   day=suborder.get('day'),
                                   years=[y['value'] for y in suborder.get('years') if y['value']],
                                   death_place=suborder.get('deathPlace'),
                                   borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                   letter=suborder.get('letter'),
                                   comment=suborder.get('comment'),
                                   _delivery_method=suborder['deliveryMethod'],
                                   suborder_number=new_suborder_obj.id)
    db.session.add(death_object)
    db.session.commit()

    new_suborder_obj.es_update(death_object.serialize)


def _create_new_marriage_object(suborder: Dict[str, Union[str, List[Dict]]], new_suborder_obj: Suborders):
    certificate_number = suborder.get('certificateNum')

    if certificate_number:
        marriage_object = MarriageCertificate(certificate_number=certificate_number,
                                              groom_last_name=suborder['groomLastName'],
                                              groom_first_name=suborder.get('groomFirstName'),
                                              bride_last_name=suborder['brideLastName'],
                                              bride_first_name=suborder.get('brideFirstName'),
                                              num_copies=suborder['numCopies'],
                                              month=suborder.get('month'),
                                              day=suborder.get('day'),
                                              years=[y['value'] for y in suborder.get('years') if y['value']],
                                              marriage_place=suborder.get('marriagePlace'),
                                              borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                              letter=suborder.get('letter'),
                                              comment=suborder.get('comment'),
                                              _delivery_method=suborder['deliveryMethod'],
                                              suborder_number=new_suborder_obj.id)
    else:
        marriage_object = MarriageSearch(groom_last_name=suborder['groomLastName'],
                                         groom_first_name=suborder.get('groomFirstName'),
                                         bride_last_name=suborder['brideLastName'],
                                         bride_first_name=suborder.get('brideFirstName'),
                                         num_copies=suborder['numCopies'],
                                         month=suborder.get('month'),
                                         day=suborder.get('day'),
                                         years=[y['value'] for y in suborder.get('years') if y['value']],
                                         marriage_place=suborder.get('marriagePlace'),
                                         borough=[b['name'].upper() for b in suborder['boroughs'] if b['checked']],
                                         letter=suborder.get('letter'),
                                         comment=suborder.get('comment'),
                                         _delivery_method=suborder['deliveryMethod'],
                                         suborder_number=new_suborder_obj.id)
    db.session.add(marriage_object)
    db.session.commit()

    new_suborder_obj.es_update(marriage_object.serialize)


def _create_new_tax_photo(suborder: Dict[str, str], new_suborder_obj: Suborders):
    new_collection = suborder['collection']

    if new_collection in [collection.YEAR_1940, collection.BOTH]:
        tax_photo_1940 = TaxPhoto(collection=collection.YEAR_1940,
                                  borough=suborder['borough'],
                                  roll=suborder.get('roll'),
                                  block=suborder.get('block'),
                                  lot=suborder.get('lot'),
                                  building_number=suborder['buildingNum'],
                                  street=suborder['street'],
                                  description=suborder.get('description'),
                                  size=suborder['size'],
                                  num_copies=suborder['numCopies'],
                                  _delivery_method=suborder['deliveryMethod'],
                                  contact_number=suborder.get('contactNum'),
                                  suborder_number=new_suborder_obj.id)
        db.session.add(tax_photo_1940)
        db.session.commit()

        new_suborder_obj.es_update(tax_photo_1940.serialize)

    if new_collection in [collection.YEAR_1980, collection.BOTH]:
        tax_photo_1980 = TaxPhoto(collection=collection.YEAR_1980,
                                  borough=suborder['borough'].title(),
                                  block=suborder.get('block'),
                                  lot=suborder.get('lot'),
                                  building_number=suborder['buildingNum'],
                                  street=suborder['street'],
                                  description=suborder.get('description'),
                                  size=suborder['size'],
                                  num_copies=suborder['numCopies'],
                                  _delivery_method=suborder['deliveryMethod'],
                                  contact_number=suborder.get('contactNum'),
                                  suborder_number=new_suborder_obj.id)
        db.session.add(tax_photo_1980)
        db.session.commit()

        new_suborder_obj.es_update(tax_photo_1980.serialize)


def _create_new_photo_gallery(suborder: Dict[str, str], new_suborder_obj: Suborders):
    photo_gallery = PhotoGallery(image_id=suborder['imageID'],
                                 description=suborder.get('description'),
                                 additional_description=suborder.get('additionalDescription'),
                                 size=suborder['size'],
                                 num_copies=suborder.get('numCopies'),
                                 _delivery_method=suborder['deliveryMethod'],
                                 contact_number=suborder.get('contactNum'),
                                 comment=suborder.get('comment'),
                                 suborder_number=new_suborder_obj.id)
    db.session.add(photo_gallery)
    db.session.commit()

    new_suborder_obj.es_update(photo_gallery.serialize)
