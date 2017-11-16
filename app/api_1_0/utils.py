from app import db
from datetime import date, datetime
from sqlalchemy import or_
from app.models import StatusTracker, Orders, Suborders, Customer


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
    photolist = {'photo tax', 'photo gallery', 'property tax'}
    other = {'multiple items in cart', 'vital records and photos in cart'}

    filter_args = []
    for name, value, col in [
        ("order_no", order_no, Orders.id),
        ("suborder_no", suborder_no, Suborders.id),
        ("order_type", order_type, Suborders.client_agency_name),
        ("billing_name", billing_name, Customer.billing_name),
        ("date_submitted_start", date_submitted_start, Orders.date_submitted),
        ("date_submitted_end", date_submitted_end, Orders.date_submitted)
    ]:
        if value:
            if name == 'order_type':
                if value not in ['all', 'multiple_items', 'vital_records']:
                    filter_args.append(
                        col.__eq__(value)
                    )
                elif value == 'multiple_items':
                    filter_args.append(
                        Orders.order_types.contains(',')
                    )
                elif value == 'vital_records':
                    filter_args.append(
                        or_(*[Orders.order_types.any(name) for name in vital_records_list])
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

    base_query = Suborders.query.join(Orders, Customer).filter(*filter_args)
    return [suborder.serialize for suborder in base_query.all()]

    # orders = Orders.query.filter(Orders.date_received >= date_received, Orders.date_received <= date_submitted)
    # if date_submitted_start and date_submitted_end:
    #     date_submitted_start = datetime.strptime(date_submitted_start, "%m/%d/%Y")
    #     date_submitted_end = datetime.strptime(date_submitted_end, "%m/%d/%Y")
    #     orders = Orders.query.filter(Orders.date_received >= date_submitted_start, Orders.date_submitted <= date_submitted_end)

    # if len(order_number) != 0:
    #     orders = orders.filter(Orders.order_no == order_number)
    # if len(suborder_number) != 0:
    #     orders = orders.filter(Orders.suborder_no == suborder_number)
    # if len(billing_name) != 0:
    #     orders = orders.filter(func.lower(Orders.billing_name).contains(func.lower(billing_name)))
    #
    # if order_type != '' and order_type not in ['all', 'multiple_items', 'vital_records_and_photos']:
    #     orders = orders.filter(Orders.client_agency_name == order_type)
    # elif order_type == 'multiple_items':
    #     orders = [order for order in orders if len(order.ordertypes.split(',')) > 1]
    # elif order_type == 'vital_records_and_photos':
    #     orders = [order for order in orders if
    #               not set(order.ordertypes.split(',')).isdisjoint(vitalrecordslist) and not set(order.ordertypes.split(
    #                   ',')).isdisjoint(photolist)]
    # order_list = [order.serialize for order in orders]
    #
    # return order_list
