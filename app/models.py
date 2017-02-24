from app import db

class Order(db.Model):
    """
    Define the Order class with the following columns and relationships:

    order_no -- Column: String(64)
    client_agency_name -- Column: String(64)
    ship_to_name -- Column: String(64)
    ship_to_street_add -- Column: String(64)
    ship_to_street_add_2 -- Column: String(64)
    ship_to_city  -- Column: String(64)
    ship_to_state -- Column: String(64)
    ship_to_zipcode -- Column: String(64)
    ship_to_country -- Column: String(64)
    ship_to_phone -- Column: String(64)
    customer_email -- Column: String(64)
    shipping_instructions -- Column: String(64)
    clients_data -- Column: Text
    confirmation_message -- Column: Text
    date_received -- Column: DateTime
    billing_name -- Column: String(64)
    date_last_modified -- Column: DateTime
    sub_order_no -- Column: BigInteger, PrimaryKey
    client_id -- Column: Integer
    order_types -- Column: String(256)
    """
    __tablename__ = 'order'
    order_no = db.Column(db.String(64))
    client_agency_name = db.Column(db.String(64))
    ship_to_name = db.Column(db.String(64))
    ship_to_street_add = db.Column(db.String(64))
    ship_to_street_add_2 = db.Column(db.String(64))
    ship_to_city = db.Column(db.String(64))
    ship_to_state = db.Column(db.String(64))
    ship_to_zipcode = db.Column(db.String(64))
    ship_to_country = db.Column(db.String(64))
    ship_to_phone = db.Column(db.String(64))
    customer_email = db.Column(db.String(64))
    shipping_instructions = db.Column(db.String(64))
    clients_data = db.Column(db.Text)
    confirmation_message = db.Column(db.Text)
    date_received = db.Column(db.DateTime)
    billing_name = db.Column(db.String(64))
    date_last_modified = db.Column(db.DateTime)
    sub_order_no = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.Integer)
    order_types = db.Column(db.String(256))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'orderno': self.order_no,
            'clientagencyname': self.client_agency_name,
            'ship_to_name': self.ship_to_name,
            'ship_to_streetadd': self.ship_to_street_add,
            'ship_to_streetadd2': self.ship_to_street_add_2,
            'ship_to_city': self.ship_to_city,
            'ship_to_state': self.ship_to_state,
            'ship_to_zipcode': self.ship_to_zipcode,
            'ship_to_country': self.ship_to_country,
            'ship_to_phone': self.ship_to_phone,
            'customeremail': self.customer_email,
            'shippinginstructions': self.shipping_instructions,
            'clientsdata': self.clients_data,
            'confirmationmessage': self.confirmation_message,
            'datereceived': str(self.date_received),
            'billingname': self.billing_name,
            'datelastmodified': self.date_last_modified,
            'suborderno': self.sub_order_no,
            'clientid': self.client_id,
            'ordertypes': self.order_types
        }
