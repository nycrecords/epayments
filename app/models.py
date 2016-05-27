"""
CREATE TABLE orders
(
    OrderNo REAL,
    ClientAgencyName TEXT,
    ShipToName TEXT,
    ShipToStreetAdd TEXT,
    ShipToStreetAdd2 TEXT,
    ShipToCity TEXT,
    ShipToState TEXT,
    ShipToZipCode TEXT,
    ShipToCountry TEXT,
    ShipToPhone TEXT,
    CustomerEmail TEXT,
    ShippingInstructions TEXT,
    ClientsData TEXT,
    ConfirmationMessage TEXT,
    DateReceived TEXT,
    BillingName TEXT,
    DateLastModified TEXT,
    SubOrderNo REAL,
    ClientID TEXT
);
"""

from . import db


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
