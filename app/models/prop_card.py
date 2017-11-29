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
    contact_no -- Column: String(35)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'prop_card'
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    block = db.Column(db.String(9), nullable=True)
    lot = db.Column(db.String(9), nullable=True)
    building_no = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(40), nullable=True)
    certified = db.Column(db.Boolean, nullable=False)
    mail_pickup = db.Column(db.Boolean, nullable=False)
    contact_info = db.Column(db.String(35), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborder.id'), nullable=False)

    def __init__(
                self,
                borough,
                building_no,
                street,
                certified,
                mail_pickup,
                contact_info,
                suborder_number
    ):
        self.borough = borough
        self.block = block
        self.lot = lot
        self.building_no = building_no
        self.street = street
        self.description = description
        self.certified = certified
        self.mail_pickup = mail_pickup
        self.contact_info = contact_info or None
        self.suborder_number = suborder_number
