from sqlalchemy.dialects import postgresql

from app import db
from app.constants import delivery_method


class HVR(db.Model):
    """

    """
    ___tablename__ = "hvr"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(256), nullable=False)
    record_id = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(16), nullable=False)
    num_copies = db.Column(db.String(40), nullable=False)
    exemplification = db.Column(db.Boolean, nullable=False)
    exemplification_copies = db.Column(db.String(1), nullable=True)
    raised_seal = db.Column(db.Boolean, nullable=False)
    raised_seal_copies = db.Column(db.String(1), nullable=True)
    no_amends = db.Column(db.Boolean, nullable=False)
    no_amends_copies = db.Column(db.String(1), nullable=True)
    delivery_method = db.Column(
        postgresql.ENUM(
            delivery_method.MAIL,
            delivery_method.EMAIL,
            delivery_method.PICKUP,
            name="delivery_method",
            create_type=False,
        ), nullable=False)
    suborder_number = db.Column(db.String(32), db.ForeignKey("suborders.id"), nullable=False)

    def __init__(
            self,
            link,
            record_id,
            _type,
            num_copies,
            exemplification,
            raised_seal,
            no_amends,
            _delivery_method,
            suborder_number,
            exemplification_copies=None,
            raised_seal_copies=None,
            no_amends_copies=None,
    ):
        self.link = link
        self.record_id = record_id
        self.type = _type
        self.num_copies = num_copies
        self.exemplification = exemplification
        self.exemplification_copies = exemplification_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies
        self.no_amends = no_amends
        self.no_amends_copies = no_amends_copies
        self.delivery_method = _delivery_method
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "link": self.link,
            "record_id": self.record_id,
            "type": self.type,
            "num_copies": self.num_copies,
            "exemplification": self.exemplification,
            "exemplification_copies": self.exemplification_copies,
            "raised_seal": self.raised_seal,
            "raised_seal_copies": self.raised_seal_copies,
            "no_amends": self.no_amends,
            "no_amends_copies": self.no_amends_copies,
            "delivery_method": self.delivery_method,
            "suborder_number": self.suborder_number,
        }
