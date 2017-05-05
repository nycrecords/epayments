from app import db


class Shipping(db.Model):

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
    order_no -- Column: String(64), foreignKey

    """
    __tablename__ = 'shipping'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    country = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    instructions = db.Column(db.String(64))

    def __init__(
                self,
                name,
                address_line_1,
                address_line_2,
                city,
                state,
                zip_code,
                country,
                phone,
                instructions

    ):
        self.name = name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone
        self.instructions = instructions
