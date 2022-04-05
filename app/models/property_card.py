from sqlalchemy.dialects import postgresql

from app import db
from app.constants import borough, delivery_method


class PropertyCard(db.Model):
    """
    Define the class with these following relationships

    borough -- Column: Enum
    block -- Column: String(9)
    lot -- Column: String(9)
    building_number -- Column: String(10)
    street -- Column: String(40)
    description -- Column: String(35)
    certified -- Column: Bool
    mail -- Column: Bool
    contact_no -- Column: String(35)
    suborder_number -- Column: BigInteger, foreignKey

    """
    __tablename__ = 'property_card'
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(
        postgresql.ENUM(
            borough.BRONX,
            borough.MANHATTAN,
            borough.STATEN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name='borough'), default=None, nullable=False)
    block = db.Column(db.String(9), nullable=False)
    lot = db.Column(db.String(9), nullable=False)
    building_number = db.Column(db.String(10), nullable=True)
    street = db.Column(db.String(40), nullable=True)
    num_copies = db.Column(db.String(1), nullable=False)
    raised_seal = db.Column(db.Boolean, nullable=False)
    raised_seal_copies = db.Column(db.String(1), nullable=True)
    delivery_method = db.Column(
        postgresql.ENUM(
            delivery_method.MAIL,
            delivery_method.EMAIL,
            delivery_method.PICKUP,
            name="delivery_method",
            create_type=False,
        ), nullable=False)
    contact_number = db.Column(db.String(64), nullable=True)
    contact_email = db.Column(db.String(256), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            borough,
            block,
            lot,
            building_number,
            street,
            num_copies,
            raised_seal,
            raised_seal_copies,
            delivery_method,
            contact_number,
            contact_email,
            suborder_number
    ):
        self.borough = borough
        self.block = block
        self.lot = lot
        self.building_number = building_number or None
        self.street = street or None
        self.num_copies = num_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies or None
        self.delivery_method = delivery_method
        self.contact_number = contact_number or None
        self.contact_email = contact_email or None
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "borough": self.borough,
            "block": self.block,
            "lot": self.lot,
            "building_number": self.building_number,
            "street": self.street,
            "num_copies": self.num_copies,
            "raised_seal": self.raised_seal,
            "raised_seal_copies": self.raised_seal_copies,
            "delivery_method": self.delivery_method,
            "contact_number": self.contact_number,
            "contact_email": self.contact_email,
            "suborder_number": self.suborder_number
        }
