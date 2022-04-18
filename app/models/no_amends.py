from sqlalchemy.dialects import postgresql

from app import db
from app.constants import delivery_method


class NoAmends(db.Model):
    """
    id
    """
    __tablename__ = "no_amends"
    id = db.Column(db.Integer, primary_key=True)
    num_copies = db.Column(db.String(1), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    delivery_method = db.Column(
        postgresql.ENUM(
            delivery_method.MAIL,
            delivery_method.EMAIL,
            delivery_method.PICKUP,
            name="delivery_method",
            create_type=False,
        ), nullable=False)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            num_copies,
            filename,
            delivery_method,
            suborder_number,
    ):
        self.num_copies = num_copies
        self.filename = filename
        self.delivery_method = delivery_method
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        return {
            "id": self.id,
            "num_copies": self.num_copies,
            "filename": self.filename,
            "delivery_method": self.delivery_method,
            "suborder_number": self.suborder_number
        }
