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
    photo_list = ['photo tax', 'photo gallery', 'property card']

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
                if value not in ['all', 'multiple_items', 'vital_records', 'vital_records_and_photos']:
                    filter_args.append(
                        col.__eq__(value)
                    )
                elif value == 'multiple_items':
                    filter_args.append(
                        Orders.multiple_items.__eq__(True)
                    )
                elif value == 'vital_records':
                    filter_args.append(
                        or_(*[Orders.order_types.any(name) for name in vital_records_list])
                    )
                elif value == 'photos':
                    filter_args.append(
                        or_(*[Orders.order_types.any(name) for name in photo_list])
                    )
                elif value == 'vital_records_and_photos':
                    vital_records_list.extend(photo_list)
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
    order_count = base_query.distinct(Suborders.order_no).group_by(Suborders.order_no, Suborders.id).count()
    suborder_list = base_query.all()
    suborder_count = len(suborder_list)
    return order_count, suborder_count, [suborder.serialize for suborder in suborder_list]
