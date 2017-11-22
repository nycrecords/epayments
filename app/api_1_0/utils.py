from flask import render_template
from flask_login import current_user
from sqlalchemy import or_
from xhtml2pdf.pisa import CreatePDF

from app import db
from app.constants import (
    order_types,
    event_type,
    printing
)
from app.constants.customer import EMPTY_CUSTOMER
from app.models import (
    Order,
    Suborder,
    Customer,
    BirthSearch,
    BirthCertificate,
    DeathSearch,
    DeathCertificate,
    MarriageSearch,
    MarriageCertificate,
    PhotoGallery,
    PhotoTax,
    PropertyCard,
    Users,
    Event
)


def _order_query_filters(order_number, suborder_number, order_type, billing_name, user, date_submitted_start,
                         date_submitted_end):
    # TODO: Need to refactor get_order_by_fields so that it performs a single function for code reuse.
    vital_records_list = ['Birth cert', 'Marriage cert', 'Death cert']  # TODO: Searches are missing from here. @gzhou??
    photo_list = ['photo tax', 'photo gallery', 'property card']

    filter_args = []
    for name, value, col in [
        ("order_number", order_number, Order.id),
        ("suborder_number", suborder_number, Suborder.id),
        ("order_type", order_type, Suborder.client_agency_name),
        ("billing_name", billing_name, Customer.billing_name),
        ("date_submitted_start", date_submitted_start, Order.date_submitted),
        ("date_submitted_end", date_submitted_end, Order.date_submitted)
    ]:
        if value:
            if name == 'order_type':
                if value not in ['all', 'multiple_items', 'vital_records', 'vital_records_and_photos']:
                    filter_args.append(
                        col.__eq__(value)
                    )
                elif value == 'multiple_items':
                    filter_args.append(
                        Order.multiple_items.__eq__(True)
                    )
                elif value == 'vital_records':
                    filter_args.append(
                        or_(*[Order.order_types.any(name) for name in vital_records_list])
                    )
                elif value == 'photos':
                    filter_args.append(
                        or_(*[Order.order_types.any(name) for name in photo_list])
                    )
                elif value == 'vital_records_and_photos':
                    vital_records_list.extend(photo_list)
                    filter_args.append(
                        or_(*[Order.order_types.any(name) for name in vital_records_list])
                    )
            elif name == 'date_submitted_start':
                filter_args.append(
                    col.__ge__(value)
                )
            elif name == 'date_submitted_end':
                filter_args.append(
                    col.__le__(value)
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
    suborder = Suborder.query.filter_by(id=suborder_number).one()
    if new_status != suborder.status:
        prev_event = Event.query.filter(Event.suborder_number == suborder_number,
                                        Event.new_value['status'].astext == suborder.status).order_by(
            Event.timestamp.desc()).first()

        previous_value = {}
        new_value = {}

        previous_value['status'] = suborder.status
        if 'comment' in prev_event.new_value:
            previous_value['comment'] = prev_event.new_value['comment']

        new_value['status'] = new_status
        if comment:
            new_value['comment'] = comment

        suborder.status = new_status

        event = Event(suborder_number,
                      event_type.UPDATE_STATUS,
                      current_user.email,
                      previous_value,
                      new_value)

        db.session.add(event)
        db.session.commit()

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
    p_tax = PhotoTax.query.filter_by(suborder_number=suborder_number).one()

    previous_value = {
        'block': p_tax.block,
        'lot': p_tax.lot,
        'roll': p_tax.roll
    }

    p_tax.block = block_no
    p_tax.lot = lot_no
    p_tax.roll = roll_no

    db.session.add(p_tax)
    db.session.commit()

    new_value = {
        'block': p_tax.block,
        'lot': p_tax.lot,
        'roll': p_tax.roll
    }

    event = Event(suborder_number,
                  event_type.UPDATE_PHOTO_TAX,
                  current_user.email,
                  previous_value,
                  new_value)

    db.session.add(event)
    db.session.commit()



def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, user, date_submitted_start,
                         date_submitted_end):
    """
    Filter orders by fields received
    get_orders_by_fields(client_id, suborder_number, order_type(Death Search or Marriage Search), billing_name
                         user??, date_received, date_submitted)
    :return:
    """
    filter_args = _order_query_filters(order_number, suborder_number, order_type, billing_name, user,
                                       date_submitted_start,
                                       date_submitted_end)
    base_query = Suborder.query.join(Order, Customer).filter(*filter_args)
    order_count = base_query.distinct(Suborder.order_number).group_by(Suborder.order_number, Suborder.id).count()
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
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    filter_args = _order_query_filters(order_number, suborder_number, order_type, billing_name, user,
                                       date_submitted_start,
                                       date_submitted_end)

    suborders = Suborder.query.join(Order, Customer).filter(*filter_args).all()

    order_type_template_handler = {
        order_types.BIRTH_SEARCH: 'birth_search.html',
        order_types.BIRTH_CERT: 'birth_cert.html',
        order_types.MARRIAGE_SEARCH: 'marriage_search.html',
        order_types.MARRIAGE_CERT: 'marriage_cert.html',
        order_types.DEATH_SEARCH: 'death_search.html',
        order_types.DEATH_CERT: 'death_cert.html',
        order_types.PHOTO_TAX: 'photo_tax.html',
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
        order_types.PHOTO_TAX: PhotoTax,
        order_types.PHOTO_GALLERY: PhotoGallery,
        order_types.PROPERTY_CARD: PropertyCard,
    }

    html = ''
    for item in suborders:
        order_info = order_type_models_handler[item.client_agency_name].query.filter_by(
            suborder_number=item.id).one().serialize
        order_info['customer'] = item.order.customer.serialize
        order_info['order'] = item.order.serialize

        order_info['client_agency_name'] = item.client_agency_name
        html += render_template("orders/{}".format(order_type_template_handler[item.client_agency_name]),
                                order_info=order_info)

    from tempfile import NamedTemporaryFile

    tempFileObj = NamedTemporaryFile(mode='w+b', suffix='jpg')
    pdf = CreatePDF(src=html, dest=tempFileObj)
    tempFileObj.seek(0, 0)

    return tempFileObj


