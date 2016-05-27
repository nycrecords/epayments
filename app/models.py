from . import db
from . import app

class Order(db.Model):
    __tablename__ = 'order'
    order_no = db.Column(db.Integer, primary_key=True)
    client_agency_name = db.Column(db.String, nullable=False)
    ship_to_name = db.Column(db.String)
    ship_to_street_address_one = db.Column(db.String)
    ship_to_street_address_two = db.Column(db.String)
    ship_to_city = db.Column(db.String)
    ship_to_state = db.Column(db.String)
    ship_to_zip_code = db.Column(db.String)
    ship_to_country = db.Column(db.String)
    ship_to_phone = db.Column(db.String)
    customer_email = db.Column(db.String)
    shipping_instructions = db.Column(db.String)
    clients_data = db.Column(db.String)
    confirmation_message = db.Column(db.String)
    date_received = db.Column(db.DateTime)
    billing_name = db.Column(db.String)
    date_last_modified = db.Column(db.DateTime)
    sub_order_no = db.Column(db.Integer)
    client_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        """
        Creates a new order in the database
        :param order_no: Order Number
        :param client_agency_nam: Line of Business
        :param ship_to_name: Customer Name for Shipping
        :param ship_to_street_address_one: Address, Line 1
        :param ship_to_street_address_two: Address, Line 2
        :param ship_to_city: Shipping City
        :param ship_to_state: Shipping State
        :param ship_to_zip_code: Shipping Zip Code
        :param ship_to_country: Shipping Country
        :param ship_to_phone: Shipping Phone (Customer)
        :param customer_email: Customer's email address
        :param shipping_instructions: Shipping Instructions
        :param clients_data: Order Information as Pipe Delimited String
        :param confirmation_message: Confirmation Message (sent to customer)
        :param date_received: Date request was entered into system
        :param billing_name: Billing Customer Name
        :param date_last_modified: Date order was modified on system
        :param sub_order_no: Sub Order Number (used by multi-part orders)
        :param client_id): Line of Business ID #
        """
        super(Order, self).__init__(**kwargs)

        return self.order_no
