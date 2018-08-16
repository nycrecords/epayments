import csv
from datetime import datetime

from flask import render_template, current_app, url_for
from flask_login import current_user
from os.path import join
from sqlalchemy import asc
from xhtml2pdf.pisa import CreatePDF

from app import db
from app.constants import (
    order_types,
    event_type,
    printing
)
from app.constants.customer import EMPTY_CUSTOMER
from app.constants.order_types import VITAL_RECORDS_LIST, PHOTOS_LIST
from app.models import (
    Orders,
    Suborders,
    Customers,
    BirthSearch,
    BirthCertificate,
    DeathSearch,
    DeathCertificate,
    MarriageSearch,
    MarriageCertificate,
    PhotoGallery,
    TaxPhoto,
    PropertyCard,
    Events
)


def _order_query_filters(order_number, suborder_number, order_type, status, billing_name, user, date_received_start,
                         date_received_end):
    # TODO: Need to refactor get_order_by_fields so that it performs a single function for code reuse.
    filter_args = []
    for name, value, col in [
        ("order_number", order_number, Orders.id),
        ("suborder_number", suborder_number, Suborders.id),
        ("order_type", order_type, Suborders.order_type),
        ("status", status, Suborders.status),
        ("billing_name", billing_name, Customers.billing_name),
        ("date_received_start", date_received_start, Orders.date_received),
        ("date_received_end", date_received_end, Orders.date_received)
    ]:
        if value:
            if name == 'order_type':
                if value not in ['all', 'multiple_items', 'vital_records', 'photos', 'vital_records_and_photos']:
                    filter_args.append(
                        col.__eq__(value)
                    )
                elif value == 'multiple_items':
                    filter_args.append(
                        Orders.multiple_items.__eq__(True)
                    )
                elif value == 'vital_records':
                    filter_args.append(
                        Suborders.order_type.in_(VITAL_RECORDS_LIST)
                    )
                elif value == 'photos':
                    filter_args.append(
                        Suborders.order_type.in_(PHOTOS_LIST)
                    )
                elif value == 'vital_records_and_photos':
                    filter_args.append(
                        # and_(or_(*[Orders.order_types.any(name) for name in VITAL_RECORDS_LIST]),
                        #      or_(*[Orders.order_types.any(name) for name in PHOTOS_LIST]))
                    )
            elif name == 'status':
                if value != 'all':
                    filter_args.append(
                        col.__eq__(value)
                    )
            elif name == 'date_received_start':
                filter_args.append(
                    col.__ge__(value)
                )
            elif name == 'date_received_end':
                filter_args.append(
                    col.__le__(value)
                )
            elif name == 'billing_name':
                filter_args.append(
                    col.ilike(value)
                )
            else:
                filter_args.append(
                    col.__eq__(value)
                )

    return filter_args


def update_status(suborder_number, comment, new_status):
    """
        POST: {suborder_number, new_status, comment};
        returns: {status_id, suborder_number, status, comment}, 201

    Take in the info, this function only gets called if the form is filled
     - access the db to get the status_id for this particular order
     - now create a new row in the db in the status table with
     - this row should have a status_id + 1 then the highest status row
     - 1) it will have the same suborder_number
     - 2) it will have the comment that was passed in or None
     - 3) it will have the new status that was passed from the user
    """
    suborder = Suborders.query.filter_by(id=suborder_number).one()
    if new_status != suborder.status:
        prev_event = Events.query.filter(Events.suborder_number == suborder_number,
                                         Events.new_value['status'].astext == suborder.status).order_by(
            Events.timestamp.desc()).first()

        previous_value = {}
        new_value = {}

        previous_value['status'] = suborder.status
        if 'comment' in prev_event.new_value:
            previous_value['comment'] = prev_event.new_value['comment']

        new_value['status'] = new_status
        if comment:
            new_value['comment'] = comment

        suborder.status = new_status

        event = Events(suborder_number,
                       event_type.UPDATE_STATUS,
                       current_user.email,
                       previous_value,
                       new_value)

        db.session.add(event)
        db.session.commit()
        suborder.es_update()
        return 201
    else:
        return 400
        # TODO: Raise error because new_status can't be the current status


def update_tax_photo(suborder_number, block_no, lot_no, roll_no):
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


def get_orders_by_fields(order_number, suborder_number, order_type, status, billing_name, user, date_received_start,
                         date_received_end):
    """
    Filter orders by fields received
    get_orders_by_fields(client_id, suborder_number, order_type(Death Search or Marriage Search), billing_name
                         user??, date_received, date_received)
    :return:
    """
    filter_args = _order_query_filters(order_number, suborder_number, order_type, status, billing_name, user,
                                       date_received_start,
                                       date_received_end)
    base_query = Suborders.query.join(Orders, Customers).filter(*filter_args)
    order_count = base_query.distinct(Suborders.order_number).group_by(Suborders.order_number, Suborders.id).count()
    suborder_list = base_query.all()
    suborder_count = len(suborder_list)

    return order_count, suborder_count, [suborder.serialize for suborder in suborder_list]


