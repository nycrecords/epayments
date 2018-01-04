from app import db
from app.constants import status
from sqlalchemy.dialects.postgresql import ARRAY


class Order(db.Model):
    """
    Define the new Order class with the following Columns & relationships

    order_number -- Column: String(64)
    suborder_number -- Column: BigInteger, PrimaryKey
    date_submitted -- Column: DateTime -- date order was submitted
    date_received -- Column: DateTime -- day we receive order
    billing_name -- Column: String(64)
    customer_email -- Column: String(64)
    confirmation_message -- Column: Text
    client_data -- Column: Text
    client_id -- Column: Integer
    client_agency_name -- Column: String(64)
    """

    __tablename__ = 'orders'
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=True)
    confirmation_message = db.Column(db.Text, nullable=False)
    client_data = db.Column(db.Text, nullable=False)
    order_types = db.Column(ARRAY(db.Text), nullable=True)
    multiple_items = db.Column(db.Boolean, nullable=False)
    suborder = db.relationship('Suborder', backref='suborder', lazy=True)
    customer = db.relationship('Customer', backref='customer', uselist=False)

    def __init__(
            self,
            id,
            date_submitted,
            date_received,
            confirmation_message,
            client_data,
            order_types,
            multiple_items

    ):
        self.id = id
        self.date_submitted = date_submitted
        self.date_received = date_received or None
        self.confirmation_message = confirmation_message
        self.client_data = client_data
        self.order_types = order_types
        self.multiple_items = multiple_items

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'order_number': self.id,
            'date_submitted': self.date_submitted.strftime("%x %I:%M %p"),
            'date_received': self.date_received.strftime("%x %I:%m %p"),
            'confirmation_message': self.confirmation_message,
            'client_data': self.client_data,
            'order_types': self.order_types,
            'multiple_items': self.multiple_items,
        }


class Suborder(db.Model):
    """

    """
    __tablename__ = 'suborders'
    id = db.Column(db.String(32), primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    client_agency_name = db.Column(db.String(64), nullable=False)
    order_number = db.Column(db.String(64), db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(
        db.Enum(
            status.RECEIVED,
            status.PROCESSING,
            status.FOUND,
            status.PRINTED,
            status.MAILED_PICKUP,
            status.NOT_FOUND,
            status.LETTER_GENERATED,
            status.UNDELIVERABLE,
            status.DONE,
            name='status'), nullable=True)
    order = db.relationship('Order', backref='orders', uselist=False)

    def __init__(
            self,
            id,
            client_id,
            client_agency_name,
            order_number,
            status
    ):
        self.id = id
        self.client_id = client_id
        self.client_agency_name = client_agency_name
        self.order_number = order_number
        self.status = status

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'order_number': self.order_number,
            'suborder_number': self.id,
            'date_submitted': self.order.date_submitted.strftime("%x %I:%M %p"),
            'date_received': self.order.date_received,
            'billing_name': self.order.customer.billing_name,
            'customer_email': self.order.customer.email,
            'client_agency_name': self.client_agency_name,
            'current_status': self.status
        }
