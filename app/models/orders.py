from app import db
from app .constants import status


class Orders(db.Model):
    """
    Define the new Order class with the following Columns & relationships

    order_number -- Column: String(64)
    sub_order_no -- Column: BigInteger, PrimaryKey
    date_submitted -- Column: DateTime -- date order was submitted
    date_received -- Column: DateTime -- day we receive order
    billing_name -- Column: String(64)
    customer_email -- Column: String(64)
    confirmation_message -- Column: Text
    client_data -- Column: Text

    """

    __tablename__ = 'orders'
    order_no = db.Column(db.String(64))
    sub_order_no = db.Column(db.BigInteger, primary_key=True, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=True)
    billing_name = db.Column(db.String(64), nullable=False)
    customer_email = db.Column(db.String(64), nullable=False)
    confirmation_message = db.Column(db.Text, nullable=False)
    client_data = db.Column(db.Text, nullable=False)

    def __init__(
            self,
            order_no,
            sub_order_no,
            date_submitted,
            billing_name,
            customer_email,
            confirmation_message,
            client_data,
            date_received=None

    ):
        self.order_no = order_no
        self.sub_order_no = sub_order_no
        self.date_submitted = date_submitted
        self.date_received = date_received
        self.billing_name = billing_name
        self.customer_email = customer_email
        self.confirmation_message = confirmation_message
        self.client_data = client_data


class StatusTracker(db.Model):

    """
    Need to make a model that will change the status of the
    process of the document

    id - db.Integer , primary key = true
    sub_order_no - Column: BigInteger, Foreign Key - connects the sub_order# to the top of this database
    status - Column: Enum - Tracks the status of the order can only be these set things

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
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))
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
            name='current_status'), default=status.RECEIVED, nullable=False)

    # Class Constructor to initialize the data
    def __init__(
                self,
                sub_order_no
    ):
        self.sub_order_no = sub_order_no
