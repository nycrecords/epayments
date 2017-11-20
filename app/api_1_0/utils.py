from app import db
from datetime import date, datetime
from sqlalchemy import or_
from app.models import (
    StatusTracker,
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
    PropertyCard
)


def update_status(suborder_no, comment, new_status):
    """
        POST: {suborder_no, new_status, comment};
        returns: {status_id, suborder_no, status, comment}, 201

    Take in the info, this function only gets called if the form is filled
     - access the db to get the status_id for this particular order
     - now create a new row in the db in the status table with
     - this row should have a status_id + 1 then the highest status row
     - 1) it will have the same suborder_no
     - 2) it will have the comment that was passed in or None
     - 3) it will have the new status that was passed from the user
    """

    object_ = StatusTracker.query.filter_by(suborder_no=suborder_no).order_by(StatusTracker.timestamp.desc()).first()

    if object_ is not None:
        previous_value = object_.current_status
    else:
        previous_value = object_.current_status

    insert_status = StatusTracker(suborder_no=suborder_no,
                                  current_status=new_status,
                                  comment=comment,
                                  timestamp=datetime.utcnow(),
                                  previous_value=previous_value)

    db.session.add(insert_status)
    db.session.commit()


def get_orders_by_fields(order_no, suborder_no, order_type, billing_name, user, date_submitted_start,
                         date_submitted_end):
    """
    Filter orders by fields received
    get_orders_by_fields(client_id, suborder_no, order_type(Death Search or Marriage Search), billing_name
                         user??, date_received, date_submitted)
    :return:
    """
    vital_records_list = ['Birth cert', 'Marriage cert', 'Death cert']
    photo_list = ['photo tax', 'photo gallery', 'property card']

    filter_args = []
    for name, value, col in [
        ("order_no", order_no, Order.id),
        ("suborder_no", suborder_no, Suborder.id),
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
    base_query = Suborder.query.join(Order, Customer).filter(*filter_args)
    order_count = base_query.distinct(Suborder.order_no).group_by(Suborder.order_no, Suborder.id).count()
    suborder_list = base_query.all()
    suborder_count = len(suborder_list)
    return order_count, suborder_count, [suborder.serialize for suborder in suborder_list]

def _order_query():
    # TODO: Need to refactor get_order_by_fields so that it performs a single function for code reuse.
    pass

def _print_orders(search_params):
    """
    Generate PDF order sheets.

    :param search_params: JSON Fields from the search form
    :type search_params: JSON

    :return: PDF
    """
    order_number = search_params.get("order_no")
    suborder_number = search_params.get("suborder_no")
    order_type = search_params.get("order_type")
    billing_name = search_params.get("billing_name")
    # user = str(request.form["user"])
    user = ''
    date_received = search_params.get("date_received")
    date_submitted = search_params.get("date_submitted")

    order_count, suborder_count, items = get_orders_by_fields(order_number, suborder_number, order_type, billing_name, user, date_received,
                                  date_submitted)

    order_type_template_handler = {
        order_type.BIRTH_SEARCH: 'birth_search.html',
        order_type.BIRTH_CERT: 'birth_certificate.html',
        order_type.MARRIAGE_SEARCH: 'marriage_search.html',
        order_type.MARRIAGE_CERT: 'marriage_certificate.html',
        order_type.DEATH_SEARCH: 'death_search.html',
        order_type.DEATH_CERT: 'death_certificate.html',
        order_type.PHOTO_TAX: 'photo_tax.html',
        order_type.PHOTO_GALLERY: 'photo_gallery.html',
        order_type.PROPERTY_CARD: 'property_card.html',
    }

    order_type_models_handler = {
        order_type.BIRTH_SEARCH: BirthSearch,
        order_type.BIRTH_CERT: BirthCertificate,
        order_type.MARRIAGE_SEARCH: MarriageSearch,
        order_type.MARRIAGE_CERT: MarriageCertificate,
        order_type.DEATH_SEARCH: DeathSearch,
        order_type.DEATH_CERT: DeathCertificate,
        order_type.PHOTO_TAX: PhotoTax,
        order_type.PHOTO_GALLERY: PhotoGallery,
        order_type.PROPERTY_CARD: PropertyCard,
    }

    for item in items:
        order_info = order_type_models_handler[item.]


def _print_small_labels():
    pass


def _print_large_labels():
    pass


def generate_csv():
    pass


def login_user(username, password):
    pass
