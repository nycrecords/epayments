from app import db, es
from app.constants import order_types, status
from sqlalchemy.dialects.postgresql import ARRAY


class Orders(db.Model):
    """
    Define the new Orders class with the following Columns & relationships

    order_number -- Column: String(64)
    date_submitted -- Column: DateTime -- date order was submitted
    date_received -- Column: DateTime -- day we receive order
    confirmation_message -- Column: Text
    client_data -- Column: Text
    order_types -- Column: Array -- type(s) of order(s)
    multiple_items -- Column: Boolean -- whether an order has multiple items
    """

    __tablename__ = 'orders'
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False)
    date_received = db.Column(db.DateTime, nullable=True)
    confirmation_message = db.Column(db.Text, nullable=False)
    client_data = db.Column(db.Text, nullable=False)
    order_types = db.Column(ARRAY(db.Text), nullable=True)
    multiple_items = db.Column(db.Boolean, nullable=False)
    suborder = db.relationship('Suborders', backref='suborders', lazy=True)
    customer = db.relationship('Customers', backref='customers', uselist=False)

    def __init__(
            self,
            id,
            date_submitted,
            date_received,
            confirmation_message,
            client_data,
            order_types,
            multiple_items):
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

    #Elastic Search


class Suborders(db.Model):
    """

    """
    __tablename__ = 'suborders'
    id = db.Column(db.String(32), primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    order_type = db.Column(
        db.Enum(
            order_types.BIRTH_SEARCH,
            order_types.BIRTH_CERT,
            order_types.MARRIAGE_SEARCH,
            order_types.MARRIAGE_CERT,
            order_types.DEATH_SEARCH,
            order_types.DEATH_CERT,
            order_types.TAX_PHOTO,
            order_types.PHOTO_GALLERY,
            order_types.PROPERTY_CARD,
            name='order_type'), nullable=False)
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
            status.REFUNDED,
            status.DONE,
            name='status'), nullable=True)

    order = db.relationship('Orders', backref='orders', uselist=False)
    # TODO: 'polymorphic_on': order_type
    tax_photo = db.relationship(
        'TaxPhoto',
        primaryjoin='Suborders.id==TaxPhoto.suborder_number',
        uselist=False
    )
    photo_gallery = db.relationship(
        'PhotoGallery',
        primaryjoin='Suborders.id==PhotoGallery.suborder_number',
        uselist=False
    )

    def __init__(
            self,
            id,
            client_id,
            order_type,
            order_number,
            _status):
        self.id = id
        self.client_id = client_id
        self.order_type = order_type
        self.order_number = order_number
        self.status = _status

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'order_number': self.order_number,
            'suborder_number': self.id,
            'date_submitted': self.order.date_submitted.strftime("%x %I:%M %p"),
            'date_received': self.order.date_received.strftime("%x %I:%M %p"),
            'billing_name': self.order.customer.billing_name,
            'customer_email': self.order.customer.email,
            'order_type': self.order_type,
            'current_status': self.status
        }


    #Elastic Search
    def es_create(self):
        """Creates Elastic Search doc"""
        es.create(
            index='suborders',
            doc_type='suborders',
            id=self.id,
            body={
                'order_number': self.order_number,
                'suborder_number': self.id,
                'date_submitted': self.order.date_submitted.strftime("%x %I:%M %p"),
                'current_status': self.status,
                'billing_name': self.order.customer.billing_name,
                'customer_email': self.order.customer.email,
                'order_type': self.order_type,
                'data_received': self.order.date_received.strftime('%x %I:%M %p')
            }
        )

    def es_update(self):
        es.update(
            index='suborders',
            doc_type='suborders',
            id=self.id,
            body={
                'doc':{
                    'order_number': self.order_number,
                    'suborder_number': self.id,
                    'date_submitted': self.order.date_submitted.strftime("%x %I:%M %p"),
                    'current_status': self.status,
                    'billing_name': self.order.customer.billing_name,
                    'customer_email': self.order.customer.email,
                    'order_type': self.order_type,
                    'data_received': self.order.date_received.strftime('%x %I:%M %p')
                }
            }
        )