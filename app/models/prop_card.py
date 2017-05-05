from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class PropertyCard(db.Model):
    """

    Define the class with these following relationships

    borough -- Column: String/Array   //// IS THIS AN ARRAY or ENUM
    block -- Column: String(9)
    lot -- Column: String(9)
    building_no -- Column: String(10)
    street -- Column: String(40)
    description -- Column: String(35)
    certified -- Column: Bool
    mail_pickup -- Column: Bool
    comment -- Column: String(35)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'propCard'
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    block = db.Column(db.String(9))
    lot = db.Column(db.String(9))
    building_no = db.Column(db.String(10))
    street = db.Column(db.String(40))
    description = db.Column(db.String(40))
    certified = db.Column(db.Boolean)
    mail_pickup = db.Column(db.Boolean)
    comment = db.Column(db.String(35))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                borough,
                block,
                lot,
                building_no,
                street,
                description,
                certified,
                mail_pickup,
                comment,
                sub_order_no
    ):
        self.borough = borough
        self.block = block
        self.lot = lot
        self.building_no = building_no
        self.street = street
        self.description = description
        self.certified = certified
        self.mail_pickup = mail_pickup
        self.comment = comment
        self.sub_order_no = sub_order_no
