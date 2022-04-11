from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app.constants import delivery_method


class MarriageSearch(db.Model):
    """

    Define the class with these following relationships

    groom_last_name -- Column: String(25)
    groom_first_name -- Column: String(40)
    bride_last_name -- Column: String(25)
    bride_first_name -- Column: String(40)
    num_copies -- Column: string // put as 40 because new one is 40
    month -- Column: string
    day -- Column: string
    year -- Column: enum[5 years]
    marriage_place -- Column: String(40)
    borough -- Column: String/Array?
    letter -- Column: bool
    comment -- Column: String(255)
    sub_order_num -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'marriage_search'
    id = db.Column(db.Integer, primary_key=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_middle_name = db.Column(db.String(40), nullable=True)
    bride_first_name = db.Column(db.String(40), nullable=True)
    alt_bride_last_name = db.Column(db.String(25), nullable=True)
    alt_bride_middle_name = db.Column(db.String(40), nullable=True)
    alt_bride_first_name = db.Column(db.String(40), nullable=True)
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_middle_name = db.Column(db.String(40), nullable=True)
    groom_first_name = db.Column(db.String(40), nullable=True)
    alt_groom_last_name = db.Column(db.String(25), nullable=True)
    alt_groom_middle_name = db.Column(db.String(40), nullable=True)
    alt_groom_first_name = db.Column(db.String(40), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=False, name='years')
    marriage_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    num_copies = db.Column(db.String(40), nullable=False)
    exemplification = db.Column(db.Boolean, nullable=True)
    exemplification_copies = db.Column(db.String(1), nullable=True)
    raised_seal = db.Column(db.Boolean, nullable=False)
    raised_seal_copies = db.Column(db.String(1), nullable=True)
    no_amends = db.Column(db.Boolean, nullable=False)
    no_amends_copies = db.Column(db.String(1), nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    delivery_method = db.Column(
        db.Enum(
            delivery_method.MAIL,
            delivery_method.EMAIL,
            delivery_method.PICKUP,
            name='delivery_method'
        ), nullable=True
    )
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            bride_last_name,
            groom_last_name,
            _years,
            _borough,
            num_copies,
            raised_seal,
            no_amends,
            _delivery_method,
            suborder_number,
            bride_middle_name=None,
            bride_first_name=None,
            alt_bride_last_name=None,
            alt_bride_middle_name=None,
            alt_bride_first_name=None,
            groom_middle_name=None,
            groom_first_name=None,
            alt_groom_last_name=None,
            alt_groom_middle_name=None,
            alt_groom_first_name=None,
            month=None,
            day=None,
            marriage_place=None,
            exemplification=None,
            exemplification_copies=None,
            raised_seal_copies=None,
            no_amends_copies=None,
            comment=None,
    ):
        self.bride_last_name = bride_last_name
        self.bride_middle_name = bride_middle_name
        self.bride_first_name = bride_first_name
        self.alt_bride_last_name = alt_bride_last_name
        self.alt_bride_middle_name = alt_bride_middle_name
        self.alt_bride_first_name = alt_bride_first_name
        self.groom_last_name = groom_last_name
        self.groom_middle_name = groom_middle_name
        self.groom_first_name = groom_first_name
        self.alt_groom_last_name = alt_groom_last_name
        self.alt_groom_middle_name = alt_groom_middle_name
        self.alt_groom_first_name = alt_groom_first_name
        self.month = month
        self.day = day
        self._years = _years
        self.marriage_place = marriage_place
        self._borough = _borough
        self.num_copies = num_copies
        self.exemplification = exemplification
        self.exemplification_copies = exemplification_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies
        self.no_amends = no_amends
        self.no_amends_copies = no_amends_copies
        self.comment = comment
        self.delivery_method = _delivery_method
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ", ".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if isinstance(self._borough, list):
            if len(self._borough) > 1:
                return ", ".join(self._borough)
            else:
                return self._borough[0]
        else:
            return None

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'bride_last_name': self.bride_last_name,
            'bride_middle_name': self.bride_middle_name,
            'bride_first_name': self.bride_first_name,
            'alt_bride_last_name': self.alt_bride_last_name,
            'alt_bride_middle_name': self.alt_bride_middle_name,
            'alt_bride_first_name': self.alt_bride_first_name,
            'groom_last_name': self.groom_last_name,
            'groom_middle_name': self.groom_middle_name,
            'groom_first_name': self.groom_first_name,
            'alt_groom_last_name': self.alt_groom_last_name,
            'alt_groom_middle_name': self.alt_groom_middle_name,
            'alt_groom_first_name': self.alt_groom_first_name,
            'month': self.month,
            'day': self.day,
            '_years': self._years,
            'marriage_place': self.marriage_place,
            '_borough': self._borough,
            'num_copies': self.num_copies,
            'exemplification': self.exemplification,
            'exemplification_copies': self.exemplification_copies,
            'raised_seal': self.raised_seal,
            'raised_seal_copies': self.raised_seal_copies,
            'no_amends': self.no_amends,
            'no_amends_copies': self.no_amends_copies,
            'comment': self.comment,
            'delivery_method': self.delivery_method,
            'suborder_number': self.suborder_number
        }


class MarriageCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_num -- Column: String(40)
    groom_last_name -- Column: String(25)
    groom_first_name -- Column: String(40)
    bride_last_name -- Column: String(25)
    bride_first_name -- Column: String(40)
    num_copies -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: enum[5 years]
    marriage_place -- Column: String(40)
    borough -- Column: String/Array?
    letter -- Column: Bool
    comment -- Column: String(255)
    sub_order_num -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'marriage_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(40))
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_first_name = db.Column(db.String(40), nullable=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_first_name = db.Column(db.String(40), nullable=True)
    num_copies = db.Column(db.String(40), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True, name='years')
    marriage_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    delivery_method = db.Column(
        db.Enum(
            delivery_method.MAIL,
            delivery_method.EMAIL,
            delivery_method.PICKUP,
            name='delivery_method'
        ), nullable=True
    )
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            certificate_number,
            groom_last_name,
            groom_first_name,
            bride_last_name,
            bride_first_name,
            num_copies,
            month,
            day,
            years,
            marriage_place,
            borough,
            letter,
            comment,
            _delivery_method,
            suborder_number
    ):
        self.certificate_number = certificate_number
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name
        self.num_copies = num_copies
        self.month = month or None
        self.day = day or None
        self._years = years or None
        self.marriage_place = marriage_place or None
        self._borough = borough or None
        self.letter = letter or None
        self.comment = comment or None
        self.delivery_method = _delivery_method
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ", ".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if isinstance(self._borough, list):
            if len(self._borough) > 1:
                return ", ".join(self._borough)
            else:
                return self._borough[0]
        else:
            return None

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'certificate_number': self.certificate_number,
            'groom_last_name': self.groom_last_name,
            'groom_first_name': self.groom_first_name,
            'bride_last_name': self.bride_last_name,
            'bride_first_name': self.bride_first_name,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': self.years if self.years is not None else "",
            'marriage_place': self.marriage_place,
            'borough': self.borough if self.borough is not None else "",
            'letter': self.letter,
            'comment': self.comment,
            'delivery_method': self.delivery_method,
            'suborder_number': self.suborder_number
        }