def _print_orders(search_params):
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

    filter_args = _order_query_filters(order_number, suborder_number, order_type, status, billing_name, user,
                                       date_received_start,
                                       date_received_end)

    suborders = Suborders.query.join(Orders, Customers).filter(*filter_args).all()

    order_type_template_handler = {
        order_types.BIRTH_SEARCH: 'birth_search.html',
        order_types.BIRTH_CERT: 'birth_cert.html',
        order_types.MARRIAGE_SEARCH: 'marriage_search.html',
        order_types.MARRIAGE_CERT: 'marriage_cert.html',
        order_types.DEATH_SEARCH: 'death_search.html',
        order_types.DEATH_CERT: 'death_cert.html',
        order_types.TAX_PHOTO: 'tax_photo.html',
        order_types.PHOTO_GALLERY: 'photo_gallery.html',
        order_types.PROPERTY_CARD: 'property_card.html',
    }

    order_type_models_handler = {
        order_types.BIRTH_SEARCH: BirthSearch,
        order_types.BIRTH_CERT: BirthCertificate,
        order_types.MARRIAGE_SEARCH: MarriageSearch,
        order_types.MARRIAGE_CERT: MarriageCertificate,
        order_types.DEATH_SEARCH: DeathSearch,
        order_types.DEATH_CERT: DeathCertificate,
        order_types.TAX_PHOTO: TaxPhoto,
        order_types.PHOTO_GALLERY: PhotoGallery,
        order_types.PROPERTY_CARD: PropertyCard,
    }

    html = ''

    for item in suborders:
        order_info = order_type_models_handler[item.order_type].query.filter_by(
            suborder_number=item.id).one().serialize
        order_info['customer'] = item.order.customer.serialize
        order_info['order'] = item.order.serialize

        order_info['order_type'] = item.order_type
        html += render_template("orders/{}".format(order_type_template_handler[item.order_type]),
                                order_info=order_info)

    filename = 'order_sheets_{username}_{time}.pdf'.format(username=current_user.email, time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_small_labels(search_params):
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

    filter_args = _order_query_filters(order_number, suborder_number, order_type, status, billing_name, user,
                                       date_received_start,
                                       date_received_end)

    suborders = Suborders.query.join(Orders, Customers).filter(*filter_args).all()

    customers = [suborder.order.customer.serialize for suborder in suborders]

    labels = [customers[i:i + printing.SMALL_LABEL_COUNT] for i in range(0, len(customers), printing.SMALL_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.SMALL_LABEL_COUNT:
            for i in range(printing.SMALL_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/small_labels.html', labels=page)

    filename = 'small_labels_{username}_{time}.pdf'.format(username=current_user.email, time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def _print_large_labels(search_params):
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

    filter_args = _order_query_filters(order_number, suborder_number, order_type, status, billing_name, user,
                                       date_received_start,
                                       date_received_end)

    suborders = Suborders.query.join(Orders, Customers).filter(*filter_args).all()

    customers = [suborder.order.customer.serialize for suborder in suborders]

    customers = sorted(customers, key=lambda customer: customer['billing_name'])

    labels = [customers[i:i + printing.LARGE_LABEL_COUNT] for i in range(0, len(customers), printing.LARGE_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.LARGE_LABEL_COUNT:
            for i in range(printing.LARGE_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/large_labels.html', labels=page)

    filename = 'large_labels_{username}_{time}.pdf'.format(username=current_user.email, time=datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(join(current_app.static_folder, 'files', filename), 'w+b') as file_:
        CreatePDF(src=html, dest=file_)

    return url_for('static', filename='files/{}'.format(filename), _external=True)


def generate_csv(search_params):
    order_type = search_params.get('order_type')

    filter_args = _order_query_filters(search_params.get('order_number'),
                                       search_params.get('suborder_number'),
                                       order_type,
                                       search_params.get('status'),
                                       search_params.get('billing_name'),
                                       '',
                                       search_params.get('date_received_start'),
                                       search_params.get('date_received_end'))

    if order_type == 'photos':
        suborders = Suborders.query.join(Orders, Customers).filter(*filter_args).order_by(asc(Suborders.order_type), asc(Orders.date_submitted)).all()
    else:
        suborders = Suborders.query.join(Orders, Customers).filter(*filter_args).all()

    filename = "orders_{}.csv".format(datetime.now().strftime("%m_%d_%Y_at_%I_%M_%p"))
    file = open(join(current_app.static_folder, 'files', filename), 'w')
    writer = csv.writer(file)
    writer.writerow(["Order Number",
                     "Suborder Number",
                     "Date Received",
                     "Customer Name",
                     "Phone",
                     "Email",
                     "Customer Address",
                     "Mail or Pickup",
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
                     "Comment"])

    for suborder in suborders:
        if suborder.tax_photo:
            writer.writerow([suborder.order_number,
                             suborder.id,
                             suborder.order.date_received.strftime('%m-%d-%Y'),
                             suborder.order.customer.billing_name,
                             suborder.tax_photo.contact_number if suborder.tax_photo.contact_number else suborder.order.customer.phone,
                             suborder.order.customer.email,
                             suborder.order.customer.address,
                             "Mail" if suborder.tax_photo.mail else "Pickup",
                             suborder.tax_photo.size,
                             suborder.tax_photo.num_copies,
                             '',
                             suborder.tax_photo.building_number,
                             suborder.tax_photo.street,
                             suborder.tax_photo.collection,
                             suborder.tax_photo.borough,
                             suborder.tax_photo.block,
                             suborder.tax_photo.lot,
                             suborder.tax_photo.roll,
                             '',
                             ])
        elif suborder.photo_gallery:
            writer.writerow([suborder.order_number,
                             suborder.id,
                             suborder.order.date_received.strftime('%m-%d-%Y'),
                             suborder.order.customer.billing_name,
                             suborder.photo_gallery.contact_number if suborder.photo_gallery.contact_number else suborder.order.customer.phone,
                             suborder.order.customer.email,
                             suborder.order.customer.address,
                             "Mail" if suborder.photo_gallery.mail else "Pickup",
                             suborder.photo_gallery.size,
                             suborder.photo_gallery.num_copies,
                             suborder.photo_gallery.image_id,
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             "Yes" if suborder.photo_gallery.comment else "No",
                             ])

    file.close()

    return url_for('static', filename='files/{}'.format(filename), _external=True)
