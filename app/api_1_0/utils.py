from app import db
from datetime import date, datetime, timedelta
from ..models import StatusTracker, Orders
from sqlalchemy import func, databases, update, desc

def update_status(sub_order_no, comment, new_status):
    """
        POST: {sub_order_no, new_status, comment};
        returns: {status_id, sub_order_no, status, comment}, 201

    Take in the info, this function only gets called if the form is filled
     - access the db to get the status_id for this particular order
     - now create a new row in the db in the status table with
     - this row should have a status_id + 1 then the highest status row
     - 1) it will have the same sub_order_no
     - 2) it will have the comment that was passed in or None
     - 3) it will have the new status that was passed from the user
    """

    current_time = datetime.utcnow()
    # ten_weeks_ago = current_time - datetime.timedelta(weeks=10)

    """ orders = Orders.query.filter(Orders.date_received >= date_received, Orders.date_received <= date_submitted) """

    object_ = StatusTracker.query.filter_by(sub_order_no=sub_order_no).order_by(StatusTracker.timestamp.desc()).first()

    if object_ is not None:
        previous_value = object_.current_status
    else:
        previous_value = object_.current_status

    insert_status = StatusTracker(sub_order_no=sub_order_no,
                                  current_status=new_status,
                                  comment=comment,
                                  timestamp=current_time,
                                  previous_value=previous_value)

    db.session.add(insert_status)
    db.session.commit()


def get_orders_by_fields(order_number, suborder_number, order_type, billing_name, user, date_received,
                         date_submitted):
    """
    Filter orders by fields received
    get_orders_by_fields(client_id, suborder_no, order_type(Death Search or Marriage Search), billing_name
                         user??, date_received, date_submitted)
    :return:
    """
    vitalrecordslist = {'Birth search', 'Birth cert', 'Marriage search', 'Marriage cert', 'Death search', 'Death cert'}
    photolist = {'tax photo', 'online gallery', 'prop card'}
    yesterday = datetime.strptime(date.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    orders = Orders.query.filter(Orders.date_received >= date_received, Orders.date_received <= date_submitted)
    if len(date_received) < 1:
        date_received_start = yesterday  # set the date received start to yesterday if nothing passed in form
    if len(date_submitted) < 1:
        date_received_end = yesterday  # set the date received end to yesterday if nothing passed in form
    orders = Orders.query.filter(Orders.date_received >= date_received, Orders.date_received <= date_submitted)
    if len(order_number) != 0:
        orders = orders.filter(Orders.client_id == order_number)
    if len(suborder_number) != 0:
        orders = orders.filter(Orders.suborderno == suborder_number)
    if len(billing_name) != 0:
        orders = orders.filter(func.lower(Orders.billing_name).contains(func.lower(billing_name)))
    if len(order_type) != 4 and order_type not in ['All', 'multipleitems', 'vitalrecordsphotos']:
        orders = orders.filter(Orders.client_agency_name == order_type)
    elif order_type == 'multipleitems':
        orders = [order for order in orders if len(order.ordertypes.split(',')) > 1]
    elif order_type == 'vitalrecordsphotos':
        orders = [order for order in orders if
                  not set(order.ordertypes.split(',')).isdisjoint(vitalrecordslist) and not set(order.ordertypes.split(
                      ',')).isdisjoint(photolist)]
    order_list = [order.serialize for order in orders]
    return order_list