def _print_small_labels(search_params):
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get("order_number")
    suborder_number = search_params.get("suborder_number")
    order_type = search_params.get("order_type")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    filter_args = _order_query_filters(order_number, suborder_number, order_type, billing_name, user,
                                       date_submitted_start,
                                       date_submitted_end)

    suborders = Suborder.query.join(Order, Customer).filter(*filter_args).all()

    customers = [suborder.order.customer.serialize for suborder in suborders]

    customers = sorted(customers, key=lambda customer: customer['billing_name'])

    labels = [customers[i:i + printing.SMALL_LABEL_COUNT] for i in range(0, len(customers), printing.SMALL_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.SMALL_LABEL_COUNT:
            for i in range(printing.SMALL_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/small_labels.html', labels=page)

    from tempfile import NamedTemporaryFile

    tempFileObj = NamedTemporaryFile(mode='w+b', suffix='pdf')
    pdf = CreatePDF(src=html, dest=tempFileObj)
    tempFileObj.seek(0, 0)

    return tempFileObj


def _print_large_labels(search_params):
    """

    :param search_params:
    :return:
    """
    order_number = search_params.get("order_number")
    suborder_number = search_params.get("suborder_number")
    order_type = search_params.get("order_type")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_submitted_start = search_params.get("date_submitted_start")
    date_submitted_end = search_params.get("date_submitted_end")

    filter_args = _order_query_filters(order_number, suborder_number, order_type, billing_name, user,
                                       date_submitted_start,
                                       date_submitted_end)

    suborders = Suborder.query.join(Order, Customer).filter(*filter_args).all()

    customers = [suborder.order.customer.serialize for suborder in suborders]

    customers = sorted(customers, key=lambda customer: customer['billing_name'])

    labels = [customers[i:i + printing.LARGE_LABEL_COUNT] for i in range(0, len(customers), printing.LARGE_LABEL_COUNT)]
    html = ''

    for page in labels:
        if len(page) < printing.LARGE_LABEL_COUNT:
            for i in range(printing.LARGE_LABEL_COUNT - len(page)):
                page.append(EMPTY_CUSTOMER)

        html += render_template('orders/large_labels.html', labels=page)

    from tempfile import NamedTemporaryFile

    tempFileObj = NamedTemporaryFile(mode='w+b', suffix='pdf')
    pdf = CreatePDF(src=html, dest=tempFileObj)
    tempFileObj.seek(0, 0)

    return tempFileObj


def generate_csv():
    pass
