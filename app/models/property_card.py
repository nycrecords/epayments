from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from app.constants import borough


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
    mail -- Column: Bool
    contact_no -- Column: String(35)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'property_card'
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(
        db.Enum(
            borough.BRONX,
            borough.MANHATTAN,
            borough.STATEN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name='borough'), default=None, nullable=True)
    block = db.Column(db.String(9), nullable=True)
    lot = db.Column(db.String(9), nullable=True)
    building_no = db.Column(db.String(10), nullable=True)
    street = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(40), nullable=True)
    certified = db.Column(db.String(40), nullable=True)
    mail = db.Column(db.Boolean, nullable=True)
    contact_info = db.Column(db.String(35), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
                self,
                borough,
                block,
                lot,
                building_no,
                street,
                description,
                certified,
                mail,
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
        self.mail = mail
        self.contact_info = contact_info or None
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "borough": self.borough,
            "block": self.block,
            "lot": self.lot,
            "building_no": self.building_no,
            "street": self.street,
            "description": self.description,
            "certified": self.certified,
            "mail": self.mail,
            "contact_info": self.contact_info,
            'suborder_number': self.suborder_number
        }
