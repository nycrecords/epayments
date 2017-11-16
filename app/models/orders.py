from app import db
from app.constants import status
from datetime import datetime
from pytz import timezone
from sqlalchemy.dialects.postgresql import ARRAY


class Orders(db.Model):
    """
    Define the new Order class with the following Columns & relationships

    order_number -- Column: String(64)
    suborder_no -- Column: BigInteger, PrimaryKey
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
    suborders = db.relationship('Suborders', backref='suborders', lazy=True)
    customer = db.relationship('Customer', backref='customer', uselist=False)

    def __init__(
            self,
            id,
            date_submitted,
            date_received,
            confirmation_message,
            client_data,
            order_types,

    ):
        self.id = id
        self.date_submitted = date_submitted
        self.date_received = date_received or None
        self.confirmation_message = confirmation_message
        self.client_data = client_data
        self.order_types = order_types


class Suborders(db.Model):
    """

    """
    __tablename__ = 'suborders'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    client_agency_name = db.Column(db.String(64), nullable=False)
    order_no = db.Column(db.String(64), db.ForeignKey('orders.id'), nullable=False)
    status = db.relationship('StatusTracker', backref=db.backref('suborders'), lazy='dynamic')
    order = db.relationship('Orders', backref='orders', uselist=False)

    def __init__(
            self,
            id,
            client_id,
            client_agency_name,
            order_no
    ):
        self.id = id
        self.client_id = client_id
        self.client_agency_name = client_agency_name
        self.order_no = order_no

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'order_no': self.order_no,
            'suborder_no': self.id,
            'date_submitted': self.order.date_submitted.strftime("%x %I:%M %p"),
            'date_received': self.order.date_received,
            'billing_name': self.order.customer.billing_name,
            'customer_email': self.order.customer.email,
            'client_agency_name': self.client_agency_name,
            'current_status': self.status.filter_by(suborder_no=self.id)
                                         .order_by(StatusTracker.id.desc()).first().current_status
        }


class StatusTracker(db.Model):

    """
    Need to make a model that will change the status of the
    process of the document

    id - db.Integer , primary key = true
    suborder_no - Column: BigInteger, Foreign Key - connects the sub_order# to the top of this database
    status - Column: Enum - Tracks the status of the order can only be these set things
    comment - Column: db.String(64) - stores the comment that was passed in
    timestamp - Column: db.datetime - holds the time that the status was updated
    previous_value - Column: db.String(25) - Stores the previous status

    1. Received || Set to this by default
    2. Processing
        a)found
        b)printed
    3. Mailed/Pickup
    4. Not_Found
        a)Letter_generated
        b)Undeliverable - Cant move down the line
    5. Done - End of status changes

    """
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborders.id'), nullable=False)
    current_status = db.Column(
        db.Enum(
            status.RECEIVED,
            status.PROCESSING,
            status.FOUND,
            status.MAILED_PICKUP,
            status.NOT_FOUND,
            status.LETTER_GENERATED,
            status.UNDELIVERABLE,
            status.DONE,
            name='current_status'), nullable=True)
    comment = db.Column(db.String(64), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_value = db.Column(db.String(25), nullable=True)

    # Class Constructor to initialize the data
    def __init__(
                self,
                suborder_no,
                current_status,
                comment,
                timestamp,
                previous_value,
    ):
        self.suborder_no = suborder_no
        self.current_status = current_status
        self.comment = comment or None
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))
        self.previous_value = previous_value or None

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'suborder_no': self.suborder_no,
            'current_status': self.current_status,
            'comment': self.comment,
            'timestamp': self.timestamp.strftime("%x %I:%M %p"),
            'previous_value': self.previous_value,
        }
