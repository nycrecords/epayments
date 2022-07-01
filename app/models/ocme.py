from sqlalchemy.dialects import postgresql

from app import db
from app.constants import borough, delivery_method


class OCME(db.Model):
    """
    id
    borough
    date
    first_name
    middle_name
    last_name
    age
    certificate_number
    num_copies
    raised_seal
    delivery_method
    """
    __tablename__ = "ocme"
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(
        postgresql.ENUM(
            borough.BRONX,
            borough.MANHATTAN,
            borough.STATEN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name="borough",
            create_type=False
        ), nullable=False)
    date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    middle_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    age = db.Column(db.String(3), nullable=True)
    certificate_number = db.Column(db.String(40), nullable=True)
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
            date,
            first_name,
            last_name,
            num_copies,
            raised_seal,
            delivery_method,
            suborder_number,
            middle_name=None,
            age=None,
            certificate_number=None,
            raised_seal_copies=None,
            contact_number=None,
            contact_email=None,
    ):
        self.borough = borough
        self.date = date
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.certificate_number = certificate_number
        self.num_copies = num_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies
        self.delivery_method = delivery_method
        self.contact_number = contact_number
        self.contact_email = contact_email
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        return {
            "id": self.id,
            "borough": self.borough,
            "date": self.date,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "age": self.age,
            "certificate_number": self.certificate_number,
            "num_copies": self.num_copies,
            "raised_seal": self.raised_seal,
            "raised_seal_copies": self.raised_seal_copies,
            "delivery_method": self.delivery_method,
            "contact_number": self.contact_number,
            "contact_email": self.contact_email,
            "suborder_number": self.suborder_number
        }
