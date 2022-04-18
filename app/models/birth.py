from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app.constants import gender, order_types, delivery_method


class BirthSearch(db.Model):
    """

    Define the class with these following relationships

    first_name -- Column: String(40)
    last_name -- Column: String(25)
    middle_name -- Column: String(40)
    gender -- Column: enum[M,F]
    father_name -- Column: string(40)
    mother_name -- Column: string(40)
    num_copies -- Column: string // put as 40 new one is 40
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[5] 1-D
    letter -- Column: Bool
    comment -- Column: string(255)
    suborder_number -- Column: BigInteger, foreignKey
    """
    __tablename__ = 'birth_search'
    __mapper_args__ = {'polymorphic_identity': order_types.BIRTH_SEARCH}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(40), nullable=True)
    alt_first_name = db.Column(db.String(40), nullable=True)
    alt_last_name = db.Column(db.String(25), nullable=True)
    alt_middle_name = db.Column(db.String(40), nullable=True)
    gender = db.Column(
        db.Enum(
            gender.MALE,
            gender.FEMALE,
            name='gender_type'), nullable=True)
    father_name = db.Column(db.String(105), nullable=True)
    mother_name = db.Column(db.String(105), nullable=True)
    num_copies = db.Column(db.String(4), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=False, name='years')
    birth_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    comment = db.Column(db.String(255), nullable=True)
    exemplification = db.Column(db.Boolean, nullable=True)
    exemplification_copies = db.Column(db.String(1), nullable=True)
    raised_seal = db.Column(db.Boolean, nullable=False)
    raised_seal_copies = db.Column(db.String(1), nullable=True)
    no_amends = db.Column(db.Boolean, nullable=False)
    no_amends_copies = db.Column(db.String(1), nullable=True)
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
            last_name,
            num_copies,
            years,
            borough,
            exemplification,
            raised_seal,
            no_amends,
            _delivery_method,
            suborder_number,
            first_name=None,
            middle_name=None,
            alt_first_name=None,
            alt_last_name=None,
            alt_middle_name=None,
            gender=None,
            father_name=None,
            mother_name=None,
            month=None,
            day=None,
            birth_place=None,
            exemplification_copies=None,
            raised_seal_copies=None,
            no_amends_copies=None,
            comment=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.alt_first_name = alt_first_name,
        self.alt_last_name = alt_last_name,
        self.alt_middle_name = alt_middle_name,
        self.gender = gender
        self.father_name = father_name
        self.mother_name = mother_name
        self.num_copies = num_copies
        self.month = month
        self.day = day
        self._years = years
        self.birth_place = birth_place
        self._borough = borough
        self.comment = comment
        self.exemplification = exemplification
        self.exemplification_copies = exemplification_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies
        self.no_amends = no_amends
        self.no_amends_copies = no_amends_copies
        self.delivery_method = _delivery_method
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ",".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if len(self._borough) > 1:
            return ", ".join(self._borough)
        else:
            return self._borough[0]

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'alt_first_name': self.alt_first_name,
            'alt_last_name': self.alt_last_name,
            'alt_middle_name': self.alt_middle_name,
            'gender': self.gender,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': str(self.years),
            'birth_place': self.birth_place,
            'borough': self.borough,
            'comment': self.comment,
            'exemplification': self.exemplification,
            'exemplification_copies': self.exemplification_copies,
            'raised_seal': self.raised_seal,
            'raised_seal_copies': self.raised_seal_copies,
            'no_amends': self.no_amends,
            'no_amends_copies': self.no_amends_copies,
            'delivery_method': self.delivery_method,
            'suborder_number': self.suborder_number
        }


class BirthCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_number -- Column: String(40)
    first_name -- Column: String(40)
    last_name -- Column: String(25)
    middle_name -- Column: String(40)
    gender -- Column: enum[M,F]
    father_name -- Column: string(40)
    mother_name -- Column: string(40)
    num_copies -- Column: String(40)
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[]
    letter -- Column: Bool
    comment -- Column: string(255)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'birth_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_number = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(40), nullable=True)
    alt_first_name = db.Column(db.String(40), nullable=True)
    alt_last_name = db.Column(db.String(25), nullable=True)
    alt_middle_name = db.Column(db.String(40), nullable=True)
    gender = db.Column(
        db.Enum(
            gender.MALE,
            gender.FEMALE,
            name='gender_type'), nullable=True)
    father_name = db.Column(db.String(105), nullable=True)
    mother_name = db.Column(db.String(105), nullable=True)
    num_copies = db.Column(db.String(4), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=False, name='years')
    birth_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    comment = db.Column(db.String(255), nullable=True)
    exemplification = db.Column(db.Boolean, nullable=True)
    exemplification_copies = db.Column(db.String(1), nullable=True)
    raised_seal = db.Column(db.Boolean, nullable=False)
    raised_seal_copies = db.Column(db.String(1), nullable=True)
    no_amends = db.Column(db.Boolean, nullable=False)
    no_amends_copies = db.Column(db.String(1), nullable=True)
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
            last_name,
            num_copies,
            years,
            borough,
            exemplification,
            raised_seal,
            no_amends,
            _delivery_method,
            suborder_number,
            first_name=None,
            middle_name=None,
            alt_first_name=None,
            alt_last_name=None,
            alt_middle_name=None,
            gender=None,
            father_name=None,
            mother_name=None,
            month=None,
            day=None,
            birth_place=None,
            comment=None,
            exemplification_copies=None,
            raised_seal_copies=None,
            no_amends_copies=None,
    ):
        self.certificate_number = certificate_number
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.alt_first_name = alt_first_name
        self.alt_last_name = alt_last_name
        self.alt_middle_name = alt_middle_name
        self.gender = gender
        self.father_name = father_name
        self.mother_name = mother_name
        self.num_copies = num_copies
        self.month = month
        self.day = day
        self._years = years
        self.birth_place = birth_place
        self._borough = borough
        self.comment = comment
        self.exemplification = exemplification
        self.exemplification_copies = exemplification_copies
        self.raised_seal = raised_seal
        self.raised_seal_copies = raised_seal_copies
        self.no_amends = no_amends
        self.no_amends_copies = no_amends_copies
        self.delivery_method = _delivery_method
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ",".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if len(self._borough) > 1:
            return ", ".join(self._borough)
        else:
            return self._borough[0]

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'certificate_number': self.certificate_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'alt_first_name': self.alt_first_name,
            'alt_last_name': self.alt_last_name,
            'alt_middle_name': self.alt_middle_name,
            'gender': self.gender,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': self.years,
            'birth_place': self.birth_place,
            'borough': self.borough,
            'comment': self.comment,
            'exemplification': self.exemplification,
            'exemplification_copies': self.exemplification_copies,
            'raised_seal': self.raised_seal,
            'raised_seal_copies': self.raised_seal_copies,
            'no_amends': self.no_amends,
            'no_amends_copies': self.no_amends_copies,
            'delivery_method': self.delivery_method,
            'suborder_number': self.suborder_number
        }
