from app import db
from app.constants import purpose
from sqlalchemy.dialects.postgresql import ARRAY


class MarriageSearch(db.Model):
    """

    Define the class with these following relationships

    groom_last_name -- Column: String(25)
    groom_first_name -- Column: String(40)
    bride_last_name -- Column: String(25)
    bride_first_name -- Column: String(40)
    relationship -- Column: String(30)
    purpose -- Column: enum[Genealogical/Historical, Personal Use, Legal, Immigration, Medicaid/Social Security
                            Health, Other] 7 Total different selection fields
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
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_first_name = db.Column(db.String(40), nullable=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_first_name = db.Column(db.String(40), nullable=True)
    relationship = db.Column(db.String(30), nullable=True)
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'), default=purpose.OTHER, nullable=False)
    num_copies = db.Column(db.String(40), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=False, name='years')
    marriage_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            groom_last_name,
            groom_first_name,
            bride_last_name,
            bride_first_name,
            relationship,
            purpose,
            num_copies,
            month,
            day,
            years,
            marriage_place,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name
        self.relationship = relationship
        self.purpose = purpose
        self.num_copies = num_copies
        self.month = month or None
        self.day = day or None
        self._years = years
        self.marriage_place = marriage_place or None
        self._borough = borough
        self.letter = letter or None
        self.comment = comment or None
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
            'groom_last_name': self.groom_last_name,
            'groom_first_name': self.groom_first_name,
            'bride_last_name': self.bride_last_name,
            'bride_first_name': self.bride_first_name,
            'relationship': self.relationship,
            'purpose': self.purpose,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': self.years if self.years is not None else "",
            'marriage_place': self.marriage_place,
            'borough': self.borough if self.borough is not None else "",
            'letter': self.letter,
            'comment': self.comment,
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
    relationship -- Column: String(30)
    purpose -- Column: enum[]
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
    certificate_no = db.Column(db.String(40))
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_first_name = db.Column(db.String(40), nullable=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_first_name = db.Column(db.String(40), nullable=True)
    relationship = db.Column(db.String(30), nullable=True)
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'), default=purpose.OTHER, nullable=False)
    num_copies = db.Column(db.String(40), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True, name='years')
    marriage_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            certificate_no,
            groom_last_name,
            groom_first_name,
            bride_last_name,
            bride_first_name,
            relationship,
            purpose,
            num_copies,
            month,
            day,
            years,
            marriage_place,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.certificate_no = certificate_no
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name
        self.relationship = relationship
        self.purpose = purpose
        self.num_copies = num_copies
        self.month = month or None
        self.day = day or None
        self._years = years or None
        self.marriage_place = marriage_place or None
        self._borough = borough or None
        self.letter = letter or None
        self.comment = comment or None
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
            'certificate_no': self.certificate_no,
            'groom_last_name': self.groom_last_name,
            'groom_first_name': self.groom_first_name,
            'bride_last_name': self.bride_last_name,
            'bride_first_name': self.bride_first_name,
            'relationship': self.relationship,
            'purpose': self.purpose,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': self.years if self.years is not None else "",
            'marriage_place': self.marriage_place,
            'borough': self.borough if self.borough is not None else "",
            'letter': self.letter,
            'comment': self.comment,
            'suborder_number': self.suborder_number
        }
