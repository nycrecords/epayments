from app import db
from app.models.orders import Order


class Customer(db.Model):

    """
    Define the Shipping class with the following columns and relationships:

    name -- Column: String(64)
    address_Line_1 -- Column: String(64)
    address_Line_1 -- Column: String(64)
    city -- Column: String(64)
    state -- Column: String(64)
    zip -- Column: String(64)
    country -- Column: String(64)
    phone -- Column: String(64)
    instructions -- Column: String(64)
    order_number -- Column: String(64), foreignKey

    """
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    billing_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    shipping_name = db.Column(db.String(64), nullable=False)
    address_line_1 = db.Column(db.String(64), nullable=True)
    address_line_2 = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=True)
    zip_code = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(64), nullable=True)
    instructions = db.Column(db.String(64), nullable=True)
    order_number = db.Column(db.String(64), db.ForeignKey('order.id'), nullable=False)

    def __init__(
                self,
                billing_name,
                email,
                shipping_name,
                address_line_1,
                address_line_2,
                city,
                state,
                zip_code,
                country,
                phone,
                instructions,
                order_number

    ):
        self.billing_name = billing_name
        self.email = email
        self.shipping_name = shipping_name
        self.address_line_1 = address_line_1 or None
        self.address_line_2 = address_line_2 or None
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone or None
        self.instructions = instructions or None
        self.order_number = order_number

    @property
    def address(self):
        address = ''
        if self.address_line_2 is not None:
            address = "{address_line_one}, {address_line_two}, {city}, {state}, {zip}".format(
                address_line_one=self.address_line_1,
                address_line_two=self.address_line_2,
                city=self.city,
                state=self.state,
                zip=self.zip_code
            )
        else:
            address = "{address_line_one}, {city}, {state}, {zip}".format(
                address_line_one=self.address_line_1,
                city=self.city,
                state=self.state,
                zip=self.zip_code
            )

        if self.country not in ['United States']:
            address += self.country

        return address

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'billing_name': self.billing_name,
            'email': self.email,
            'shipping_name': self.shipping_name,
            'address_line_one': self.address_line_1,
            'address_line_two': self.address_line_2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'phone': self.phone,
            'instructions': self.instructions,
            'order_number': self.order_number,
            'address': self.address
        }
